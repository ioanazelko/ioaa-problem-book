#!/usr/bin/env python
"""Extract each problem's figures from the official papers as cropped PDFs.

Figures are taken mechanically from the source PDFs, so they stay vector where
the original was vector. Each problem's region (from snippets/manifest.json) is
scanned for images and large vector drawings; each contiguous graphic block is
written to images/<problem-id>-fN.pdf and can be included with \\includegraphics.

Usage:
    python extract_images.py            # all problems
    python extract_images.py 2016_TH_T3 # one problem
"""
import json
import os
import sys

import pymupdf

from pdf_sanitize import assert_no_delegation_watermark, open_source_pdf

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "source")
sys.path.insert(0, SRC)
from paper_paths import PAPER_DIRS  # noqa: E402

PAPERS = PAPER_DIRS
OUT = os.path.join(HERE, "images")

# a graphic must be at least this big (points) to be worth extracting;
# smaller marks are almost always rules, bullets or inline math glyphs
MIN_W, MIN_H = 60, 40
# ...and this big in area, which rejects page-banner logos that clear MIN_W/MIN_H
MIN_AREA = 12000
# papers put their logo in a running header/footer; ignore those bands entirely
HEADER_H, FOOTER_H = 90, 55


def worth_keeping(r, page):
    if r.width < MIN_W or r.height < MIN_H:
        return False
    if r.width * r.height < MIN_AREA:
        return False
    if r.y1 < page.rect.y0 + HEADER_H or r.y0 > page.rect.y1 - FOOTER_H:
        return False
    # Letterhead banners: very wide, very short, and pinned to the page edges.
    # Real figures are rarely this letterbox-shaped.
    if r.width > page.rect.width * 0.70 and r.height < 110:
        return False
    return True


def paper_path(fname):
    for d in PAPERS:
        p = os.path.join(d, fname)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(fname)


_docs = {}


def doc(fname):
    if fname not in _docs:
        # The official 2021/2023 files contain a separate delegation-print
        # overlay.  Remove it from the in-memory source before any crop is made.
        _docs[fname] = open_source_pdf(paper_path(fname))
    return _docs[fname]


def text_bands(page, y0, y1):
    """Vertical bands occupied by ordinary paragraph text in the region.

    Used to stop a figure's bounding box from swallowing the prose above or
    below it: a wide, short block of text is body copy, not part of the figure.
    """
    bands = []
    clip = pymupdf.Rect(page.rect.x0, y0, page.rect.x1, y1)
    for blk in page.get_text("dict", clip=clip)["blocks"]:
        if blk.get("type") != 0:
            continue
        r = pymupdf.Rect(blk["bbox"])
        if r.width > page.rect.width * 0.55 and r.height < 90:
            bands.append((r.y0, r.y1))
    return bands


def clipped_by_text(r, bands):
    """True if this box mostly overlaps body text (so it is not a figure)."""
    covered = 0.0
    for a, b in bands:
        lo, hi = max(r.y0, a), min(r.y1, b)
        if hi > lo:
            covered += hi - lo
    return r.height > 0 and covered / r.height > 0.55


