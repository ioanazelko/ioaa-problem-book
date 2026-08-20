#!/usr/bin/env python
"""Merge transcription fragments from staging/<source_id>.tex into chapters/chNN.tex.

A fragment replaces the '% TODO transcribe statement' line of its problem block.
If the fragment itself contains \\ioaafig lines, the scaffold's auto-placed
\\ioaafig lines for that block are dropped (the fragment repositioned them).
Chapters are only modified where a fragment exists; nothing else is touched.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MODE_SOL = "--solutions" in sys.argv
STAGING = os.path.join(HERE, "staging_sol" if MODE_SOL else "staging")
MARKER = "% TODO transcribe solution" if MODE_SOL else "% TODO transcribe statement"
CHAPTERS = os.path.join(HERE, "chapters")

def merge_chapter(path, frags):
    lines = open(path).read().split("\n")
    out, i, used = [], 0, []
    while i < len(lines):
        ln = lines[i]
        m = re.match(r"% source id: (\S+)", ln)
        if not m or m.group(1) not in frags:
            out.append(ln); i += 1; continue
        pid = m.group(1)
        out.append(ln); i += 1
        # collect block until next \probhead / \chapter / \section / EOF
        block = []
        while i < len(lines) and not re.match(r"\\probhead|\\solhead|\\chapter|\\section", lines[i]):
            block.append(lines[i]); i += 1
        if not any(MARKER in b for b in block):
            out.extend(block); continue  # already transcribed; leave alone
        frag = open(frags[pid]).read().rstrip("\n")
        drop_figs = "\\ioaafig" in frag
        newblock = []
        for b in block:
            if MARKER in b:
                newblock.append(frag)
            elif drop_figs and b.strip().startswith("\\ioaafig"):
                continue
            else:
                newblock.append(b)
        out.extend(newblock)
        used.append(pid)
    if used:
        open(path, "w").write("\n".join(out))
    return used

def main():
    frags = {}
    for f in os.listdir(STAGING):
        if f.endswith(".tex"):
            frags[f[:-4]] = os.path.join(STAGING, f)
    total = []
    for ch in sorted(os.listdir(CHAPTERS)):
        if ch.endswith(".tex"):
            total += merge_chapter(os.path.join(CHAPTERS, ch), frags)
    print(f"merged {len(total)} fragments")
    unused = set(frags) - set(total)
    if unused:
        print("UNUSED (no matching TODO):", sorted(unused))

if __name__ == "__main__":
    main()
