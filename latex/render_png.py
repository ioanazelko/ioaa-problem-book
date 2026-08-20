#!/usr/bin/env python
"""Render a problem's source crop to PNG(s) for visual transcription.

Usage: python render_png.py 2016_TH_T11 [outdir]
Writes <outdir>/<id>-0.png, -1.png ... (default outdir: /tmp)
"""
import json, os, sys
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "source")
sys.path.insert(0, SRC)
from paper_paths import PAPER_DIRS  # noqa: E402

PAPERS = PAPER_DIRS

def paper_path(fname):
    for d in PAPERS:
        p = os.path.join(d, fname)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(fname)

pid = sys.argv[1]
outdir = sys.argv[2] if len(sys.argv) > 2 else "/tmp"
m = json.load(open(os.path.join(SRC, "snippets", "manifest.json")))
if pid not in m:
    print(f"no manifest entry for {pid} (observation problem? read the paper PDF directly)")
    sys.exit(1)
for k, (f, pno, y0, y1) in enumerate(m[pid]):
    d = pymupdf.open(paper_path(f))
    page = d[pno]
    pix = page.get_pixmap(dpi=150, clip=pymupdf.Rect(0, y0, page.rect.x1, y1))
    out = os.path.join(outdir, f"{pid}-{k}.png")
    pix.save(out)
    print(out)
