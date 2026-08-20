#!/usr/bin/env python
"""Helper for extracting figures from source papers.

Usage:
  python fig_helper.py grid <pdf> <page_1based> [dpi]
      Renders /tmp/grid_<pdf>_<page>.png with 50pt gridlines and coordinate
      labels so you can read off bounding boxes in POINTS directly.
  python fig_helper.py crop <pdf> <page_1based> <x0> <y0> <x1> <y1> <outname>
      Crops the rect (points, top-left origin) into images/<outname>.pdf
      (vector) and renders /tmp/chk_<outname>.png for verification.
  python fig_helper.py rotate <asset> <angle>
      Rewrites images/<asset> on a tight page, rotated clockwise by 90, 180,
      or 270 degrees, and renders a verification PNG in /tmp.
  python fig_helper.py pad <asset> <points>
      Adds an even white margin around an existing asset.
  python fig_helper.py trim <asset> [margin] [threshold]
      Removes white margins detected from a raster preview while retaining
      the original PDF content. Defaults: 5 pt margin, white threshold 245.
  python fig_helper.py cropasset <asset> <x0> <y0> <x1> <y1> [outname]
      Crops an existing asset in page coordinates. If outname is omitted,
      the source asset is replaced.
  python fig_helper.py audit
      Verifies that no PDF in images/ contains an active delegation watermark.

<pdf> is resolved against the external IOAA Source Papers archive.
"""
import os, sys
import pymupdf

from pdf_sanitize import assert_no_delegation_watermark, open_source_pdf

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(HERE, "..", "source")
sys.path.insert(0, SOURCE_DIR)
from paper_paths import PAPER_DIRS  # noqa: E402

DIRS = PAPER_DIRS

def paper(f):
    for d in DIRS:
        p = os.path.join(d, f)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f)

def grid(pdf, page, dpi=60):
    d = open_source_pdf(paper(pdf))
    pg = d[page - 1]
    pix = pg.get_pixmap(dpi=dpi)
    from PIL import Image, ImageDraw
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    dr = ImageDraw.Draw(im)
    s = dpi / 72.0
    x = 0
    while x * s < pix.width:
        dr.line([(x*s, 0), (x*s, pix.height)], fill=(255, 120, 120), width=1)
        dr.text((x*s + 2, 2), str(x), fill=(255, 0, 0))
        x += 50
    y = 0
    while y * s < pix.height:
        dr.line([(0, y*s), (pix.width, y*s)], fill=(255, 120, 120), width=1)
        dr.text((2, y*s + 2), str(y), fill=(255, 0, 0))
        y += 50
    out = f"/tmp/grid_{os.path.basename(pdf)}_{page}.png"
    im.save(out)
    print(out, f"(page is {pg.rect.width:.0f} x {pg.rect.height:.0f} pt)")

def crop(pdf, page, x0, y0, x1, y1, outname):
    d = open_source_pdf(paper(pdf))
    src = d[page - 1]
    r = pymupdf.Rect(x0, y0, x1, y1) & src.rect
    o = pymupdf.open()
    pg = o.new_page(width=r.width, height=r.height)
    pg.show_pdf_page(pg.rect, d, page - 1, clip=r)
    out = os.path.join(HERE, "images", outname if outname.endswith(".pdf") else outname + ".pdf")
    assert_no_delegation_watermark(o, out)
    o.save(out, garbage=3, deflate=True)
    o.close()
    v = pymupdf.open(out)
    assert_no_delegation_watermark(v, out)
    v[0].get_pixmap(dpi=60).save(f"/tmp/chk_{os.path.basename(out).replace('.pdf', '.png')}")
    v.close()
    print(out, "and /tmp/chk_...png written")

def rotate(asset, angle):
    if angle not in (90, 180, 270):
        raise ValueError("angle must be 90, 180, or 270 degrees")
    path = os.path.join(HERE, "images", asset)
    d = pymupdf.open(path)
    assert_no_delegation_watermark(d, path)
    src = d[0]
    if angle in (90, 270):
        width, height = src.rect.height, src.rect.width
    else:
        width, height = src.rect.width, src.rect.height
    o = pymupdf.open()
    pg = o.new_page(width=width, height=height)
    pg.show_pdf_page(pg.rect, d, 0, rotate=angle)
    tmp = path + ".tmp.pdf"
    o.save(tmp, garbage=4, deflate=True)
    o.close()
    d.close()
    os.replace(tmp, path)
    v = pymupdf.open(path)
    assert_no_delegation_watermark(v, path)
    stem = os.path.basename(path).removesuffix(".pdf")
    v[0].get_pixmap(dpi=60).save(f"/tmp/chk_{stem}.png")
    v.close()
    print(path, "rotated and /tmp/chk_...png written")

