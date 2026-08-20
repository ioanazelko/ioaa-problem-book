#!/usr/bin/env python
"""Generate chapters/chNN.tex scaffolding from the classification TSVs.

Every problem gets a \\probhead with its real provenance, its figures already
wired in, and a TODO marker where the statement text goes. Transcription is then
a matter of replacing the TODO blocks - the structure, numbering, provenance and
figures are all correct from the start.

Re-running this OVERWRITES only chapters that have no transcription in them yet;
a chapter containing typed text is left alone unless --force is given, so work
in progress is never destroyed.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "source")
OUT = os.path.join(HERE, "chapters")

TODO = "% TODO transcribe"

CHAPTERS = {
    1: "Positional Astronomy \\& Time",
    2: "Celestial Mechanics \\& Gravitation",
    3: "Solar System \\& Planetary Science",
    4: "The Sun \\& Heliophysics",
    5: "Optics, Telescopes \\& Detectors",
    6: "Radiation, Magnitudes \\& Spectra",
    7: "Stellar Astrophysics",
    8: "Binary \\& Variable Stars",
    9: "Exoplanets",
    10: "Compact Objects \\& Relativistic Astrophysics",
    11: "Galactic Astrophysics",
    12: "Extragalactic Astrophysics",
    13: "Cosmology",
    14: "Gravitational Waves",
}

HOSTS = {2007: "Chiang Mai, Thailand", 2008: "Bandung, Indonesia", 2009: "Tehran, Iran",
         2010: "Beijing, China", 2011: "Katowice, Poland", 2012: "Rio de Janeiro, Brazil",
         2013: "Volos, Greece", 2014: "Suceava, Romania", 2015: "Magelang, Indonesia",
         2016: "Bhubaneswar, India", 2017: "Phuket, Thailand", 2018: "Beijing, China",
         2019: "Keszthely, Hungary", 2020: "GeCAA (Estonia, remote)", 2021: "Bogot\\'a (remote)",
         2022: "Kutaisi, Georgia", 2023: "Katowice, Poland", 2024: "Rio de Janeiro, Brazil",
         2025: "Mumbai, India"}

# round code -> (section title, sort rank)
SECTIONS = {
    "TH": ("Theory problems", 0),
    "DA": ("Data-analysis problems", 1),
    "OBS-PLAN": ("Observation --- planetarium", 2),
    "OBS-SKY": ("Observation --- written and sky map", 3),
    "OBS-TEL": ("Observation --- telescope", 4),
}

TSVS = ["classify_2007_2011.tsv", "classify_2012_2016.tsv",
        "classify_2017_2021.tsv", "classify_2022_2025.tsv", "classify_obs.tsv"]


def tex_escape(s):
    if not s:
        return ""
    for a, b in [("\\", "\\textbackslash{}"), ("&", "\\&"), ("%", "\\%"),
                 ("$", "\\$"), ("#", "\\#"), ("_", "\\_"), ("{", "\\{"),
                 ("}", "\\}"), ("~", "\\textasciitilde{}"), ("^", "\\textasciicircum{}")]:
        s = s.replace(a, b)
    return s


def load():
    recs = []
    for fn in TSVS:
        path = os.path.join(SRC, fn)
        if not os.path.exists(path):
            print("missing (skipped):", fn)
            continue
        for line in open(path):
            if not line.strip():
                continue
            p = line.rstrip("\n").split("\t")
            if len(p) < 8:
                continue
            year, rnd, label, title, pts, ch, tag, sec = p[:8]
            recs.append(dict(year=int(year), rnd=rnd, label=label,
                             title=None if title == "-" else title,
                             pts=None if pts == "-" else pts,
                             ch=int(ch), tag=tag))
    return recs


def pid_of(r):
    """Manifest / image id for a record (theory and data analysis only)."""
    return f"{r['year']}_{r['rnd']}_{r['label']}"


def main():
    force = "--force" in sys.argv
    os.makedirs(OUT, exist_ok=True)
    figs = {}
    idx = os.path.join(HERE, "images", "index.json")
    if os.path.exists(idx):
        figs = json.load(open(idx))

    recs = load()
    org = {c: {} for c in CHAPTERS}
    for r in recs:
        org[r["ch"]].setdefault(r["rnd"], []).append(r)

    for ch in CHAPTERS:
        # number problems continuously through the chapter, in section order
        n = 0
        ordered = []
        for rnd, (sect, rank) in sorted(SECTIONS.items(), key=lambda kv: kv[1][1]):
            rows = sorted(org[ch].get(rnd, []), key=lambda r: (r["year"], r["label"]))
            if not rows:
                continue
            block = []
            for r in rows:
                n += 1
                r["num"] = f"{ch}.{n}"
                block.append(r)
            ordered.append((sect, block))

        path = os.path.join(OUT, f"ch{ch:02d}.tex")
        if os.path.exists(path) and not force:
            body = open(path).read()
            # A chapter is "untouched scaffolding" only when every problem AND
            # every solution slot is still a TODO. As soon as one statement or
            # solution has been typed, the file is never regenerated.
            slots = body.count("\\probhead") + body.count("\\solhead")
            if body.count(TODO) < slots:
                done = slots - body.count(TODO)
                print(f"ch{ch:02d}: {done}/{slots} transcribed, left alone")
                continue

        L = [f"\\chapter{{{CHAPTERS[ch]}}}", ""]
        for sect, block in ordered:
            L += [f"\\section*{{{sect}}}", ""]
            for r in block:
                title = tex_escape(r["title"]) or ""
                host = HOSTS.get(r["year"], "")
                lab = f"{r['rnd']} {tex_escape(r['label'])}"
                pts = r["pts"] or ""
                L.append(f"\\probhead{{{r['num']}}}{{{title}}}{{{r['year']}}}"
                         f"{{{host}}}{{{lab}}}{{{pts}}}")
                L.append(f"% source id: {pid_of(r)}   tag: {r['tag']}")
                L.append(f"{TODO} statement")
                for f in figs.get(pid_of(r), []):
                    L.append(f"\\ioaafig{{{f}}}")
                L.append("")
        # solutions for this chapter
        L += ["\\clearpage", f"\\section*{{Solutions to Chapter {ch}}}", ""]
        for sect, block in ordered:
            for r in block:
                title = tex_escape(r["title"]) or ""
                L.append(f"\\solhead{{{r['num']}}}{{{title}}}")
                L.append(f"{TODO} solution")
                L.append("")

        open(path, "w").write("\n".join(L) + "\n")
        print(f"ch{ch:02d}: {n} problems -> {os.path.basename(path)}")


if __name__ == "__main__":
    main()
