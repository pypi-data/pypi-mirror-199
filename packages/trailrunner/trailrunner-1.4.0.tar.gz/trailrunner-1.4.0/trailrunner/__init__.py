# Copyright 2022 Amethyst Reese
# Licensed under the MIT license

"""
Run things on paths
"""

__author__ = "Amethyst Reese"
from .__version__ import __version__
from .core import (
    gitignore,
    project_root,
    run,
    run_iter,
    Trailrunner,
    walk,
    walk_and_run,
)

__all__ = [
    "__author__",
    "__version__",
    "gitignore",
    "project_root",
    "run",
    "run_iter",
    "Trailrunner",
    "walk",
    "walk_and_run",
]
