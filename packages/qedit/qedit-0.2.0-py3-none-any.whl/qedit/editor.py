import json
from vosk import Model, KaldiRecognizer, SetLogLevel
import typer
import subprocess
from subprocess import Popen
from pathlib import Path
from rich import print
from rich.progress import Progress
from rich.console import Console
import ffmpeg
import zipfile
import requests
import time


AUDIO_FRAMERATE = 16000
SetLogLevel(-1)
console = Console()
consoleError = Console(stderr=True)
MODEL_NAME = "vosk-model-small-en-us-0.15"
MODEL_URL = f"https://alphacephei.com/vosk/models/{MODEL_NAME}.zip"
MODEL_PATH = Path.home() / ".qedit" / MODEL_NAME


def convert_video_to_wav(video: str):
    return subprocess.Popen(
        [
            "ffmpeg",
            "-v",
            "error",
            "-i",
            video,
            "-ar",
            str(AUDIO_FRAMERATE),
            "-ac",
            "1",
            "-f",
            "s16le",
            "-",
        ],
        stdout=subprocess.PIPE,
    )


class Word:
    def __init__(self, start, end, word, conf):
        self.start = start
        self.end = end
        self.word = word
        self.conf = conf

    def __str__(self):
        return f"{self.word} ({self.start}, {self.end})"

    def __repr__(self):
        return self.__str__()


def download_model():
    if not MODEL_PATH.exists():
        response = typer.prompt(f"Model not found. Download to {MODEL_PATH} now? (y/n)")
        if response.lower() != "y":
            raise typer.Abort()

        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

        print(f"Downloading model from {MODEL_URL}...")
        response = requests.get(MODEL_URL)
        with open(f"{MODEL_NAME}.zip", "wb") as f:
            f.write(response.content)
        print(f"Extracting model to {MODEL_PATH}...")
        with zipfile.ZipFile(f"{MODEL_NAME}.zip", "r") as zip_ref:
            zip_ref.extractall(MODEL_PATH.parent)
        Path(f"{MODEL_NAME}.zip").unlink()
        print(f"Model downloaded and extracted to {MODEL_PATH}")
    else:
        print(f"Model already exists at {MODEL_PATH}")