def graphic_boxes(page, y0, y1):
    """Rectangles of picture-like content inside the y-band, merged when they overlap."""
    bands = text_bands(page, y0, y1)
    boxes = []
    for d in page.get_image_info():
        r = pymupdf.Rect(d["bbox"])
        if r.y1 >= y0 and r.y0 <= y1 and worth_keeping(r, page):
            boxes.append(r)
    # vector drawings: cluster them, a diagram is many small strokes
    vec = [d["rect"] for d in page.get_drawings()
           if d["rect"].y1 >= y0 and d["rect"].y0 <= y1
           and not clipped_by_text(d["rect"], bands)]
    if vec:
        cluster = None
        for r in sorted(vec, key=lambda r: r.y0):
            if cluster is None:
                cluster = +r
            elif r.y0 <= cluster.y1 + 12:
                cluster |= r
            else:
                if worth_keeping(cluster, page):
                    boxes.append(cluster)
                cluster = +r
        if cluster is not None and worth_keeping(cluster, page):
            boxes.append(cluster)

    def text_between(a, b):
        """Is a band of body text sandwiched between these two boxes?

        Only the vertical gap that separates them counts. Bands that merely
        overlap one of the boxes are captions or axis labels sitting alongside
        the graphic, not a paragraph dividing two different figures.
        """
        lo, hi = min(a.y1, b.y1), max(a.y0, b.y0)
        if hi <= lo:
            return False  # boxes overlap vertically: nothing sits between them
        return any(t0 < hi - 2 and t1 > lo + 2 for t0, t1 in bands)

    # merge overlapping boxes so one figure is one file, but never merge across
    # a paragraph of text - that means they are two separate figures
    merged = []
    for r in sorted(boxes, key=lambda r: (r.y0, r.x0)):
        placed = False
        for i, m in enumerate(merged):
            if (m.intersects(r) or abs(m.y1 - r.y0) < 10) and not text_between(m, r):
                merged[i] = m | r
                placed = True
                break
        if not placed:
            merged.append(+r)
    out = []
    for r in merged:
        if not worth_keeping(r, page) or clipped_by_text(r, bands):
            continue
        # A real figure holds labels, not paragraphs. If a box contains whole
        # bands of body text, the vector clustering has run past the graphic and
        # swallowed the prose around it - shrink it to the part that is picture.
        inner = [b for b in bands if b[0] >= r.y0 - 2 and b[1] <= r.y1 + 2]
        if inner:
            r = shrink_past_text(r, inner, page)
            if r is None or not worth_keeping(r, page):
                continue
        out.append(r)
    return out


def shrink_past_text(r, inner_bands, page):
    """Trim a box down to the largest slice of it that holds no body text."""
    cuts = [r.y0] + [y for b in inner_bands for y in b] + [r.y1]
    cuts = sorted(set(cuts))
    best = None
    for a, b in zip(cuts, cuts[1:]):
        if any(t0 < b - 2 and t1 > a + 2 for t0, t1 in inner_bands):
            continue  # this slice is text
        if best is None or (b - a) > (best[1] - best[0]):
            best = (a, b)
    if best is None or best[1] - best[0] < MIN_H:
        return None
    return pymupdf.Rect(r.x0, best[0], r.x1, best[1])


def is_blank(clip, page):
    """True if the region carries no real ink."""
    try:
        pix = page.get_pixmap(clip=clip, dpi=36, colorspace=pymupdf.csGRAY)
    except Exception:
        return False
    data = pix.samples
    if not data:
        return True
    dark = sum(1 for b in data if b < 200)
    return dark / len(data) < 0.012


def extract(pid, segments):
    made = []
    for fname, pno, y0, y1 in segments:
        page = doc(fname)[pno]
        for r in graphic_boxes(page, y0, y1):
            r = r & page.rect
            if r.is_empty or is_blank(r, page):
                continue
            n = len(made) + 1
            out = os.path.join(OUT, f"{pid}-f{n}.pdf")
            new = pymupdf.open()
            # keep it vector: copy the clipped region onto a same-size page
            pg = new.new_page(width=r.width, height=r.height)
            pg.show_pdf_page(pymupdf.Rect(0, 0, r.width, r.height),
                             doc(fname), pno, clip=r)
            assert_no_delegation_watermark(new, out)
            new.save(out, garbage=4, deflate=True)
            new.close()
            made.append(os.path.basename(out))
    return made


def main():
    manifest = json.load(open(os.path.join(SRC, "snippets", "manifest.json")))
    os.makedirs(OUT, exist_ok=True)
    want = sys.argv[1:] or [k for k in manifest if "SOL" not in k]
    index = {}
    for pid in sorted(want):
        if pid not in manifest:
            print("no such problem:", pid)
            continue
        try:
            figs = extract(pid, manifest[pid])
        except Exception as e:
            print(f"{pid}: FAILED {e}")
            continue
        if figs:
            index[pid] = figs
            print(f"{pid}: {len(figs)} figure(s)")
    with open(os.path.join(OUT, "index.json"), "w") as fh:
        json.dump(index, fh, indent=1, sort_keys=True)
    print(f"\n{len(index)} problems have figures; index written to images/index.json")


if __name__ == "__main__":
    main()
