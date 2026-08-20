#!/usr/bin/env python
"""Assemble the IOAA problems-by-topic book from manifest + classification."""
import json, os, re, sys
import pymupdf

from paper_paths import paper_path

SCRATCH = "."
MANIFEST = json.load(open("snippets/manifest.json"))

CHAPTERS = {
    1: "Positional Astronomy & Time",
    2: "Celestial Mechanics & Gravitation",
    3: "Solar System & Planetary Science",
    4: "The Sun & Heliophysics",
    5: "Optics, Telescopes & Detectors",
    6: "Radiation, Magnitudes & Spectra",
    7: "Stellar Astrophysics",
    8: "Binary & Variable Stars",
    9: "Exoplanets",
    10: "Compact Objects & Relativistic Astrophysics",
    11: "Galactic Astrophysics",
    12: "Extragalactic Astrophysics",
    13: "Cosmology",
    14: "Gravitational Waves",
}
HOSTS = {2007:"Chiang Mai, Thailand",2008:"Bandung, Indonesia",2009:"Tehran, Iran",
         2010:"Beijing, China",2011:"Katowice, Poland",2012:"Rio de Janeiro, Brazil",
         2013:"Volos, Greece",2014:"Suceava, Romania",2015:"Magelang, Indonesia",
         2016:"Bhubaneswar, India",2017:"Phuket, Thailand",2018:"Beijing, China",
         2019:"Keszthely, Hungary",2020:"GeCAA (Estonia, remote)",2021:"Bogotá (remote)",
         2022:"Kutaisi, Georgia",2023:"Katowice, Poland",2024:"Rio de Janeiro, Brazil",
         2025:"Mumbai, India"}

def prob_id(year, rnd, label):
    y = int(year)
    if y == 2007:
        return f"2007_{'TH' if rnd=='TH' else 'DA'}_{label}"
    if y == 2019 or y == 2020 or y == 2022:
        return f"{y}_{rnd}_{label}"
    return f"{y}_{rnd}_{label}"

def sol_id(pid):
    return pid.replace("_TH_", "_THSOL_").replace("_DA_", "_DASOL_")

def load_class():
    recs = []
    for f in ["classify_2007_2011.tsv","classify_2012_2016.tsv","classify_2017_2021.tsv","classify_2022_2025.tsv"]:
        for line in open(f):
            line = line.rstrip("\n")
            if not line.strip(): continue
            parts = line.split("\t")
            year, rnd, label, title, pts, ch, tag, sec = parts
            recs.append(dict(year=int(year), rnd=rnd, label=label,
                             title=None if title=="-" else title,
                             pts=None if pts=="-" else pts, ch=int(ch), tag=tag,
                             sec=None if sec=="-" else sec))
    return recs

# label sort key: keeps exam order within a year/round
def label_key(label):
    m = re.findall(r"\d+", label)
    pref = 0
    if label.startswith("L") or "Q2" == label or label.startswith("Long"): pref = 1
    if re.match(r"^Q[234]$", label): pref = 1  # 2007 long problems
    if label.startswith("L"): pref = 1
    return (pref, [int(x) for x in m] if m else [0])

# ---------- geometry helpers ----------
PAGE_W, PAGE_H = 595.0, 842.0
ML, MR, MT, MB = 42.0, 42.0, 50.0, 48.0
CW = PAGE_W - ML - MR

_srcs = {}

def src(fname):
    if fname not in _srcs:
        _srcs[fname] = pymupdf.open(paper_path(fname))
    return _srcs[fname]

_bbox_cache = {}
def seg_bbox(fname, pno, y0, y1):
    """Tight content bbox within the y-clip of a source page."""
    key = (fname, pno, y0, y1)
    if key in _bbox_cache: return _bbox_cache[key]
    page = src(fname)[pno]
    x0, x1 = None, None
    clip = pymupdf.Rect(page.rect.x0, y0, page.rect.x1, y1)
    for blk in page.get_text("dict", clip=clip)["blocks"]:
        bb = pymupdf.Rect(blk["bbox"])
        if bb.height < 1 or bb.width < 1: continue
        x0 = bb.x0 if x0 is None else min(x0, bb.x0)
        x1 = bb.x1 if x1 is None else max(x1, bb.x1)
    try:
        for d in page.get_image_info():
            bb = pymupdf.Rect(d["bbox"])
            if bb.y1 < y0 or bb.y0 > y1: continue
            x0 = bb.x0 if x0 is None else min(x0, bb.x0)
            x1 = bb.x1 if x1 is None else max(x1, bb.x1)
    except Exception:
        pass
    try:
        dr = page.get_drawings()
        for d in dr:
            bb = d["rect"]
            if bb.y1 < y0 or bb.y0 > y1 or bb.width < 2: continue
            x0 = bb.x0 if x0 is None else min(x0, bb.x0)
            x1 = bb.x1 if x1 is None else max(x1, bb.x1)
    except Exception:
        pass
    if x0 is None or x1 - x0 < 100:  # scanned page or sparse: use full width
        x0, x1 = page.rect.x0 + 30, page.rect.x1 - 30
    x0 = max(page.rect.x0, x0 - 4); x1 = min(page.rect.x1, x1 + 4)
    r = (x0, x1)
    _bbox_cache[key] = r
    return r

