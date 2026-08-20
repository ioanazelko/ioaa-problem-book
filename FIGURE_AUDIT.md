# Figure audit

Audit of `latex/book.pdf`. All 460 pages containing figures were reviewed.

The page column gives `printed page / PDF page`.

## Repair status

Repair pass completed on 2026-08-18. Every actionable item in the audit below
was corrected or materially improved, and the rebuilt 906-page PDF was reviewed
again at the affected pages. The tables retain the original findings as a record
of what was found before the repair pass.

The repairs included:

- replacing wrong full-page/header crops with the intended figures;
- removing non-figure fragments and duplicate official-paper banners;
- restoring clipped axes, labels, captions, annotations, and diagram edges;
- rotating sideways solution pages and plots;
- splitting the seven-panel observing montage, three-histogram stack, five-panel
  radio sequence, and five-model strip into readable panels;
- tightening excessive margins and enlarging dense figures in the LaTeX layout;
- preserving the original scientific content rather than inventing details in
  low-resolution source artwork.

### Verified exceptions and source limitations

- `2012_DA_D1-s1.pdf` and `s2.pdf` are already upright, but remain limited by
  the resolution of the only available official scan. Pages `s3`--`s7` were
  rotated into the correct reading orientation.
- `2020_DA_3-s1.pdf` was verified to be the intended Sun--Galactic-centre--HVS
  geometry diagram, not a screenshot of solution prose, so it was retained.
- The coloured curve/vector in `2021_TH_Q11-f1.pdf` is intentional reference
  information in the official chart, not a handwritten answer mark, so it was
  retained.
- `2014_TH_L1-s11.pdf` and `2014_TH_P6-s1.pdf` were verified as complete; their
  companion figures were the crops that required correction.
- `2021_TH_Q10-s1.pdf`, `2021_DA_DA1-f5.pdf`, and `2025_DA_D01-s3.pdf` remain
  limited by their source artwork. They were cleanly cropped and/or enlarged,
  but not redrawn because doing so would require inferring scientific details.

## Original clear defects (resolved)

