6.17 OK
6.18 OK
6.19 OK
6.20 OK
6.21 OK
6.22 OK
6.23 OK
6.24 OK
6.25 OK
6.26 OK
6.27 OK
6.28 OK
6.29 OK
6.30 OK
6.31 FIXED-PROPOSED: statement 2.2 keeps the official typo "Alfirak" (elsewhere "Alfirk") without a sic marker; add one.
OLD<<<\item[2.2:] Use table 2-2 and figure 2, then Estimate the ``apparent visual
  magnitude'' of stars 2 (Alfirak) and 3 (Alderamin) and complete Table 2-3.
  \textbf{(40 Points)}>>>
NEW<<<\item[2.2:] Use table 2-2 and figure 2, then Estimate the ``apparent visual
  magnitude'' of stars 2 (Alfirak) and 3 (Alderamin) and complete Table 2-3.
  % sic: "Alfirak" as printed in the source; the star is called Alfirk
  % elsewhere in the same problem
  \textbf{(40 Points)}>>>
(Everything else in 6.31 verified OK against 2009_OBS.pdf p.6 and 2009_OBS_sol.pdf pp.87-88: angular distances 11:09:10~11deg / 18:36:50~19deg, magnitudes 3.2 / 2.4, tables and 40+40=80 points all match.)
6.32 FIXED-PROPOSED: statement keeps the official typos "dots where supressed" (for "were suppressed") without a sic marker; add one.
OLD<<<\textbf{Note}: To avoid confusion between decimal dots and real stars, dots
where supressed. So, magnitude 60 corresponds to magnitude 6.0. Give your
answer using one decimal figure and 0.1 precision.>>>
NEW<<<\textbf{Note}: To avoid confusion between decimal dots and real stars, dots
where supressed. % sic: "where supressed" as printed in the source
So, magnitude 60 corresponds to magnitude 6.0. Give your
answer using one decimal figure and 0.1 precision.>>>
(Everything else in 6.32 verified OK against 2012_OBS.pdf p.1/chart p.3 and 2012_OBS_sol.pdf p.1: statement verbatim, solution "7.9 / 7.7-8.1 correct / 7.5-7.7 or 8.1-8.3 70% / (5 minutes)" matches.)

NOTES (out of scope of single problems):
- ch06.tex lines 465-466 (inside 6.28 statement): stale truncated comment claims Figures 2/3 "are not in images/" although images/2013_DA_D3-f1.pdf and -f2.pdf exist and are \ioaafig'ed. Suggest deleting the stale comment.
- ch06.tex lines 763-764: the "Solutions to Chapter 6" section opens with a quote saying "Solutions are not transcribed in this edition", yet full solutions 6.1-6.32 follow. Boilerplate appears stale/contradictory; flagging for the editor.
- Decimal commas: 2014 Romanian-sourced solutions (6.17, 6.29) consistently use 0{,}4-style decimal commas (79 occurrences across chapters, and 6.29 carries an explicit "Decimal commas kept as printed" header comment), so I treated this as deliberate retention, not a policy violation.
