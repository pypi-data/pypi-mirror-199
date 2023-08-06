"""
Command line interface for sprof.
"""
from typing import Optional

import typer

import sprof

app = typer.Typer()


@app.command()
def init(path: Optional[str] = typer.Argument(None)):
    """
    Create a new sprof project.

    Parameters
    ----------
    path
        The path to the new project directory. If None use cwd.
    """
    sprof.init(path)


@app.command()
def new(name: str):
    """
    Create a new sprof project.

    Parameters
    ----------
    name
        The name of the project (and directory).
    """
    typer.echo(f"Conquering reign: {name}")


if __name__ == "__main__":
    app()