# ---------- book writer ----------
class Book:
    def __init__(self):
        self.doc = pymupdf.open()
        self.page = None
        self.y = MT
        self.toc = []
        self.pagemarks = {}   # id -> page number (1-based)
        self.link_texts = {}  # id -> text to append in header (pass 2)

    def new_page(self):
        self.page = self.doc.new_page(width=PAGE_W, height=PAGE_H)
        self.y = MT
        n = self.doc.page_count
        self.page.insert_text((PAGE_W/2 - 8, PAGE_H - 24), str(n), fontsize=9, fontname="helv")

    def need(self, h):
        if self.page is None or self.y + h > PAGE_H - MB:
            self.new_page()

    def chapter(self, num, title):
        self.new_page()
        self.toc.append([1, f"{num}. {title}", self.doc.page_count])
        self.page.insert_text((ML, self.y + 24), f"Chapter {num}", fontsize=13, fontname="helv", color=(0.35,0.35,0.35))
        self.page.insert_text((ML, self.y + 52), title, fontsize=22, fontname="hebo")
        self.page.draw_line((ML, self.y + 66), (PAGE_W - MR, self.y + 66), width=1.2)
        self.y += 88

    def section(self, title):
        self.need(46)
        self.toc.append([2, title, self.doc.page_count])
        self.page.insert_text((ML, self.y + 16), title, fontsize=14, fontname="hebo")
        self.page.draw_line((ML, self.y + 22), (ML + 180, self.y + 22), width=0.7)
        self.y += 34

    def _draw_header(self, left, right):
        self.page.insert_text((ML, self.y + 12), left, fontsize=11, fontname="hebo")
        w = pymupdf.get_text_length(right, fontname="helv", fontsize=8.5)
        self.page.insert_text((PAGE_W - MR - w, self.y + 12), right, fontsize=8.5, fontname="helv", color=(0.3,0.3,0.3))
        self.page.draw_line((ML, self.y + 16), (PAGE_W - MR, self.y + 16), width=0.4, color=(0.6,0.6,0.6))
        self.y += 20

    def problem_header(self, mark_id, left, right, segs):
        """Emit the header on the page where the first segment will actually land.

        Keeps header and content together: if the first segment cannot share the
        current page with the header, start a fresh page for both.
        """
        HDR = 20
        first_h = self._fit_height(segs, avail=PAGE_H - MB - (MT + HDR)) if segs else 0
        if self.page is None or self.y + HDR + first_h > PAGE_H - MB:
            self.new_page()
        self._draw_header(left, right)
        self.pagemarks[mark_id] = self.doc.page_count

    def _seg_scale(self, fname, pno, y0, y1, avail):
        """Scale for one segment given the vertical space available on this page."""
        x0, x1 = seg_bbox(fname, pno, y0, y1)
        w, h = x1 - x0, y1 - y0
        s = min(CW / w, 1.15)
        maxh = PAGE_H - MT - MB
        if h * s > maxh:
            s = maxh / h
        # modest shrink to avoid a page break that would strand the header
        if h * s > avail >= maxh * 0.55 and avail / (h * s) >= 0.80:
            s *= avail / (h * s)
        # guard against float dust making a just-fitting block overflow
        if h * s > avail >= h * s - 0.5:
            s = avail / h
        return x0, x1, w, h, s

    def _fit_height(self, segs, avail):
        """Rendered height of the first segment when placed with `avail` space."""
        fname, pno, y0, y1 = segs[0]
        if y1 - y0 < 8:
            return 0
        _, _, _, h, s = self._seg_scale(fname, pno, y0, y1, avail)
        return h * s

    def place_segments(self, segs):
        for fname, pno, y0, y1 in segs:
            if y1 - y0 < 8: continue
            avail = PAGE_H - MB - self.y
            x0, x1, w, h, s = self._seg_scale(fname, pno, y0, y1, avail)
            if self.y + h * s > PAGE_H - MB + 0.5:
                self.new_page()
                avail = PAGE_H - MB - self.y
                x0, x1, w, h, s = self._seg_scale(fname, pno, y0, y1, avail)
            rect = pymupdf.Rect(ML, self.y, ML + w * s, self.y + h * s)
            clip = pymupdf.Rect(x0, y0, x1, y1)
            try:
                self.page.show_pdf_page(rect, src(fname), pno, clip=clip)
            except Exception as e:
                self.page.insert_text((ML, self.y + 10), f"[render error: {fname} p{pno+1}: {e}]",
                                      fontsize=8, color=(0.7,0,0))
                self.y += 16
                continue
            self.y += h * s + 10

    def text_block(self, text, size=10, font="helv", gap=6, color=(0,0,0)):
        lines = text.split("\n")
        lh = size * 1.35
        self.need(lh * len(lines) + gap)
        for ln in lines:
            self.page.insert_text((ML, self.y + size), ln, fontsize=size, fontname=font, color=color)
            self.y += lh
        self.y += gap

