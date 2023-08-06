from typing import Optional
import typer
from rich import print
from pathlib import Path

from qedit import __app_name__, __version__, __author__, editor

app = typer.Typer(rich_markup_mode="rich")


def _version_callback(value: bool) -> None:
    if value:
        print(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback(
    epilog="A CLI by Tyler",
    help="A CLI for automatically [green]editing[/green] videos using [bold]word detection[/bold]. :movie_camera:",
    invoke_without_command=True,
)
def main(
    video: str = typer.Argument(..., help="The video to edit."),
    output: str = typer.Argument("output.mp4", help="The output video."),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
    silence_delay: float = typer.Option(
        1,
        "--silence-delay",
        "-d",
        help="The amount of silence (in seconds) to wait before cutting a section.",
    ),
    silence_buffer: float = typer.Option(
        0.5,
        "--silence-buffer",
        "-b",
        help="The amount of silence (in seconds) to keep between two adjacent sections.",
    ),
    content_factor: float = typer.Option(
        1,
        "--content-factor",
        "-c",
        help="The factor by which to speed up the content.",
    ),
    whitespace_factor: float = typer.Option(
        0,
        "--whitespace-factor",
        "-w",
        help="The factor by which to speed up the whitespace. 0 for no whitespace.",
    ),
) -> None:
    """
    Edit a video using word detection. :movie_camera:
    """
    if not Path(video).exists():
        raise typer.BadParameter(f"Video {video} does not exist.")
    else:
        print(f"Editing {video} and saving to {output}.")
        editor.edit(
            video,
            output,
            silence_delay,
            silence_buffer,
            content_factor,
            whitespace_factor,
        )
