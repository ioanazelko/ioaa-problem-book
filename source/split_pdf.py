#!/usr/bin/env python
"""Split IOAA paper PDFs into per-problem snippet PDFs.

Config JSON: list of jobs:
{
  "file": "2016_theory.pdf",
  "start_page": 0,
  "problems": [
     {"id": "2016_TH_T1", "rx": "^\\(T1\\)"},          # anchored heading
     {"id": "X", "rx": "...", "stop_rx": "^Solution"},  # crop ends at stop_rx
     {"id": "Y", "rx": "...", "end_rx": "Bulgarian"},   # ditto (alias)
     {"id": "Z", "pages": [4, 6]},                      # 0-based inclusive page range
     {"id": "W", "whole": true}                         # entire document
  ],
  "end_rx": "..."   # optional end marker for the LAST anchored problem
}
Guard: heading lines containing 4+ consecutive dots (TOC leaders) are ignored.
"""
import json, re, sys, os
import pymupdf

from paper_paths import paper_path

PAD_ABOVE = 10
PAD_BELOW = 4
DOTS = re.compile(r"\.{4}")

def all_lines(doc, start_page=0):
    out = []
    for pno in range(start_page, doc.page_count):
        page = doc[pno]
        lines = []
        for blk in page.get_text("dict")["blocks"]:
            if blk.get("type") != 0:
                continue
            for ln in blk["lines"]:
                txt = "".join(s["text"] for s in ln["spans"]).strip()
                if txt:
                    lines.append((ln["bbox"][1], txt))
        lines.sort(key=lambda t: t[0])
        out.extend((pno, y, t) for y, t in lines)
    return out

def find_seq(lines, rx, cursor):
    r = re.compile(rx)
    for i in range(cursor, len(lines)):
        if r.search(lines[i][2]) and not DOTS.search(lines[i][2]):
            return i
    return None

MANIFEST = {}

def emit(doc, pid, start, stop, outdir, dry):
    spno, sy = start
    if stop is None:
        epno, ey = doc.page_count - 1, None
    else:
        epno, ey = stop
    segs = []
    for pno in range(spno, epno + 1):
        r = doc[pno].rect
        top = max(r.y0, sy - PAD_ABOVE) if pno == spno else r.y0
        bot = min(r.y1, ey - PAD_BELOW) if (pno == epno and ey is not None) else r.y1
        if bot - top >= 20:
            segs.append([os.path.basename(doc.name), pno,
                         round(top, 1), round(bot, 1)])
    if not segs:
        segs = [[doc.name, spno, doc[spno].rect.y0, doc[spno].rect.y1]]
    MANIFEST[pid] = segs
    if dry:
        return f"{pid}: p{spno+1}@{sy:.0f} -> p{epno+1}@{'end' if ey is None else f'{ey:.0f}'}"
    out = pymupdf.open()
    for pno in range(spno, epno + 1):
        src = doc[pno]
        r = src.rect
        top = max(r.y0, sy - PAD_ABOVE) if pno == spno else r.y0
        if pno == epno and ey is not None:
            bot = min(r.y1, ey - PAD_BELOW)
        else:
            bot = r.y1
        if bot - top < 20:
            continue
        out.insert_pdf(doc, from_page=pno, to_page=pno)
        np_ = out[-1]
        try:
            np_.remove_rotation()
        except Exception:
            pass
        try:
            crop = pymupdf.Rect(r.x0, top, r.x1, bot) & np_.mediabox
            if crop.height >= 20:
                np_.set_cropbox(crop)
        except Exception:
            pass  # keep the full page if cropping fails
    if out.page_count == 0:  # degenerate: keep the anchor page uncropped
        out.insert_pdf(doc, from_page=spno, to_page=spno)
    out.save(os.path.join(outdir, pid + ".pdf"), garbage=3, deflate=True)
    out.close()
    return f"{pid}: p{spno+1} -> p{epno+1}"

def process(job, outdir, dry, report):
    doc = pymupdf.open(paper_path(job["file"]))
    lines = all_lines(doc, job.get("start_page", 0))
    probs = job["problems"]
    # locate anchors sequentially (page/whole entries pass through)
    marks = []  # (index_in_probs, kind, data)
    cursor = 0
    for k, p in enumerate(probs):
        if p.get("whole"):
            marks.append((k, "whole", None))
        elif "pages" in p:
            marks.append((k, "pages", tuple(p["pages"])))
        else:
            i = find_seq(lines, p["rx"], cursor)
            if i is None:
                report["missing"].append(f'{job["file"]}: {p["id"]}')
                marks.append((k, "miss", None))
            else:
                marks.append((k, "anchor", i))
                cursor = i + 1
    # next-anchor lookup for span ends
    def next_anchor_after(k):
        for kk in range(k + 1, len(probs)):
            m = marks[kk]
            if m[1] == "anchor":
                i = m[2]
                return (lines[i][0], lines[i][1])
            if m[1] == "pages":
                return (m[2][0], None)  # next problem starts at top of that page
        # job-level end_rx
        if job.get("end_rx"):
            m = marks[k]
            i = m[2] if m[1] == "anchor" else 0
            j = find_seq(lines, job["end_rx"], i + 1)
            if j is not None:
                return (lines[j][0], lines[j][1])
        return None
    for k, kind, data in marks:
        p = probs[k]
        if kind == "miss":
            continue
        if kind == "whole":
            start, stop = (0, 0.0), None
        elif kind == "pages":
            start = (data[0], 0.0)
            stop = (data[1], doc[data[1]].rect.y1 + PAD_BELOW)
        else:
            i = data
            start = (lines[i][0], lines[i][1])
            srx = p.get("stop_rx") or p.get("end_rx")
            stop = None
            if srx:
                j = find_seq(lines, srx, i + 1)
                if j is not None:
                    stop = (lines[j][0], lines[j][1])
            if stop is None:
                stop = next_anchor_after(k)
        report["log"].append(emit(doc, p["id"], start, stop, outdir, dry))
    doc.close()

def main(cfg_path, outdir, dry):
    os.makedirs(outdir, exist_ok=True)
    jobs = json.load(open(cfg_path))
    report = {"log": [], "missing": []}
    for job in jobs:
        process(job, outdir, dry, report)
    json.dump(MANIFEST, open(os.path.join(outdir, "manifest.json"), "w"), indent=0)
    print("\n".join(report["log"]))
    if report["missing"]:
        print("MISSING:")
        print("\n".join(report["missing"]))

if __name__ == "__main__":
    dry = "--dry" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--dry"]
    main(args[0], args[1], dry)
