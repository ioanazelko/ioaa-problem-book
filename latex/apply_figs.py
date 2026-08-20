#!/usr/bin/env python
"""Apply figure-extraction mappings produced by agents.

Mapping files: staging_fig/*.tsv, tab-separated, one row per FIGURE NEEDED
block IN FILE ORDER:
  chNN <TAB> <first-45-chars-of-marker-line-after-normalization> <TAB> <action>
action = one or more image names separated by ';' (e.g. "2014_TH_P9-s1.pdf")
         OR "NOTE:<text>" to insert a visible italic note
         OR "SKIP" to leave the comment untouched.

Normalization: strip leading spaces/%, collapse whitespace.
The applier walks each chapter; at each FIGURE NEEDED block it takes the next
unconsumed mapping for that chapter whose prefix matches; replaces the block
(marker line + following continuation comment lines that are not sic/source-id
markers) with \\ioaafig lines or the note.
"""
import os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))

def norm(s):
    return re.sub(r"\s+", " ", s.strip().lstrip("%").strip())[:45]

def load_maps():
    maps = {}
    for f in sorted(glob.glob(os.path.join(HERE, "staging_fig", "*.tsv"))):
        for ln in open(f):
            ln = ln.rstrip("\n")
            if not ln.strip() or ln.startswith("#"):
                continue
            parts = ln.split("\t")
            if len(parts) != 3:
                print(f"BAD ROW in {f}: {ln!r}"); continue
            ch, prefix, action = parts
            maps.setdefault(ch.strip(), []).append([norm(prefix), action.strip(), False, f])
    return maps

def apply_chapter(path, rows):
    lines = open(path).read().split("\n")
    out, i, used, unmatched = [], 0, 0, []
    while i < len(lines):
        ln = lines[i]
        if "FIGURE NEEDED" not in ln:
            out.append(ln); i += 1; continue
        block_first = norm(ln)
        # consume continuation comment lines
        j = i + 1
        while j < len(lines):
            nx = lines[j].strip()
            if nx.startswith("%") and "sic" not in nx and "source id" not in nx \
               and "FIGURE NEEDED" not in nx and "TABLE" not in nx:
                j += 1
            else:
                break
        # find next unconsumed mapping with matching prefix
        row = None
        for r in rows:
            if not r[2] and r[0] == block_first:
                row = r; break
        if row is None:
            # try startswith both ways (agents may have truncated differently)
            for r in rows:
                if not r[2] and (r[0].startswith(block_first[:30]) or block_first.startswith(r[0][:30])):
                    row = r; break
        if row is None:
            unmatched.append(block_first)
            out.append(ln); i += 1; continue
        row[2] = True; used += 1
        action = row[1]
        indent = re.match(r"\s*", ln).group(0)
        if action == "SKIP":
            out.extend(lines[i:j])
        elif action.startswith("NOTE:"):
            out.append(f"{indent}\\textit{{[{action[5:].strip()}]}}")
        else:
            for img in action.split(";"):
                img = img.strip()
                if img:
                    out.append(f"{indent}\\ioaafig{{{img}}}")
        i = j
    open(path, "w").write("\n".join(out))
    return used, unmatched, [r for r in rows if not r[2]]

def main():
    maps = load_maps()
    total, all_unmatched, all_unused = 0, [], []
    for ch, rows in sorted(maps.items()):
        path = os.path.join(HERE, "chapters", f"{ch}.tex")
        if not os.path.exists(path):
            print("no chapter file:", ch); continue
        used, unmatched, unused = apply_chapter(path, rows)
        total += used
        all_unmatched += [(ch, u) for u in unmatched]
        all_unused += [(ch, r[0], r[3]) for r in unused]
        print(f"{ch}: {used} applied")
    print(f"TOTAL applied: {total}")
    if all_unmatched:
        print("UNMATCHED BLOCKS (no mapping):")
        for ch, u in all_unmatched[:20]: print(" ", ch, u)
    if all_unused:
        print("UNUSED MAPPINGS:")
        for ch, p, f in all_unused[:20]: print(" ", ch, p, os.path.basename(f))

if __name__ == "__main__":
    main()
