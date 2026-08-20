#!/usr/bin/env python
"""Dump the source text of problems so they can be transcribed into LaTeX.

Usage:
    python dump_source.py 2016_TH_T11          # one problem
    python dump_source.py --chapter 4          # every problem in a chapter
    python dump_source.py --chapter 4 --todo   # only ones still untranscribed
"""
import json
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "source")
sys.path.insert(0, SRC)
from paper_paths import PAPER_DIRS  # noqa: E402

PAPERS = PAPER_DIRS

TSVS = ["classify_2007_2011.tsv", "classify_2012_2016.tsv",
        "classify_2017_2021.tsv", "classify_2022_2025.tsv"]


def paper_path(fname):
    for d in PAPERS:
        p = os.path.join(d, fname)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(fname)


_docs = {}


def doc(f):
    if f not in _docs:
        _docs[f] = pymupdf.open(paper_path(f))
    return _docs[f]


def text_of(pid, manifest):
    out = []
    for f, pno, y0, y1 in manifest[pid]:
        page = doc(f)[pno]
        out.append(page.get_text(clip=pymupdf.Rect(0, y0, page.rect.x1, y1)))
    return "\n".join(out)


def chapter_of(pid, recs):
    for r in recs:
        if r["pid"] == pid:
            return r["ch"]
    return None


def load_recs():
    recs = []
    for fn in TSVS:
        p = os.path.join(SRC, fn)
        if not os.path.exists(p):
            continue
        for line in open(p):
            if not line.strip():
                continue
            c = line.rstrip("\n").split("\t")
            if len(c) < 8:
                continue
            recs.append(dict(year=int(c[0]), rnd=c[1], label=c[2],
                             title=None if c[3] == "-" else c[3],
                             pts=None if c[4] == "-" else c[4],
                             ch=int(c[5]), tag=c[6],
                             pid=f"{c[0]}_{c[1]}_{c[2]}"))
    return recs


def todo_ids(ch):
    """Problem ids in a chapter whose statement is still a TODO."""
    path = os.path.join(HERE, "chapters", f"ch{ch:02d}.tex")
    if not os.path.exists(path):
        return set()
    body = open(path).read()
    out = set()
    # a source-id comment followed by a TODO statement marker
    for m in re.finditer(r'% source id: (\S+)[^\n]*\n% TODO transcribe statement',
                         body):
        out.add(m.group(1))
    return out


def main():
    manifest = json.load(open(os.path.join(SRC, "snippets", "manifest.json")))
    recs = load_recs()
    args = sys.argv[1:]

    if "--chapter" in args:
        i = args.index("--chapter")
        ch = int(args[i + 1])
        want = [r["pid"] for r in sorted(recs, key=lambda r: (r["rnd"] != "TH",
                                                             r["year"], r["label"]))
                if r["ch"] == ch]
        if "--todo" in args:
            t = todo_ids(ch)
            want = [p for p in want if p in t]
    else:
        want = [a for a in args if not a.startswith("--")]

    for pid in want:
        if pid not in manifest:
            print(f"\n### {pid}\n[NO MANIFEST ENTRY]")
            continue
        r = next((x for x in recs if x["pid"] == pid), None)
        head = f"{pid}"
        if r:
            head += f"  | ch{r['ch']} | {r['title'] or '-'} | {r['pts'] or '-'}pt | {r['tag']}"
        print(f"\n{'='*78}\n### {head}\n{'='*78}")
        print(text_of(pid, manifest).strip())


if __name__ == "__main__":
    main()
