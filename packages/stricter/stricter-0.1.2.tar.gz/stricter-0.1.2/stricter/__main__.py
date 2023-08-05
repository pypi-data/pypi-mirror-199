import subprocess

import typer

DEFAULT_PATH = typer.Argument(".")


def main(path: str = DEFAULT_PATH) -> None:
    subprocess.run(f"black {path}")
    subprocess.run(f"ruff {path}")
    subprocess.run(f"mypy {path}")


typer.run(main)