| Page | Figure asset | Problem |
|---|---|---|
| 61 / 67 | `2007_TH_1.5-s1.pdf` | Lower orbit line and the bottom of the $2a$ bracket are clipped. Source: `latex/chapters/ch01.tex:2163`. |
| 555 / 561 | `2008_DA_D2-f1.pdf` | Tall table runs below the page; bottom rows are cut off. Source: `latex/chapters/ch08.tex:591`. |
| 597–598 / 603–604 | `2010_DA_D2-s1.pdf`, `s2.pdf` | Headings, margin marks, and the caption/right edge are truncated by the source crops. Source: `latex/chapters/ch08.tex:2581`. |
| 325–330 / 331–336 | `2012_DA_D1-s1.pdf`–`s7.pdf` | Low-resolution scans; several pages are rotated 90 degrees, making the solution awkward to read. Source: `latex/chapters/ch03.tex:3183`. |
| 560 / 566 | `2012_DA_D2-f2.pdf` | The x-axis label “(days)” is clipped at the bottom. Source: `latex/chapters/ch08.tex:756`. |
| 728 / 734 | `2013_DA_D4-f1.pdf` | Bottom axis/right-ascension label is clipped. Source: `latex/chapters/ch11.tex:232`. |
| 512 / 518 | `2013_TH_S3-f1.pdf` | Stray cropped text (“.1”) appears at lower right; the footer/x-axis area needs cleaning. Source: `latex/chapters/ch07.tex:63`. |
| 277 / 283 | `2014_DA_D2-s7.pdf` | Explanatory sentence below the chart is cut off at the bottom/right. Source: `latex/chapters/ch03.tex:1034`. |
| 506 / 512 | `2014_DA_D3-s2.pdf` | Formula above the figure and “Fig.” below it are clipped. Source: `latex/chapters/ch06.tex:2092`. |
| 75–76 / 81–82 | `2014_TH_L1-s10.pdf`, `s11.pdf` | Crop includes partial adjacent material; `s10` visibly has a clipped line below the figure. Source: `latex/chapters/ch01.tex:2748`. |
| 195 / 201 | `2014_TH_L3-s1.pdf` | The “Fig.” label is clipped at the bottom. Source: `latex/chapters/ch02.tex:1987`. |
| 159 / 165 | `2014_TH_P1-f1.pdf`, `2014_TH_P2-f1.pdf` | Both are duplicated official-paper header strips, not the intended figures. The Lagrange-orbit diagram for P1 is missing. Source: `latex/chapters/ch02.tex:310`. |
| 513, 528 / 519, 534 | `2014_TH_P6-f1.pdf`, `s1.pdf` | Source crop is too tight around the boxed axis labels; expand and verify the crop. Source: `latex/chapters/ch07.tex:102`. |
| 564 / 570 | `2015_DA_D1-f4.pdf` | Only an official-paper “Problem 2” header/banner was inserted; it is not a useful figure. Source: `latex/chapters/ch08.tex:821`. |
| 161 / 167 | `2015_TH_L1-f1.pdf` | The right-hand radius label/circle edge touches or extends past the crop. Source: `latex/chapters/ch02.tex:362`. |
| 672 / 678 | `2016_TH_T10-f1.pdf` | Grey circular body is cut off along its bottom edge. Source: `latex/chapters/ch10.tex:118`. |
| 801–803 / 807–809 | `2017_DA_D1-s1.pdf`–`s3.pdf` | Handwritten labels at the top/right lie outside or against the crop and are truncated. Source: `latex/chapters/ch12.tex:2042`. |
| 864–867 / 870–873 | `2017_DA_D2-s2.pdf`, `s3.pdf`, `s5.pdf` | Handwritten axis labels and annotations are clipped, especially the right-side notes in `s3`. Source: `latex/chapters/ch13.tex:3015`. |
| 615, 617–618 / 621, 623–624 | `2019_DA_1-s1.pdf`–`s3.pdf` | All three solution plots are sideways and fill their pages awkwardly; rotate and rescale. Source: `latex/chapters/ch08.tex:3403`. |
| 103 / 109 | `2019_TH_12-s1.pdf` | Caption text at the bottom is clipped by the source crop. Source: `latex/chapters/ch01.tex:3932`. |
| 752 / 758 | `2020_DA_3-s1.pdf` | Screenshot of solution prose embedded as a figure; it should be typeset or removed. Source: `latex/chapters/ch11.tex:1299`. |
| 726 / 732 | `2020_TH_5-f1.pdf` | An entire low-resolution official solution page is inserted instead of a figure. Source: `latex/chapters/ch11.tex:156`. |
| 264 / 270 | `2020_TH_8-f1.pdf` | Jupiter velocity map is sideways; it also needs a tighter crop and better contrast. Source: `latex/chapters/ch03.tex:350`. |
| 164 / 170 | `2021_TH_Q11-f1.pdf` | Reference chart contains a blue handwritten answer mark; replace it with a clean copy. Source: `latex/chapters/ch02.tex:562`. |
| 167 / 173 | `2021_TH_Q14-f1.pdf` | Clipped fragment of the preceding sentence remains at the top. Source: `latex/chapters/ch02.tex:630`. |
| 168 / 174 | `2021_TH_Q3-f1.pdf` | Crop contains a truncated preceding sentence along the top and sides. Source: `latex/chapters/ch02.tex:666`. |
| 549 / 555 | `2021_TH_Q7-f1.pdf` | Truncated sentence appears above the graph. Source: `latex/chapters/ch08.tex:408`. |
| 12 / 18 | `2021_TH_Q8-f1.pdf` | Composite crop includes clipped text and header material; the map/logo should be isolated cleanly. Source: `latex/chapters/ch01.tex:597`. |
| 45 / 51 | `2022_OBS-SKY_O7-s1.pdf` | Four-object Messier figure is clipped along the top and right, cutting off much of the right-hand panels. Source: `latex/chapters/ch01.tex:1800`. |
| 48 / 54 | `2022_OBS-SKY_O9-s1.pdf` | Both star grids are clipped along the right edge. Source: `latex/chapters/ch01.tex:1819`. |
| 883 / 889 | `2023_TH_Q13-f1.pdf` | Not a figure: it consists of two clipped prose fragments. Remove or replace it. Source: `latex/chapters/ch14.tex:116`. |
| 884 / 890 | `2023_TH_Q13-f2.pdf` | Plot includes a truncated preceding label at the top. Source: `latex/chapters/ch14.tex:117`. |
| 731 / 737 | `2024_DA_D2-f1.pdf` | Entire official problem page—header, prose, tables, and footer—is inserted as one figure. Extract or typeset the relevant material. Source: `latex/chapters/ch11.tex:258`. |
| 765 / 771 | `2024_TH_T2-f1.pdf`, `f2.pdf` | `f1` is only a footer strip; `f2` is an unrelated/full page containing T3/T4 text. The cluster-distribution plot promised by the problem is missing. Source: `latex/chapters/ch12.tex:264`. |
| 119 / 125 | `2024_TH_T7-s2.pdf` | Lower part/label of the ecliptic–equator diagram is clipped. Source: `latex/chapters/ch01.tex:4969`. |
| 553 / 559 | `2024_TH_T8-f1.pdf` | Entire official problem page is inserted as a shrunken figure; the actual binary-hardening figure should be extracted. Source: `latex/chapters/ch08.tex:527`. |
| 637, 640 / 643, 646 | `2025_DA_D01-f2.pdf`, `f4.pdf` | Stray black symbols/crop artifacts remain at the right edge. Source: `latex/chapters/ch09.tex:571`. |
| 681 / 687 | `2025_TH_T08-f1.pdf` | Accretion-disk artwork and lower label touch or are clipped by the bottom boundary. Source: `latex/chapters/ch10.tex:526`. |
| 378, 380 / 384, 386 | `2025_TH_T09-f1.pdf`, `f2.pdf` | Telescope/point and dimension labels are crowded against or clipped by the source boundaries. Source: `latex/chapters/ch05.tex:721`. |
| 516–517 / 522–523 | `2025_TH_T11-f1.pdf` | Used twice; both instances include clipped prose above/below the plot. Recrop to the plot itself. Source: `latex/chapters/ch07.tex:236`. |
| 685 / 691 | `2025_TH_T12-f2.pdf` | Preceding prose/figure-introduction line is included and cut off at the top. Source: `latex/chapters/ch10.tex:734`. |