def recognize_sections(
    process: Popen,
    duration: float,
    silence_delay: float = 1,
    silence_buffer: float = 0.5,
) -> list:
    if silence_buffer > silence_delay:
        raise typer.BadParameter("Silence buffer cannot be greater than silence delay.")

    if not MODEL_PATH.exists():
        download_model()

    print("Loading recognizer...")
    model = Model(str(MODEL_PATH))
    rec = KaldiRecognizer(model, AUDIO_FRAMERATE)

    rec.SetWords(True)

    results = []

    with Progress() as progress:
        task = progress.add_task(
            "Recognizing words...",
            total=2 * duration * AUDIO_FRAMERATE,
        )
        while True:
            data = process.stdout.read(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                jres = json.loads(rec.Result())
                results.append(jres)
            progress.update(task, advance=4000)
        progress.update(task, completed=2 * duration * AUDIO_FRAMERATE)

    part_result = json.loads(rec.FinalResult())
    results.append(part_result)

    words = []
    for sentence in results:
        if len(sentence) == 1:
            continue
        for word in sentence["result"]:
            words.append(Word(**word))
    words.remove(words[0])

    sections = []
    last_section = None
    for i in range(len(words) - 1):
        if last_section is None:
            last_section = (words[i].start, None)
        if words[i + 1].start - words[i].end > silence_delay:
            last_section = (
                last_section[0] - silence_buffer / 2,
                words[i].end + silence_buffer / 2,
            )
            sections.append(last_section)
            last_section = None
    if last_section is not None and last_section[1] is None:
        last_section = (last_section[0], words[-1].end)
        sections.append(last_section)

    sections[0] = (max(sections[0][0], 0), sections[0][1])
    sections[-1] = (sections[-1][0], min(sections[-1][1], words[-1].end))

    return sections


def generate_ffmpeg_commands(video: str, output: str, sections: list):
    in_file = ffmpeg.input(f"{video}")
    v = in_file.video
    a = in_file.audio

    print(f"Number of segments to cut: {len(sections)}")

    max_sections_per_batch = 128
    batches = len(sections) // max_sections_per_batch + 1
    spb = len(sections) / batches
    section_batches = [
        sections[round(i * spb) : round((i + 1) * spb)] for i in range(0, batches)
    ]

    commands = []
    for i, section_batch in enumerate(section_batches):
        filters = []
        for section, factor in section_batch:
            filters.append(
                v.trim(start=section[0], end=section[1]).filter(
                    "setpts", f"{1/factor}*PTS-STARTPTS"
                )
            )
            filters.append(
                a.filter("atrim", start=section[0], end=section[1])
                .filter("asetpts", f"PTS-STARTPTS")
                .filter("atempo", f"{factor}")
            )

        out = ffmpeg.concat(
            *filters,
            v=1,
            a=1,
        )
        out = ffmpeg.output(out, f"qedit_{i}_{output}")
        out = out.global_args(
            "-progress", "pipe:1", "-loglevel", "quiet", "-nostats", "-hide_banner"
        )
        out = ffmpeg.overwrite_output(out)

        commands.append(out)

    return commands


def monitor_progress_of_multiple_ffmpeg_processes(duration, processes):
    with Progress() as progress:
        task = progress.add_task(
            "Processing video...",
            total=duration * 1_000_000,
        )
        out_times = [0] * len(processes)
        while True:
            updated = False
            for i, process in enumerate(processes):
                line = process.stdout.readline()
                if not line:
                    continue
                updated = True
                line = line.decode("utf-8")
                if "out_time_ms" in line:
                    out_times[i] = int(line.split("=")[1])
            if not updated:
                break
            progress.update(task, completed=sum(out_times))
        progress.update(task, advance=duration * 1_000_000)


def monitor_progress_of_ffmpeg_process(duration, process):
    with Progress() as progress:
        task = progress.add_task(
            "Processing video...",
            total=duration * 1_000_000,
        )
        while True:
            line = process.stdout.readline()
            if not line:
                break
            line = line.decode("utf-8")
            if "out_time_ms" in line:
                progress.update(task, completed=int(line.split("=")[1]))
        progress.update(task, advance=duration * 1_000_000)


def run_ffmpeg(video: str, output: str, sections: list):
    commands = generate_ffmpeg_commands(video, output, sections)

    try:
        processes = []
        for command in commands:
            processes.append(command.run_async(pipe_stdout=True))

        duration = sum(
            [(section[1] - section[0]) * factor for section, factor in sections]
        )

        monitor_progress_of_multiple_ffmpeg_processes(duration, processes)

        # ensure all processes are finished
        for process in processes:
            process.wait()

        with open("qedit_filelist.txt", "w") as f:
            for i in range(len(commands)):
                f.write(f"file 'qedit_{i}_{output}'\n")

        concat = (
            ffmpeg.input("qedit_filelist.txt", f="concat", safe=0)
            .output(output)
            .global_args(
                "-progress", "pipe:1", "-loglevel", "quiet", "-nostats", "-hide_banner"
            )
            .overwrite_output()
        )

        with concat.run_async(pipe_stdout=True) as process:
            monitor_progress_of_ffmpeg_process(duration, process)
    except KeyboardInterrupt:
        print("Keyboard interrupt received, qutting...")
        for process in processes:
            process.kill()
        # It takes a very small amount of time for the processes to actually die
        time.sleep(0.1)

        Path(output).unlink(missing_ok=True)
    finally:
        for i in range(len(commands)):
            Path(f"qedit_{i}_{output}").unlink(missing_ok=True)

        Path("qedit_filelist.txt").unlink(missing_ok=True)


def cut_sections(
    video: str,
    content_sections: "list[tuple[float, float]]",
    output: str,
    content_factor: float = 1,
    whitespace_factor: float = 0,
):
    """Takes a clip and speeds up the content and whitespace sections by the content and whitespace factors respectively.

    Args:
        video (str): Input video file name.
        content_sections (list): Tuples of content start and end timestamps. Defaults to [].
        whitespace_sections (list, optional): Tuples of whitespace start and end timestamps. Defaults to [].
        output (str): Output file name.
        content_factor (float, optional): Speed up factor of content sections. Defaults to 1.
        whitespace_factor (float, optional): Speed up factor of whitespace sections. 0 to not include whitespace. Defaults to 0.
    """
    sections = []
    last_end = 0
    for section in content_sections:
        if whitespace_factor != 0 and section[0] - last_end > 0:
            sections.append(((last_end, section[0]), whitespace_factor))
        sections.append((section, content_factor))
        last_end = section[1]
    if whitespace_factor != 0 and last_end < content_sections[-1][1]:
        sections.append(((last_end, content_sections[-1][1]), whitespace_factor))

    run_ffmpeg(video, output, sections)


def edit(
    video: str,
    output: str,
    silence_delay: float,
    silence_buffer: float,
    content_factor: float,
    whitespace_factor: float,
):
    try:
        probe = ffmpeg.probe(video)
    except ffmpeg.Error as e:
        console.print_exception(e)

    print(f"Length of video: {round(float(probe['format']['duration']), 2)}s")
    with convert_video_to_wav(video) as process:
        sections = recognize_sections(
            process,
            float(probe["format"]["duration"]),
            silence_delay=silence_delay,
            silence_buffer=silence_buffer,
        )
    cut_sections(
        video,
        sections,
        output,
        content_factor,
        whitespace_factor,
    )
