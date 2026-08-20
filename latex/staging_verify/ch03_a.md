# ch03 verification, problems 3.1-3.19 (statements + solutions)

3.1 OK
3.2 OK
3.3 OK
3.4 OK
3.5 OK
3.6 OK
3.7 OK
3.8 OK
3.9 OK
3.10 OK
3.11 FIXED-PROPOSED: solution matches proceedings digit-for-digit; add sic comment for verbatim source grammar left unmarked (file convention marks these, cf. 3.12):
OLD<<<When $r > R$, if there occurred an center eclipse, it must be total solar
eclipse. Otherwise when $r \le R$, the center eclipse must be annular.>>>
NEW<<<When $r > R$, if there occurred an center eclipse, it must be total solar
eclipse. Otherwise when $r \le R$, the center eclipse must be annular.
% sic: "in a ellipse", "an center eclipse" as in the original.>>>
3.12 OK
3.13 OK
3.14 SKIPPED-BY-POLICY: decimal commas normalized to dots book-wide

3.15 OK
3.16 FLAG: all digits/exponents/sic-marks verified correct (incl. the 491520 vs 327680 sic), but the source solution prints decimal commas everywhere (2,5·log; 0,00256; 12,5^m; 0,25^m; -12,25^m; 0,2; 0,2 in 65536/0,2; 10,75^m; -10,5^m) and the transcription silently normalizes them to dots, while the problem statement keeps $0{,}25^m$. Same policy question as 3.14 -- needs a decision (normalize everywhere or preserve; if preserved, ~9 substitutions in the 3.16 solution).
3.17 FLAG: statement and solution verified digit-for-digit (both sic comments accurate: 0.995 vs 0.945, and 86701.8 vs 86715.6). One residue of the same decimal-comma policy question: source prints v_J = 16742,9 m/s (comma) while the other two speeds use dots; transcription silently normalized to 16742.9. Resolve together with 3.14/3.16 policy.
3.18 OK
3.19 OK (grader-only marking notes in the source box — 50% deduction rule, half-mark note, 13.0–13.4 acceptance band — are omitted, consistent with book style elsewhere)
