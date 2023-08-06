"""
Module which handles the creation of sprof metadata.
"""
from pathlib import Path
from typing import Union

import sprof
from sprof.utils import ensure_spf_project, path_or_cwd

METADATA_DIRECTORY_NAME = ".sprof"
SPF_VERSION_FILE_NAME = "spf_version.txt"


def get_doit_tasks(project_path):
    """Create dictionaries of doit tasks."""
    # local_contents = get_local_contents(project_path)


def _get_timestamps(path):
    """Get the timestamp for all python files in project."""
    out = {}
    for py_path in path.rglob("*.py"):
        rel = py_path.relative_to(path)
        ts = py_path.mtime
        out[rel] = ts
    return out


def default_metadata(project_path: Path):
    """return a dict of default metada."""
    out = dict(
        spf_version=sprof.__version__,
        time_stamps=_get_timestamps(project_path),
    )
    return out


def _write_version(spf_path):
    """Write the current version of sprof."""
    with (spf_path / SPF_VERSION_FILE_NAME).open("w") as fi:
        fi.write(sprof.__version__)


def _read_version(spf_path):
    """Read the version of sprof used to generate project."""
    with (spf_path / SPF_VERSION_FILE_NAME).open("r") as fi:
        out = fi.read().rstrip()
    return out


def write_metadata(project_path: Union[str, Path]):
    """Write the metadata to a path."""
    # get expected directory name and ensure it exists
    spf_path = Path(project_path) / METADATA_DIRECTORY_NAME
    spf_path.mkdir(exist_ok=True, parents=True)
    # parse project and write basic info.
    _write_version(spf_path)


def read_metadata(project_path):
    """Read metadata from project."""
    path = path_or_cwd(project_path)
    ensure_spf_project(path)
    spf_path = path / METADATA_DIRECTORY_NAME
    out = {
        "spf_version": _read_version(spf_path),
    }
    return out
