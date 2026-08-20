#!/usr/bin/env python3
"""Build the LaTeX edition, with optional post-build PDF optimization."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


PROFILES = ("lossless", "print", "ebook", "screen")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--optimize",
        nargs="?",
        const="lossless",
        choices=PROFILES,
        metavar="PROFILE",
        help="optimize book.pdf after building (default profile: lossless)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    latex_dir = Path(__file__).resolve().parent
    command = ["latexmk"]
    # A forced build ensures that a lossy profile is always applied to fresh
    # pdfTeX output instead of recompressing an earlier optimized build.
    if args.optimize:
        command.append("-g")
    command.extend(["-pdf", "-halt-on-error", "-file-line-error", "book.tex"])

    try:
        subprocess.run(command, cwd=latex_dir, check=True)
        if args.optimize:
            subprocess.run(
                [
                    sys.executable,
                    str(latex_dir.parent / "optimize_pdf.py"),
                    str(latex_dir / "book.pdf"),
                    "--profile",
                    args.optimize,
                    "--replace",
                ],
                cwd=latex_dir,
                check=True,
            )
    except FileNotFoundError as error:
        print(f"Build tool not found: {error.filename}", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as error:
        return error.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
