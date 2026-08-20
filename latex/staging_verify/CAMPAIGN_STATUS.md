# Verification campaign status
Goal: verify every chapter's statements+solutions against the original papers
(digit-by-digit), via agents that log per-problem to chNN_log.md files here.
Fixes are logged as OLD<<<...>>> NEW<<<...>>> blocks and applied centrally.

| Chapter | Status |
|---|---|
| ch01 | DONE: 84/84 verified; 27 fixes applied; 2 flags resolved (1.82 answer-leaking statement figure replaced with question-only crop from the official 2025 SkyMap questions file; 1.28 solution geometry diagram extracted+inserted) |
| ch02 | DONE: 44/44 verified; 8 fixes applied incl. removal of a mis-cropped figure that embedded problem T4 inside 2.43 and a solution-leaking figure in 2.33 |
| ch03 | DONE: 38/38 verified; 9 fixes applied (overbar restoration in 3.23, 2007 point-contradiction sics); decimal-comma policy set: normalize to dots (noted in front matter) |
| ch04 | DONE: 10/10; 4 fixes incl. FULL statement restorations for 4.8 and 4.9 (paraphrased/incomplete statements replaced with faithful transcriptions) |
| ch05 | DONE: 54/54; 10 fixes; 5.11 wrong official solution (Exoplanets-in-place-of-AstroSat, confirmed in BOTH archive copies) replaced with explanatory note; 5.44 statement answer-leak removed |
| ch06 | DONE: 32/32; 13 fixes; stale 'solutions not transcribed' notes purged from ALL 14 chapters; 223 decimal commas normalized book-wide |
| ch07 | DONE: 17/17; 10 fixes incl. full statement restorations for 7.13/7.17 and missing statement graphs extracted (2014 P6 log L-log M, 2025 T11 structure plot) |
| ch08 | DONE: 27/27; 14 fixes; 2020_TH_4-f3 solution-leak figure re-cropped; 5 junk figure refs removed; second half (8.15-8.27) verified perfect incl. all data tables |
| ch09 | DONE: 12/12 verified; 13 fixes applied; 9.10 + 9.11 truncated statements being re-transcribed in full (agent running) |
| ch10 | DONE: 20/20; 1 fix; missing T12.2d scale-factor plot extracted and wired |
| ch11 | IN PROGRESS (wave 5) |
| ch12 | IN PROGRESS (wave 5) |
| ch13 | IN PROGRESS (wave 5: 13.1-13.14 / 13.15-13.27) |
| ch14 | IN PROGRESS (wave 5) |

Resume point: if interrupted, check chNN_log.md files for the last verified
problem number in each slice; relaunch verifiers for unlogged problems only.