## Original readability issues (resolved or mitigated)

| Page | Figure asset | Recommended improvement |
|---|---|---|
| 196 / 202 | `2014_TH_L3-s3.pdf` | Detailed world map is too small for its labels; enlarge or split it. |
| 84 / 90 | `2014_TH_P13-s1.pdf` | Dense Galactic-coordinate diagram is too small; enlarge. |
| 217 / 223 | `2015_TH_S5-s1.pdf` | Tight/unclean crop with stray material near the upper-right corner. |
| 825 / 831 | `2021_DA_DA1-f5.pdf` | Low-resolution rotation-curve schematic with a tiny embedded caption; redraw or enlarge. |
| 361 / 367 | `2021_OBS-SKY_1-s1.pdf` | Seven software screenshots are combined into one montage; UI details are unreadable. Split into panels. |
| 651 / 657 | `2021_TH_Q10-s1.pdf` | Low-quality hand-drawn diagram with a cropped right arc; redraw. |
| 819–820 / 825–826 | `2021_TH_Q15-f4.pdf`, `f5.pdf` | Diagrams and embedded labels are extremely small; enlarge or redraw. |
| 46 / 52 | `2022_OBS-SKY_O7-s2.pdf` | Excessive blank margin and black rule waste space; crop to the star field. |
| 141 / 147 | `2022_OBS-SKY_O8-s1.pdf` | Full interface screenshot and correction sheet are faint and tiny; split, crop, and increase contrast. |
| 870, 872–879 / 876, 878–885 | `2022_DA_2-s1.pdf`–`s14.pdf` | Solution plots have large margins, embedded captions, and faint/tiny labels. Tight-crop and enlarge each plot. |
| 756 / 762 | `2024_DA_D2-s1.pdf` | Three histograms are stacked into a tall, narrow asset; split them so the axes are legible. |
| 663 / 669 | `2025_DA_D01-s3.pdf` | Low-contrast handwritten graph on orange paper; boost contrast or redraw. |
| 767 / 773 | `2025_TH_T05-f1.pdf` | Five radio panels are stacked vertically, leaving timestamps and scale labels too small. Split or enlarge. |
| 822 / 828 | `2025_TH_T10-f1.pdf` | Five model panels form one wide strip with unreadable legends and axes. Split or enlarge. |
