#!/usr/bin/env python
"""Apply OLD<<<>>> NEW<<<>>> fix blocks from staging_verify logs to a chapter."""
import re, sys
log_files, chapter = sys.argv[1:-1], sys.argv[-1]
b = open(chapter).read()
applied, failed = 0, []
for lf in log_files:
    txt = open(lf).read()
    for m in re.finditer(r"OLD<<<(.*?)>>>\s*NEW<<<(.*?)>>>", txt, re.S):
        old, new = m.group(1), m.group(2)
        n = b.count(old)
        if n == 1:
            b = b.replace(old, new); applied += 1
        else:
            failed.append((lf, old[:60].replace("\n", "\\n"), n))
open(chapter, "w").write(b)
print(f"applied {applied} fixes to {chapter}")
for lf, o, n in failed: print(f"  NO MATCH ({n}x): [{lf}] {o}")
