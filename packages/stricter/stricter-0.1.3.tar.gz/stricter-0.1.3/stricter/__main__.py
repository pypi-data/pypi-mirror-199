import subprocess

import typer

DEFAULT_PATH = typer.Argument(".")
DEFAULT_IGNORE = "ANN101,ANN102,D"


class Options:
    BLACK = "-q"
    RUFF = "--fix --show-fixes --select ALL"
    MYPY = "--strict"


def main(path: str = DEFAULT_PATH, ignore: str = "") -> None:
    ignore = ",".join([DEFAULT_IGNORE, ignore]).strip(",")
    subprocess.run(f"black {path} {Options.BLACK}")
    subprocess.run(f"ruff {path} {Options.RUFF} --ignore {ignore}")
    subprocess.run(f"mypy {path} {Options.MYPY}")


typer.run(main)
