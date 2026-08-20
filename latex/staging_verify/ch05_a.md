# ch05 verify: 5.1-5.18

5.1 OK
5.2 OK
5.3 OK
5.4 OK
5.5 FIXED-PROPOSED: statement OK; solution silently corrects an official misprint (source prints 0.83 x 10^11, minus sign missing) -- add sic comment.
OLD<<<0.0 &= -2.5\lg(0.83 \times 10^{-11}) + const\\>>>
NEW<<<0.0 &= -2.5\lg(0.83 \times 10^{-11}) + const\\
% sic: the source prints 0.83 x 10^{11} (exponent sign lost in print); the
% value meant is 0.83 x 10^{-11} = 8.3 x 10^{-12}, as const = -27.7 confirms.>>>
5.6 OK (note: source statement misprints "wavelngth"; book normalizes spelling in re-typeset statements, left as is)
5.7 OK
5.8 OK
5.9 OK
5.10 OK
5.11 FLAG: statement (AstroSat, T12.1-T12.6) verified OK against 2016_theory.pdf. BUT the transcribed solution (ch05.tex lines 2176-2408) is the solution to a DIFFERENT problem: it is the "(T12) Exoplanets" wobble/transit solution with parts T12.1-T12.13. Root cause: the source files are inconsistent -- 2016_theory.pdf has T12 = AstroSat (6 pages, 12 problems, no Exoplanets problem), while 2016_theory_sol.pdf has T12 = Exoplanets (solutions T1-T12, NO AstroSat solution anywhere; text search for "AstroSat"/"LAXPC" in the sol PDF finds nothing). So the official AstroSat solution is simply absent from the external source-paper archive, and the crop 2016_THSOL_T12 (and figures 2016_TH_T12-s1/s2/s3.pdf referenced in the solution) belong to the Exoplanets problem. Needs an editorial decision: remove/replace solution 5.11 (e.g. note "official solution not available" or source the IOAA 2016 solutions from elsewhere), and note that the 2016 Exoplanets problem statement is missing from the collection entirely (no chapter uses it). Cannot be fixed by a text edit within my slice.
5.12 OK (note: three grading-only remarks of the official solution -- "Declination = ZA + Latitude also gets full credit", "Use of 4 min per degree is also acceptable", "Missing cos delta gets a penalty of 2.0" -- are not transcribed; consistent with the book's trimming of marking remarks elsewhere; all numbers/marks match)
5.13 FIXED-PROPOSED: statement OK; solution T7.4 denominator printed as 2.06'' in the source but transcribed as 2.0600.
OLD<<<n_{\mathrm{p}} = \frac{20''}{2.0600}\ \mathrm{pixels}>>>
NEW<<<n_{\mathrm{p}} = \frac{20''}{2.06''}\ \mathrm{pixels}>>>
(also note: grader remarks "Exact answer required for credit." / "Acceptable range: 9.5 to 10.5 pixels." not transcribed, consistent with book style)
5.14 OK
5.15 OK (note: official question paper gives part a) [6] but the official solution totals 5 marks for a); each is transcribed faithfully from its own source)
5.16 OK
5.17 OK (pre-existing sic on eq. 14.9 verified accurate)
5.18 FIXED-PROPOSED: statement OK; all formulas/values of the solution match the official solution, BUT the official solution swaps parts b) and c) relative to the question paper (solution b) = eye-detectability answer, solution c) = star-diagonal calculation) and this is transcribed faithfully without a sic note. Add one:
OLD<<<\item[b)] Yes, it is well appreciable by most human eyes. Therefore,>>>
NEW<<<\item[b)] % sic: the official solution swaps parts b) and c) relative to
% the question paper -- this item answers question c) (eye detectability),
% and the next item answers question b) (the star diagonal calculation).
Yes, it is well appreciable by most human eyes. Therefore,>>>

## Summary (5.1-5.18)
- OK: 14 (5.1-5.4, 5.6-5.10, 5.12, 5.14-5.17)
- FIXED-PROPOSED: 3 (5.5 missing sic for source's 0.83x10^11 misprint; 5.13 "2.0600" should be "2.06''"; 5.18 missing sic for official b)/c) swap)
- FLAG: 1 (5.11 -- transcribed solution is the 2016 Exoplanets solution, not AstroSat; official AstroSat solution absent from source papers)
