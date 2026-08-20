#!/usr/bin/env python
"""Harvest % sic comments from the chapters and build the errata appendix."""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER_TITLES = {}

UNI = {"\u00b0": r"$^\circ$", "\u00b1": r"$\pm$", "\u00d7": r"$\times$",
       "\u2013": "--", "\u2014": "---", "\u2018": "`", "\u2019": "'",
       "\u201c": "``", "\u201d": "''", "\u2192": r"$\to$", "\u2248": r"$\approx$",
       "\u2264": r"$\le$", "\u2265": r"$\ge$", "\u0394": r"$\Delta$",
       "\u03c6": r"$\varphi$", "\u03c9": r"$\omega$", "\u03bc": r"$\mu$",
       "\u03b1": r"$\alpha$", "\u03b2": r"$\beta$", "\u03b3": r"$\gamma$",
       "\u03b4": r"$\delta$", "\u03b5": r"$\varepsilon$", "\u03b8": r"$\theta$",
       "\u03bb": r"$\lambda$", "\u03c3": r"$\sigma$", "\u03c4": r"$\tau$",
       "\u03c0": r"$\pi$", "\u03bd": r"$\nu$", "\u03c1": r"$\rho$",
       "\u03b7": r"$\eta$", "\u2299": r"$\odot$", "\u221a": r"$\surd$",
       "\u221e": r"$\infty$", "\u2032": "'", "\u2033": "''", "\u0142": r"\l{}",
       "\u2113": r"$\ell$"}

def esc_text(s):
    out = []
    for ch in s:
        if ch in UNI:
            out.append(UNI[ch]); continue
        if ord(ch) > 127:
            out.append("?"); continue
        out.append({"&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_",
                    "^": r"\^{}", "~": r"\textasciitilde{}",
                    "<": r"$<$", ">": r"$>$"}.get(ch, ch))
    return "".join(out)

def esc_textpart(p):
    # wrap bare LaTeX macros (with optional brace groups) in math mode
    segs = []
    def stash(m):
        segs.append(m.group(0))
        return f"\x00{len(segs)-1}\x00"
    p = re.sub(r"\\[a-zA-Z]+(?:\{(?:[^{}]|\{[^{}]*\})*\})*", stash, p)
    p = esc_text(p)
    for k, s in enumerate(segs):
        p = p.replace(f"\x00{k}\x00", f"${s}$")
    return p

def esc(s):
    # keep $...$ math intact; escape specials elsewhere
    parts = s.split("$")
    if len(parts) % 2 == 0:      # unbalanced $ -> escape everything
        return esc_textpart(s.replace("$", ""))
    return "".join(p if i % 2 else esc_textpart(p) for i, p in enumerate(parts))

def harvest():
    entries = []  # (chapnum, kind, num, year, label, text)
    for f in sorted(os.listdir(os.path.join(HERE, "chapters"))):
        m = re.match(r"ch(\d+)\.tex$", f)
        if not m: continue
        chap = int(m.group(1))
        lines = open(os.path.join(HERE, "chapters", f)).read().split("\n")
        title = ""
        kind, num, year, label = "Problem", "?", "?", ""
        provmap = {}
        i = 0
        while i < len(lines):
            ln = lines[i]
            tm = re.match(r"\\chapter\{(.+)\}", ln)
            if tm: CHAPTER_TITLES[chap] = tm.group(1)
            hm = re.match(r"\\(prob|sol)head\{([\d.]+)\}\{[^}]*\}(?:\{(\d{4})\}\{[^}]*\}\{([^}]*)\})?", ln)
            if hm:
                kind = "Problem" if hm.group(1) == "prob" else "Solution"
                num = hm.group(2)
                if hm.group(3):
                    year, label = hm.group(3), hm.group(4)
                    provmap[num] = (year, label)
                else:
                    year, label = provmap.get(num, ("?", ""))
            sm = re.search(r"%\s*sic\b(.*)$", ln, re.I)
            if sm and "FIGURE" not in ln:
                text = sm.group(1).lstrip(" :—-–,.")
                j = i + 1
                while j < len(lines):
                    nx = lines[j].strip()
                    if nx.startswith("%") and not re.search(r"%\s*(sic\b|FIGURE|source id|TABLE)", nx, re.I):
                        text += " " + nx.lstrip("% ").strip()
                        j += 1
                    else:
                        break
                text = re.sub(r"\s+", " ", text).strip()
                if text:
                    entries.append((chap, kind, num, year, label, text))
                i = j
                continue
            i += 1
    return entries

def main():
    entries = harvest()
    out = [r"\chapter{Errata in the Official Solutions}",
           r"\label{ch:errata}",
           "",
           r"During transcription every solution was checked digit by digit against",
           r"the official papers. The list below collects the places where the",
           r"\emph{official} text itself is wrong or internally inconsistent ---",
           r"sign slips, inverted relations, mismatched values between a derivation",
           r"and its numerical substitution, misprints, and stray editorial leftovers.",
           r"In the body of this book each is transcribed \emph{as printed} and",
           r"marked with a comment in the source; this appendix is the reader-facing",
           r"summary. Trivial spelling slips are included only where they could",
           r"confuse (wrong symbol names, wrong units).",
           ""]
    cur = None
    n = 0
    for chap, kind, num, year, label, text in entries:
        if chap != cur:
            out.append(rf"\section*{{Chapter {chap} --- {CHAPTER_TITLES.get(chap, '')}}}")
            out.append(r"\begin{itemize}" if False else "")
            cur = chap
        head = f"{kind} {num}"
        prov = f"IOAA {year} {label}".strip()
        out.append(rf"\noindent\textbf{{{head}}} ({esc_text(prov)}): {esc(text)}")
        out.append(r"\smallskip")
        out.append("")
        n += 1
    open(os.path.join(HERE, "chapters", "errata.tex"), "w").write("\n".join(out))
    print(f"errata.tex written with {n} entries across {len(set(e[0] for e in entries))} chapters")

if __name__ == "__main__":
    main()
