"""
Module for getting info about a sprof project.
"""
from pathlib import Path
from typing import Optional, Union

from sprof.core.meta import read_metadata


def info(project_path: Optional[Union[Path, str]] = None) -> dict:
    """
    Return info about a project.
    """
    data = read_metadata(project_path)
    return data
