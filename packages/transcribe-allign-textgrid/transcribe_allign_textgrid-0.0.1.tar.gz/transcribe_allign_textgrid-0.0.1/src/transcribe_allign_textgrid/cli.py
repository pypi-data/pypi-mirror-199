from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from importlib.util import find_spec
from pathlib import Path
from typing import List, Optional


# Preprocessing: Managing imports that are not in requirements.txt
def check_cli_dependencies() -> bool:
    if ffmpeg := shutil.which("ffmpeg") is None:
        print(
            """Dependency ffmpeg is not installed.
            Please install if following the instructions on whisper's documentation:
            https://github.com/openai/whisper-timestamped
            """
        )
    if timestamped := find_spec("whisper_timestamped") is None:
        print(
            """Dependency whisper-timestamped is not installed.
            This needs to be installed sperately, as it cannot be installed via pypi
            Please read the requirement documentation on:
            https://github.com/JJWRoeloffs/transcribe_allign_textgrid
            """
        )
    if whisper := find_spec("whisper") is None:
        print(
            """Dependency whisper is not installed.
            This should have been installed as a dependency of whisper-timestamped, but was not.
            It might be wise to reinstall whisper-timestamped, as something clearly went wrong.
            Else, if you want simply want this error to go away, install whisper manually.
            """
        )

    return whisper is not None and timestamped is not None and ffmpeg is not None


@dataclass
class Args:
    paths: List[Path]
    model: str
    language: Optional[str]


def parse_args(args: List[str]) -> Args:
    parser = argparse.ArgumentParser(
        prog="transcribe_allign_textgrid",
        description="""
            A small wrapper cli around whisper-timestamped.
            Create force-alligned transcription TextGrids from raw audio!
            """,
    )

    if not check_cli_dependencies():
        parser.error("Could not resolve all cli dependencies")

    from whisper import _MODELS
    from whisper.tokenizer import LANGUAGES

    parser.add_argument(
        "paths",
        help="The File(s) or Directory of the to-transcribe audio",
        nargs="+",
    )
    parser.add_argument(
        "--model",
        choices=_MODELS.keys(),
        help="The model size to use for the transcription. Default tiny",
        default="tiny",
        nargs="?",
        required=False,
    )
    parser.add_argument(
        "--language",
        choices=LANGUAGES.values(),
        help="Language size to use for the transcription, Default automatic",
        nargs="?",
        required=False,
    )
    arguments = parser.parse_args(args)
    paths = [Path(x) for x in arguments.paths]

    for path in paths:
        if not path.exists():
            parser.error(f"Passed path does not exist: {path}")

    return Args(paths=paths, model=arguments.model, language=arguments.language)


def run(args: Args) -> None:
    if not check_cli_dependencies():
        raise ImportError
    pass


def main(args: List[str]) -> None:
    arguments = parse_args(args)
    print(arguments.paths)
    print(arguments.model)
    print(arguments.language)
    run(arguments)
