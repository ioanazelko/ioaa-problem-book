#!/usr/bin/env python
"""Locate the private IOAA source-paper archive outside this repository."""

import os


SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
REPOSITORY_DIR = os.path.dirname(SOURCE_DIR)
DEFAULT_PAPER_ROOT = os.path.join(
    os.path.dirname(REPOSITORY_DIR), "IOAA Source Papers"
)
PAPER_ROOT = os.path.abspath(
    os.path.expanduser(os.environ.get("IOAA_PAPERS_DIR", DEFAULT_PAPER_ROOT))
)
PAPER_DIRS = (PAPER_ROOT, os.path.join(PAPER_ROOT, "observation"))


def paper_path(filename):
    """Return the path to a source paper in the external archive."""
    if os.path.isabs(filename) and os.path.isfile(filename):
        return filename
    for directory in PAPER_DIRS:
        candidate = os.path.join(directory, filename)
        if os.path.isfile(candidate):
            return candidate
    raise FileNotFoundError(
        f"source paper {filename!r} not found under {PAPER_ROOT!r}; "
        "set IOAA_PAPERS_DIR to override the external archive location"
    )
