#!/usr/bin/env python3
"""Create a smaller PDF and verify that its page count is unchanged.

The ``lossless`` profile only rewrites and recompresses PDF objects.  The other
profiles use Ghostscript to downsample raster images; vector artwork and text
remain vector content.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import pymupdf


PROFILES = {
    "lossless": "lossless object cleanup and stream compression",
    "print": "300 dpi images (high-quality print copy)",
    "ebook": "150 dpi images (recommended distribution copy)",
    "screen": "72 dpi images (smallest screen-only copy)",
}

GHOSTSCRIPT_PROFILES = {
    "print": "printer",
    "ebook": "ebook",
    "screen": "screen",
}


def human_size(size: int) -> str:
    """Format a byte count for build output."""
    value = float(size)
    for unit in ("B", "KiB", "MiB", "GiB"):
        if value < 1024 or unit == "GiB":
            return f"{value:.1f} {unit}"
        value /= 1024
    raise AssertionError("unreachable")


def _lossless_rewrite(source: Path, destination: Path) -> None:
    with pymupdf.open(source) as document:
        if document.needs_pass:
            raise ValueError(f"cannot optimize password-protected PDF: {source}")
        document.save(
            destination,
            garbage=4,
            clean=True,
            deflate=True,
            deflate_images=True,
            deflate_fonts=True,
            use_objstms=1,
            compression_effort=100,
        )


def _ghostscript_rewrite(source: Path, destination: Path, profile: str) -> None:
    ghostscript = shutil.which("gs")
    if ghostscript is None:
        raise RuntimeError(
            f"the {profile!r} profile requires Ghostscript (the 'gs' command)"
        )
    subprocess.run(
        [
            ghostscript,
            "-q",
            "-dBATCH",
            "-dNOPAUSE",
            "-dSAFER",
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.7",
            f"-dPDFSETTINGS=/{GHOSTSCRIPT_PROFILES[profile]}",
            "-dAutoRotatePages=/None",
            "-dDetectDuplicateImages=true",
            "-dCompressFonts=true",
            "-dSubsetFonts=true",
            f"-sOutputFile={destination}",
            str(source),
        ],
        check=True,
    )


def _page_count(path: Path) -> int:
    with pymupdf.open(path) as document:
        if document.needs_pass:
            raise ValueError(f"cannot verify password-protected PDF: {path}")
        return document.page_count


def optimize_pdf(source: Path, output: Path, profile: str) -> bool:
    """Optimize ``source`` atomically; return whether a smaller file was kept."""
    source = source.resolve()
    output = output.resolve()
    if profile not in PROFILES:
        raise ValueError(
            f"unknown profile {profile!r}; choose from {', '.join(PROFILES)}"
        )
    if not source.is_file():
        raise FileNotFoundError(f"input PDF not found: {source}")
    if source.suffix.lower() != ".pdf" or output.suffix.lower() != ".pdf":
        raise ValueError("input and output paths must end in .pdf")
    output.parent.mkdir(parents=True, exist_ok=True)

    original_pages = _page_count(source)
    original_size = source.stat().st_size
    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{output.stem}.", suffix=".tmp.pdf", dir=output.parent
    )
    os.close(file_descriptor)
    temporary = Path(temporary_name)
    temporary.unlink()

    try:
        if profile == "lossless":
            _lossless_rewrite(source, temporary)
        else:
            _ghostscript_rewrite(source, temporary, profile)

        optimized_pages = _page_count(temporary)
        if optimized_pages != original_pages:
            raise RuntimeError(
                "optimized PDF failed verification: "
                f"expected {original_pages} pages, found {optimized_pages}"
            )
        optimized_size = temporary.stat().st_size

        # An optimization pass can occasionally add a little overhead to an
        # already optimized PDF.  Never replace or create an output with a
        # candidate that is not actually smaller.
        if optimized_size >= original_size:
            print(
                f"Skipped {output.name}: {profile} output was not smaller "
                f"than {source.name} ({human_size(original_size)})."
            )
            return False

        os.replace(temporary, output)
        saving = 100 * (original_size - optimized_size) / original_size
        print(
            f"Optimized {output.name} with {profile}: "
            f"{human_size(original_size)} -> {human_size(optimized_size)} "
            f"({saving:.1f}% smaller), {optimized_pages} pages verified."
        )
        return optimized_size < original_size
    finally:
        temporary.unlink(missing_ok=True)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="PDF to optimize")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output PDF (defaults to INPUT-PROFILE.pdf)",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="atomically replace the input only when the result is smaller",
    )
    parser.add_argument(
        "--profile",
        choices=PROFILES,
        default="lossless",
        help="compression profile (default: lossless)",
    )
    args = parser.parse_args(argv)
    if args.replace and args.output is not None:
        parser.error("--replace and --output cannot be used together")
    if args.replace:
        args.output = args.input
    elif args.output is None:
        args.output = args.input.with_name(
            f"{args.input.stem}-{args.profile}{args.input.suffix}"
        )
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        optimize_pdf(args.input, args.output, args.profile)
    except (OSError, RuntimeError, ValueError, subprocess.CalledProcessError) as error:
        print(f"PDF optimization failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
