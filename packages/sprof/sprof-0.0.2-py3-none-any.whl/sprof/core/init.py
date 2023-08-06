"""
Code for creating new sprof projects.
"""
from pathlib import Path
from typing import Optional, Union

import jinja2

import sprof
from sprof.core.meta import write_metadata


def _init_directory(template_directory, output_directory, data):
    """render each template into output directory."""
    for path in Path(template_directory).rglob("*"):
        if path.is_dir():
            continue
        template_contents = path.read_text()
        template = jinja2.Template(template_contents)
        out = template.render(data)
        new_path = output_directory / path.relative_to(template_directory)
        if new_path.exists():
            continue
        new_path.parent.mkdir(exist_ok=True, parents=True)
        # dont copy example script if a010 already exists
        is_a010 = new_path.name.startswith("a010")
        has_a010 = bool(list(output_directory.glob("a010*.py")))
        if is_a010 and has_a010:
            continue
        # finally. copy rendered template file.
        with new_path.open("w") as fi:
            fi.write(out)


def init(path: Optional[Union[Path, str]] = None) -> Path:
    """
    Initiate an sprof project.

    Parameters
    ----------
    path
        The path of the target directory. If it does not exist it will be created.
        If not provided, use current working directory.

    Returns
    -------
    A path to the new project.

    """
    path = Path(path) if path is not None else Path.cwd()
    path.mkdir(exist_ok=True, parents=True)
    data = {"project_name": path.name}
    _init_directory(sprof._template_path, path, data=data)
    write_metadata(path)
    return path