def main(out_path):
    recs = load_class()
    # map to manifest ids, validate
    missing = []
    for r in recs:
        pid = prob_id(r["year"], r["rnd"], r["label"])
        sid = sol_id(pid)
        r["pid"], r["sid"] = pid, sid
        if pid not in MANIFEST: missing.append(pid)
        if sid not in MANIFEST: missing.append(sid)
    if missing:
        print("UNMAPPED:", missing)
        sys.exit(1)

    # organize: chapter -> {TH: [recs], DA: [recs]}
    org = {ch: {"TH": [], "DA": []} for ch in CHAPTERS}
    for r in recs:
        org[r["ch"]][r["rnd"]].append(r)
    for ch in org:
        for rnd in ("TH", "DA"):
            org[ch][rnd].sort(key=lambda r: (r["year"], label_key(r["label"])))
    # assign numbers: continuous within chapter
    for ch in org:
        n = 0
        for rnd in ("TH", "DA"):
            for r in org[ch][rnd]:
                n += 1
                r["num"] = f"{ch}.{n}"

    book = Book()
    # pass reference: problem->solution page fills in second run; here single run,
    # we do two full runs: run1 to get pagemarks, run2 to print refs.
    return recs, org, book

def run(org, sol_pages=None, prob_pages=None):
    book = Book()
    # ---- front matter ----
    book.new_page()
    p = book.page
    p.insert_text((ML, 200), "International Olympiad on", fontsize=26, fontname="hebo")
    p.insert_text((ML, 234), "Astronomy & Astrophysics", fontsize=26, fontname="hebo")
    p.insert_text((ML, 274), "Problems by Topic, 2007 - 2025", fontsize=18, fontname="helv")
    p.insert_text((ML, 300), "Theory and Data Analysis rounds, with solutions", fontsize=12, fontname="helv", color=(0.3,0.3,0.3))
    p.insert_text((ML, 330), "Assembled by I. A. Zelko", fontsize=14, fontname="hebo")
    p.draw_line((ML, 348), (PAGE_W-MR, 348), width=1.5)
    intro = [
        "All problems are reproduced from the official IOAA papers (aoXiv archive mirror,",
        "aoxiv.aoguide.app), cropped from the original PDFs so figures, tables and",
        "typesetting are unchanged. Compiled for private tutoring use.",
        "",
        "AI usage: this volume was assembled with the assistance of Claude (Anthropic).",
        "The AI classified each problem by subject, located the crop boundaries in the",
        "source papers, and wrote the Python/PyMuPDF code that lays out the book. The",
        "problems and official solutions themselves are the work of the IOAA organisers",
        "and are reproduced verbatim as images, not regenerated. The topic scheme and",
        "the classification were reviewed by the compiler, but AI-assigned chapters may",
        "still contain errors.",
        "",
        "Organization (in the style of A. Sule's 'Selected Problems in Astronomy &",
        "Astrophysics', with an updated topic list):",
        "  - 14 subject chapters. Within a chapter the theory problems come first, then",
        "    the data-analysis problems as their own section, both in chronological order.",
        "  - Each chapter is followed immediately by its own solutions, in the same",
        "    order and numbering, so a problem and its answer stay in one place.",
        "",
        "Numbering: 'Problem 13.4' is the fourth problem of Chapter 13; the same number",
        "finds its solution at the end of that chapter. The header of each problem names",
        "the year, host, original problem label and point value, and carries a page",
        "reference to its solution (and back).",
        "",
        "Notes:",
        "  - Observation, planetarium and team rounds are not included.",
        "  - For 2010, 2013 and 2020 no separate problem paper survives; statements were",
        "    cropped from the solution files.",
        "  - The 2009, 2011 and 2012 solution files are scans; where two solutions share",
        "    a page, the neighbouring solution is visible in the crop.",
        "  - Official solutions often restate the problem before solving it.",
        "  - 2014 data-analysis: the official solutions file pairs 'Problem 3' A and B;",
        "    the same crop serves problems D2 and D3 of that year.",
    ]
    y = 368
    for ln in intro:
        p.insert_text((ML, y), ln, fontsize=10, fontname="helv")
        y += 13.0

    # ---- chapter overview page ----
    book.new_page()
    book.text_block("Contents", size=18, font="hebo", gap=10)
    for ch, title in CHAPTERS.items():
        nth = len(org[ch]["TH"]); nda = len(org[ch]["DA"])
        line = f"{ch}. {title}   -   {nth} theory, {nda} data analysis"
        book.text_block(line, size=11, gap=1)
    book.text_block("Each chapter is followed by its own solutions.", size=10, gap=0, color=(0.3,0.3,0.3))

    # ---- chapters: problems then that chapter's own solutions ----
    for ch, title in CHAPTERS.items():
        book.chapter(ch, title)
        for rnd, sect in (("TH", "Theory problems"), ("DA", "Data-analysis problems")):
            if not org[ch][rnd]: continue
            book.section(sect)
            for r in org[ch][rnd]:
                right = f"IOAA {r['year']} ({HOSTS[r['year']]}) - {r['rnd']} {r['label']}"
                if r["pts"]: right += f" - {r['pts']} pt"
                if r["sec"]: right += f" - also ch. {r['sec']}"
                left = f"Problem {r['num']}"
                if r["title"]: left += f" - {r['title']}"
                if sol_pages and r["sid"] + "!S" in sol_pages:
                    right += f"  [sol. p. {sol_pages[r['sid'] + '!S']}]"
                book.problem_header(r["pid"] + "!P", left, right, MANIFEST[r["pid"]])
                book.place_segments(MANIFEST[r["pid"]])
                book.toc.append([3, f"{r['num']}  ({r['year']} {r['label']})", book.pagemarks[r["pid"] + "!P"]])

        # solutions to this chapter, starting on a fresh page
        book.new_page()
        book.toc.append([2, f"Solutions to Chapter {ch}", book.doc.page_count])
        book.page.insert_text((ML, book.y + 18), f"Solutions to Chapter {ch}", fontsize=16, fontname="hebo")
        book.page.draw_line((ML, book.y + 26), (PAGE_W - MR, book.y + 26), width=1.0)
        book.y += 44
        for rnd, sect in (("TH", "Theory solutions"), ("DA", "Data-analysis solutions")):
            if not org[ch][rnd]: continue
            book.section(sect)
            for r in org[ch][rnd]:
                right = f"IOAA {r['year']} - {r['rnd']} {r['label']}"
                if prob_pages and r["pid"] + "!P" in prob_pages:
                    right += f"  [problem p. {prob_pages[r['pid'] + '!P']}]"
                left = f"Solution {r['num']}"
                if r["title"]: left += f" - {r['title']}"
                book.problem_header(r["sid"] + "!S", left, right, MANIFEST[r["sid"]])
                book.place_segments(MANIFEST[r["sid"]])

    # ---- year index ----
    book.new_page()
    book.toc.append([1, "Index by year", book.doc.page_count])
    book.text_block("Index by year", size=18, font="hebo", gap=8)
    by_year = {}
    for ch in org:
        for rnd in ("TH","DA"):
            for r in org[ch][rnd]:
                by_year.setdefault(r["year"], []).append(r)
    for yy in sorted(by_year):
        rows = sorted(by_year[yy], key=lambda r: (r["rnd"]=="DA", label_key(r["label"])))
        line = f"IOAA {yy} ({HOSTS[yy]}):"
        book.text_block(line, size=11, font="hebo", gap=2)
        txt = "   ".join(f"{r['rnd']} {r['label']} -> {r['num']}" for r in rows)
        # wrap
        words = txt.split("   ")
        cur = ""
        for wds in words:
            if pymupdf.get_text_length(cur + "   " + wds, fontname="helv", fontsize=9.5) > CW:
                book.text_block(cur, size=9.5, gap=0); cur = wds
            else:
                cur = (cur + "   " + wds).strip()
        if cur: book.text_block(cur, size=9.5, gap=4)
    return book

if __name__ == "__main__":
    recs, org, _ = main("x")
    b1 = run(org)                              # pass 1: learn page numbers
    b2 = run(org, sol_pages=b1.pagemarks, prob_pages=b1.pagemarks)  # pass 2
    b2.doc.set_toc([t for t in b2.toc if t[0] <= 2] and b2.toc)
    out = "IOAA_Problems_by_Topic_2007-2025.pdf"
    b2.doc.save(out, garbage=3, deflate=True)
    print(out, b2.doc.page_count, "pages")