def pad(asset, margin):
    if margin <= 0:
        raise ValueError("margin must be positive")
    path = os.path.join(HERE, "images", asset)
    d = pymupdf.open(path)
    assert_no_delegation_watermark(d, path)
    src = d[0]
    o = pymupdf.open()
    pg = o.new_page(width=src.rect.width + 2 * margin,
                    height=src.rect.height + 2 * margin)
    target = pymupdf.Rect(margin, margin,
                          margin + src.rect.width, margin + src.rect.height)
    pg.show_pdf_page(target, d, 0)
    tmp = path + ".tmp.pdf"
    o.save(tmp, garbage=4, deflate=True)
    o.close()
    d.close()
    os.replace(tmp, path)
    v = pymupdf.open(path)
    assert_no_delegation_watermark(v, path)
    stem = os.path.basename(path).removesuffix(".pdf")
    v[0].get_pixmap(dpi=60).save(f"/tmp/chk_{stem}.png")
    v.close()
    print(path, "padded and /tmp/chk_...png written")

def trim(asset, margin=5, threshold=245):
    from PIL import Image
    path = os.path.join(HERE, "images", asset)
    d = pymupdf.open(path)
    assert_no_delegation_watermark(d, path)
    src = d[0]
    pix = src.get_pixmap(dpi=144, colorspace=pymupdf.csGRAY, alpha=False)
    im = Image.frombytes("L", (pix.width, pix.height), pix.samples)
    mask = im.point(lambda value: 255 if value < threshold else 0)
    box = mask.getbbox()
    if box is None:
        raise ValueError(f"no content detected in {asset}")
    sx = src.rect.width / pix.width
    sy = src.rect.height / pix.height
    r = pymupdf.Rect(box[0] * sx - margin, box[1] * sy - margin,
                     box[2] * sx + margin, box[3] * sy + margin) & src.rect
    o = pymupdf.open()
    pg = o.new_page(width=r.width, height=r.height)
    pg.show_pdf_page(pg.rect, d, 0, clip=r)
    tmp = path + ".tmp.pdf"
    o.save(tmp, garbage=4, deflate=True)
    o.close()
    d.close()
    os.replace(tmp, path)
    v = pymupdf.open(path)
    assert_no_delegation_watermark(v, path)
    stem = os.path.basename(path).removesuffix(".pdf")
    v[0].get_pixmap(dpi=60).save(f"/tmp/chk_{stem}.png")
    v.close()
    print(path, "trimmed to", r, "and /tmp/chk_...png written")

def cropasset(asset, x0, y0, x1, y1, outname=None):
    source_path = os.path.join(HERE, "images", asset)
    output_name = outname or asset
    output_path = os.path.join(HERE, "images", output_name)
    d = pymupdf.open(source_path)
    assert_no_delegation_watermark(d, source_path)
    src = d[0]
    r = pymupdf.Rect(x0, y0, x1, y1) & src.rect
    if r.is_empty:
        raise ValueError("crop rectangle does not intersect the asset")
    o = pymupdf.open()
    pg = o.new_page(width=r.width, height=r.height)
    pg.show_pdf_page(pg.rect, d, 0, clip=r)
    tmp = output_path + ".tmp.pdf"
    o.save(tmp, garbage=4, deflate=True)
    o.close()
    d.close()
    os.replace(tmp, output_path)
    v = pymupdf.open(output_path)
    assert_no_delegation_watermark(v, output_path)
    stem = os.path.basename(output_path).removesuffix(".pdf")
    v[0].get_pixmap(dpi=60).save(f"/tmp/chk_{stem}.png")
    v.close()
    print(output_path, "cropped and /tmp/chk_...png written")

def audit():
    image_dir = os.path.join(HERE, "images")
    paths = [os.path.join(image_dir, name)
             for name in sorted(os.listdir(image_dir))
             if name.lower().endswith(".pdf")]
    for path in paths:
        document = pymupdf.open(path)
        try:
            assert_no_delegation_watermark(document, path)
        finally:
            document.close()
    print(f"Checked {len(paths)} figure PDFs: no delegation watermarks found")

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "grid":
        grid(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else 60)
    elif cmd == "crop":
        crop(sys.argv[2], int(sys.argv[3]), *map(float, sys.argv[4:8]), sys.argv[8])
    elif cmd == "rotate":
        rotate(sys.argv[2], int(sys.argv[3]))
    elif cmd == "pad":
        pad(sys.argv[2], float(sys.argv[3]))
    elif cmd == "trim":
        trim(sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 5,
             int(sys.argv[4]) if len(sys.argv) > 4 else 245)
    elif cmd == "cropasset":
        cropasset(sys.argv[2], *map(float, sys.argv[3:7]),
                  sys.argv[7] if len(sys.argv) > 7 else None)
    elif cmd == "audit":
        audit()
