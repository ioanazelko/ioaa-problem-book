# ch08 slice A (8.1-8.14) verification log

8.1 OK (2007 broken-font paper: w=omega, D-prefix=Delta read as intended; all point values, eq numbers (1)-(8), 2.89e-7 and 6.20e-7 per year, M2->M1 direction all match. Source statement has a small illustrative schematic (M1--CM--M2, separation D) not carried into the book; setup is fully described in the text, consistent with resolved-figure policy.)

8.2 FIXED-PROPOSED: (a) solution carries an extra "(10%)" margin mark on the R_2 equation row; the source has only one (10%) (beside "can be determined from the equation:") and the marks must sum to 100% (10+10+10+20+10+15+15+10) -- transcription currently sums to 110%; (b) statement silently normalizes source grammar ("has an inclination", "in unit of solar radius") without a sic comment (book convention marks these).
OLD<<<  R_2 &= \frac{2\pi a}{4P}(t_e - t_t)
  && \text{(10\%)} \\>>>
NEW<<<  R_2 &= \frac{2\pi a}{4P}(t_e - t_t) \\>>>
OLD<<<of $i = 90^\circ$, determine the radii and the masses of both stars in units
of solar radius and solar mass.>>>
NEW<<<of $i = 90^\circ$, determine the radii and the masses of both stars in units
of solar radius and solar mass.
% sic: the source prints "has an inclination" and "in unit of solar radius";
% grammar normalized in transcription.>>>
(Also: solution prose "Binary Periode"/"1 hour 18 minute" normalized to standard English -- kept, prose-level paraphrase consistent with book style. Figure 2008_TH_L1-f1 matches the ABCD/EFGH light curve. Solution correctly located under the source's scrambled label "10.")

8.3 OK (2009 scan: statement verbatim incl. a=2b prolate wording and rugby-ball hint; solution I_max 2piab (3 pts), I_min pib^2 (3 pts), -2.5 log 4 (2 pts), Delta m = -1.5 (2 pts) all match "Solution 15"; the existing NOTE about the un-printed "figure 1"/"Figure 2" verified accurate -- no figures appear in the source solution pages.)

8.4 OK (2010 scan: statement and solution match digit-for-digit: a = 1/2 x (7+1) x 10 = 40 AU (2), M1+M2 = 40^3/100^2 = 6.4 Msun (4), m1/m2 = a2/a1 (2), m1 = 1.6 / m2 = 4.8 Msun (2); the source's own mass assignment (larger orbit -> smaller mass) transcribed as printed.)

8.5 FIXED-PROPOSED: statement silently corrects the source's "Write YES of bound" to "Write YES if bound"; book convention keeps a sic marker for official typos.
OLD<<<bound system. Assume the stars are on the main sequence. Write YES if bound
or NO if not bound alongside your final calculation.>>>
NEW<<<bound system. Assume the stars are on the main sequence. Write YES if bound
% sic: the source prints "Write YES of bound"
or NO if not bound alongside your final calculation.>>>
(Table data all verified against scan: RA 14h29m44.95s/14h39m39.39s, Dec -62d40'46.14"/-60d50'22.10", 1.2953/1.3475 pc, -3.776/-3.600, 0.95/0.77. Solution marking scheme verified: 1.58e15 m [2], 2.4767deg [2], 1.84deg [2], 3.09deg [3], 2.1e15 m [2], 2.63e15 m [3], 0.18 arcsec/yr [4], around 15 [4], lower limit [2], massive-stars argument [4], conclusion [2] = 30; decimal commas 1,58/2,1/2,63 normalized per policy; source typos "angulare"/"aroud" normalized in already-paraphrased marking prose -- left as is.)

8.6 OK (statement verbatim incl. "local group galaxy ." spacing normalized; figures f1/f2 = source Figure 2 (P-L relation) / Figure 3 (HV 2063 light curve). Solution: all four existing sic comments verified accurate against the source -- "From Figure 2"/"From Figure 1" swaps as printed; official adds +0.25 instead of subtracting; official prints 53000 pc AND 64.5 kpc which are mutually inconsistent, 10^4.78 = 60300 pc. Point values 2/1/1/1/3/2 match.)

8.7 FIXED-PROPOSED: the statement carries three \ioaafig references, but the source statement (2014 short problems, Problem 15) has NO figures at all, and the three PDFs are crops of unrelated content (f1 = Lagrange-point orbit schematic, f2 = log L vs period scatter plot, f3 = objective/plane-mirror optics diagram) evidently mis-assigned from other 2014 problems. Remove all three references.
OLD<<<\ioaafig{2014_TH_P15-f1.pdf}
\ioaafig{2014_TH_P15-f2.pdf}
\ioaafig{2014_TH_P15-f3.pdf}>>>
NEW<<<>>>
(Statement/solution content otherwise verified digit-for-digit: P^2=4pi^2R^3/KM chain, R^2=(KM/4pi^2)^{2/3}P^{4/3}, Pogson step, and the existing sic on the source's 3/2 exponent in the k_1 constant is accurate; decimal commas -2,5/0,4 normalized per policy; source's broken English ("cariable stars, whom luminosities and luminosities varies", "oscilations", "rezults", "Erath", "according the") lightly normalized -- consistent with 2014 handling elsewhere. Source solution header oddly reads "Problem 15. Marking scheme Apparent magnitude of the Moon" -- header omitted in book, no action.)

8.8 FIXED-PROPOSED: (a) statement references \ioaafig{2014_TH_P4-f1.pdf}, but the source statement has no figure and that PDF is a crop of the solutions-file cover/contents page ("Content / Indications / Problem 1. Lagrange Points ...") -- remove; (b) source title is "Mass function of a visual binary stellar system", probhead/solhead truncate it to "Mass function of a visual binary" (cf. 6.16 title-fidelity precedent).
OLD<<<\ioaafig{2014_TH_P4-f1.pdf}>>>
NEW<<<>>>
OLD<<<\probhead{8.8}{Mass function of a visual binary}{2014}{Suceava, Romania}{TH P4}{}>>>
NEW<<<\probhead{8.8}{Mass function of a visual binary stellar system}{2014}{Suceava, Romania}{TH P4}{}>>>
OLD<<<\solhead{8.8}{Mass function of a visual binary}>>>
NEW<<<\solhead{8.8}{Mass function of a visual binary stellar system}>>>
(Statement body verified: formulas, T = 7 days, z = 0.001 (source 0,001), c = 3e8, K = 6.67e-11 all match; "consisted of"->"consisting of" and "K -- the gravitational constant ,"->"K is the gravitational constant" are light grammar normalizations consistent with 2014 handling. The no-published-solution note at \solhead{8.8} verified sensible and accurate: the solutions file reprints the Problem 4 statement without any marking scheme, and its Content index lists "Problem N. Marking scheme" for every problem except Problem 4.)

8.9 FIXED-PROPOSED: second statement figure 2015_TH_L2-f2.pdf is a junk crop of the page-header logo banner (2015 IOAA logos), not problem content; the source statement has a single figure (Figure 2, the X-Y-Z orbit/observer diagram = f1). Remove the f2 reference.
OLD<<<\ioaafig{2015_TH_L2-f1.pdf}
\ioaafig{2015_TH_L2-f2.pdf}>>>
NEW<<<\ioaafig{2015_TH_L2-f1.pdf}>>>
(Statement text and solution verified digit-for-digit: parts a/b/c, K cos(wt+eps), 30 M_S, 1/250 M_S, marking 30/30/40, eq (**), 64/125, sin theta < 0.8 (source 0,8 normalized), 53/127 deg; source's broken "the probability of B is a black hole" kept as printed.)

8.10 FIXED-PROPOSED: statement omits the per-part boxed marks [7]/[3]/[5]/[5] printed in the 2016 paper; other 2016 problems in the book carry these (cf. 2.30's \hfill[2] marks), and 20 total matches the probhead.
OLD<<<\item[(T6.1)] Find the ratio of radii of the star in its most contracted and
  most expanded states ($R_1/R_2$).
\item[(T6.2)] Find the radii of the star (in metres) in its most contracted
  and most expanded states ($R_1$ and $R_2$).
\item[(T6.3)] Calculate the flux of the star, $F_2$, when it is in its most
  expanded state.
\item[(T6.4)] Find the distance to the star, $D_{\mathrm{star}}$, in
  parsecs.>>>
NEW<<<\item[(T6.1)] Find the ratio of radii of the star in its most contracted and
  most expanded states ($R_1/R_2$). \hfill[7]
\item[(T6.2)] Find the radii of the star (in metres) in its most contracted
  and most expanded states ($R_1$ and $R_2$). \hfill[3]
\item[(T6.3)] Calculate the flux of the star, $F_2$, when it is in its most
  expanded state. \hfill[5]
\item[(T6.4)] Find the distance to the star, $D_{\mathrm{star}}$, in
  parsecs. \hfill[5]>>>
(Solution verified digit-for-digit incl. 1.77, 0.890 +-0.010, 5.441e9, R2=4.95e10, R1=4.41e10 +-0.02e10, 4.7863e-13, F2=6.51e-10 +-0.04e-10, 2.898e-3, 5.670e-8, 9.208e18 m = 298+-2 pc, and all 1.0/2.0/0.5/3.0 marks. Official solutions file titles it "Cepheid Pulsation" (singular); book keeps the question paper's "Cepheid Pulsations" -- fine.)

8.11 FIXED-PROPOSED: title is paraphrased -- the 2019 question paper prints "Identification of light curves of types of selected variable stars" (solutions file: "Identification of light curve type of selected variable stars"); the book's "Identification of light curves of selected variable star types" matches neither. Use the question paper's wording per title-fidelity convention.
OLD<<<\probhead{8.11}{Identification of light curves of selected variable star types}{2019}{Keszthely, Hungary}{TH 11}{25}>>>
NEW<<<\probhead{8.11}{Identification of light curves of types of selected variable stars}{2019}{Keszthely, Hungary}{TH 11}{25}>>>
OLD<<<\solhead{8.11}{Identification of light curves of selected variable star types}>>>
NEW<<<\solhead{8.11}{Identification of light curves of types of selected variable stars}>>>
(Everything else verified: statement body, star list, bullet types, (8 p)/(16 p)/(1 p), options A-E; solution matches 8/4/6/5/3/2/1/7, the full period table incl. all +-5% ranges, and (D) ASASSN-18tb. Solution bullet labels "alpha^2 CVn star" / "W Vir type (Population II) Cepheid pulsating variable" shortened forms match the solutions file as transcribed.)

8.12 OK (statement parts a-e with (5/3/3/5/4 p) and options A-D verified; solution equations (8.1)-(8.7), all boxed answers 4, 1^m, 0.33^m, 0.25^m, 0.6^m, 0.15^m and per-line marks match; the existing sic on the (8.2) sign slip verified accurate -- expanding -2.5 log I indeed gives +2.5 log e C_b/(lambda T), absorbed by the absolute value in (8.3).)

8.13 FLAG: figure 2020_TH_4-f3.pdf, placed in the STATEMENT, is a page-wide crop that contains not only light curves C/D/E/F but also the top of the official Solution box -- it visibly leaks the answers to parts (a) and (b) ("(a) As Y is smaller, yet hotter...", the 1.5 +- 0.2 radius-ratio derivation and the L_X/L_Y = 1.67 result) right inside the problem statement. Needs a re-crop to the four light curves only (cf. how the 1.82 answer-leaking figure was replaced in ch01). Additionally 2020_TH_4-f4.pdf merely duplicates curves D and F already shown in f3 -- once f3 is re-cropped cleanly, f4 should be dropped or the set re-cut as A/B/C-F. Text-only edit cannot fix this; image re-extraction required.
(Statement text and solution otherwise verified: (a)/(b)(I)/(II)/(c) wording, all fifteen roman options, marks 1/2/2/15 and 4/4/3/2/2, values 1.25+-0.10, 0.25+-0.05, 5.0+-1.5, 1.5+-0.2, 10/16/6 e-12 W/m^2, 1.67 all match. Source labels the (c) answers "(cxi)/(cxii)/(cix)/(cxv)/(cx)" (part letter c + numeral); book's plain (xi)/(xii)/(ix)/(xv)/(x) is a faithful normalization.)

8.14 FIXED-PROPOSED: all digits verified (6561/6565/6562.8 A, 2.998e5, -82.23, +100.50, 1.026, 1.975, 0.00662", 81.1 ly, 9.46e15, 3.96 d, 7.528e31 kg, 37.868/18.691/19.177 M_sun, 3.088e4/2.823e4 L_sun; mark totals 5+4+2+2 = 13 correct), but in parts 7.1-7.3 each margin mark is placed one step EARLY relative to the source (e.g. the first [2 point] precedes the v_A equation it rewards; in the source every mark sits beside its result line). Three placement fixes:
OLD<<<  both H$\alpha$ lines and later find the velocity of each star by Doppler.
  \hfill[2 point]
  \[ v_A = \frac{6561\,\text{\AA} - 6562.8\,\text{\AA}}{6562.8\,\text{\AA}}
     \times\left(2.998\cdot 10^5\ \mathrm{km\cdot s^{-1}}\right)
     = -82.23\ \mathrm{km\cdot s^{-1}} \]
  \hfill[2 point]
  \[ v_B = \frac{6565\,\text{\AA} - 6562.8\,\text{\AA}}{6562.8\,\text{\AA}}
     \times\left(2.998\cdot 10^5\ \mathrm{km\cdot s^{-1}}\right)
     = +100.50\ \mathrm{km\cdot s^{-1}} \]>>>
NEW<<<  both H$\alpha$ lines and later find the velocity of each star by Doppler.
  \[ v_A = \frac{6561\,\text{\AA} - 6562.8\,\text{\AA}}{6562.8\,\text{\AA}}
     \times\left(2.998\cdot 10^5\ \mathrm{km\cdot s^{-1}}\right)
     = -82.23\ \mathrm{km\cdot s^{-1}} \]
  \hfill[2 point]
  \[ v_B = \frac{6565\,\text{\AA} - 6562.8\,\text{\AA}}{6562.8\,\text{\AA}}
     \times\left(2.998\cdot 10^5\ \mathrm{km\cdot s^{-1}}\right)
     = +100.50\ \mathrm{km\cdot s^{-1}} \]
  \hfill[2 point]>>>
OLD<<<  From the definition of CM: \hfill[0.5 points]
  \[ \frac{\alpha_B}{\alpha_A} = 1.026 \]
  \hfill[0.5 points]
  \[ \alpha = (\alpha_A + \alpha_B)
     = \alpha_B\left(1 + \frac{\alpha_A}{\alpha_B}\right)
     = 1.975\,\alpha_B \]
  Applying the 3rd Kepler's law, the total mass of the system is:
  \hfill[1 point]
  \[ M_{tot} = \frac{4\pi^2}{G}\times\frac{\alpha^3\cdot d^3}{T^2} \]>>>
NEW<<<  From the definition of CM:
  \[ \frac{\alpha_B}{\alpha_A} = 1.026 \]
  \hfill[0.5 points]
  \[ \alpha = (\alpha_A + \alpha_B)
     = \alpha_B\left(1 + \frac{\alpha_A}{\alpha_B}\right)
     = 1.975\,\alpha_B \]
  \hfill[0.5 points]
  Applying the 3rd Kepler's law, the total mass of the system is:
  \[ M_{tot} = \frac{4\pi^2}{G}\times\frac{\alpha^3\cdot d^3}{T^2} \]
  \hfill[1 point]>>>
OLD<<<  \[ M_{tot} = m_A + m_B = 1.026\cdot m_B + m_B = 2.026\,m_B
     = 37.868\,M_\odot \]
  \hfill[1 point]
  \[ m_B = 18.691\,M_\odot \]
  \hfill[1 point]
  \[ m_A = 1.026\cdot m_B = 19.177\,M_\odot \]>>>
NEW<<<  \[ M_{tot} = m_A + m_B = 1.026\cdot m_B + m_B = 2.026\,m_B
     = 37.868\,M_\odot \]
  \[ m_B = 18.691\,M_\odot \]
  \hfill[1 point]
  \[ m_A = 1.026\cdot m_B = 19.177\,M_\odot \]
  \hfill[1 point]>>>
(Also verified: statement 7.1-7.4 texts and 5.0/4.0/2.0/2.0 pt values; figure f1 = the Halpha spectrum; solution figure s1 = the spectrum with the two green measurement lines; source's singular "[2 point]" kept as printed; the 7.2 [2 point] mark now sits with the 7.528e31 kg result as in the source. In 8.14's 7.4 the marks were already correctly placed.)

--- SUMMARY (slice 8.1-8.14) ---
OK: 5 (8.1, 8.3, 8.4, 8.6, 8.12)
FIXED-PROPOSED: 8 (8.2, 8.5, 8.7, 8.8, 8.9, 8.10, 8.11, 8.14)
FLAG: 1 (8.13 -- answer-leaking statement figure, needs image re-crop)
Most serious: (1) 8.13 statement figure f3 leaks the official solution to parts (a)-(b); (2) 8.7/8.8/8.9 carry mis-assigned or junk figure crops (three unrelated figures on 8.7, a contents-page crop on 8.8, a logo banner on 8.9) where the sources have no such figures.
