# IOAA Problems by Topic — LaTeX edition

A transcribed edition of the book: problem statements typed as real LaTeX so
they can be reflowed, restyled and pulled into worksheets. Figures are the
original vector art from the official papers, not redrawn.

This is a **companion to**, not a replacement for, the crop edition
(`../IOAA_Problems_by_Topic_2007-2025.pdf`). Where the two disagree, the crop
edition is authoritative — it is a photograph of the official paper, while a
transcription can be silently wrong.

## Status

**COMPLETE: 402/402 statements and 386/402 solutions transcribed.**

Every problem statement and every published official solution is now typed as
LaTeX, verified digit-by-digit against rendered images of the official papers.
Solutions carry the official reasoning with inline point values; standalone
marking-scheme rubrics are omitted (the crop edition keeps full rubrics).

The 16 solution slots without transcription carry explanatory notes in place:
the 2016 and 2017 observation-round solutions were never published (12), the
2007 pointer-task and 2014 outdoor-telescope keys don't survive (2), one 2012
task has no answer content (1), and the 2014 solutions file simply skips
short problem 4 (1).

All 369 figure references flagged during transcription are now resolved:
~330 diagrams (solution sketches, fitted plots, marked observation charts,
answer keys) were extracted as vector/scan crops into `images/`, and the
handful of items whose source material was never digitised (printed-only exam
charts, plots the organisers never published) carry visible italic notes in
place. The book also ends with an appendix collecting the ~280 errata found
in the official solutions during digit-by-digit verification.

### Why the solutions are not transcribed

The crop edition already reproduces all 326 theory and data-analysis solutions
exactly as the organisers wrote them, under the same problem numbers. Retyping
them would add ~400 long derivations of hand-typed mathematics whose errors are
invisible — a wrong exponent reads as plausible. For the 2009, 2011 and 2012
papers the solutions are scanned images with no extractable text at all, so they
would have to be read off the page by eye.

Until someone types and checks them, the crop edition is the answer key.

## Build

```bash
latexmk -pdf -halt-on-error -file-line-error book.tex
```

This produces `book.pdf`, the only LaTeX-edition PDF. The build automatically
audits every figure and stops if an active delegation watermark is found. Do
not make renamed or manually copied editions; they become stale and are ignored
by Git. `siunitx` and `enumitem` are used when installed and stubbed out when
not, so this builds on a minimal TeX Live.

For an optionally smaller `book.pdf`, use the build wrapper:

```bash
python build_book.py --optimize ebook
```

The optimization profiles are:

| Profile | Treatment | Intended use |
|---|---|---|
| `lossless` | Cleans PDF objects and recompresses streams without resampling images. | Archival copy; modest savings. |
| `print` | Downsamples raster images to 300 dpi. | High-quality printing. |
| `ebook` | Downsamples raster images to 150 dpi. | Recommended distribution copy. |
| `screen` | Downsamples raster images to 72 dpi. | Smallest screen-only copy. |

Running `python build_book.py` without `--optimize` is equivalent to the normal
`latexmk` command. An optimized run first forces a fresh LaTeX build, then
atomically replaces `book.pdf` only after checking that the new PDF has the
same page count and is smaller. The three downsampling profiles require
Ghostscript (`gs`); `lossless` only requires PyMuPDF.

## Files

| File | Role |
|---|---|
| `book.tex` | Master document: preamble, `\probhead`/`\solhead`/`\ioaafig` macros, front matter, `\include`s the chapters. |
| `book.pdf` | The sole generated LaTeX-edition PDF. |
| `.latexmkrc` | Runs the delegation-watermark audit before each build. |
| `build_book.py` | Runs the normal build and, when requested, an optimization profile. |
| `../optimize_pdf.py` | PDF optimizer used by the optional LaTeX build step. |
| `chapters/chNN.tex` | One file per chapter. **This is where transcription happens.** |
| `images/` | 565 cropped vector PDF assets, plus `index.json` mapping problem ids to their figures. |
| `extract_images.py` | Regenerates `images/` from the source papers. |
| `fig_helper.py` | Makes manual figure crops; `python fig_helper.py audit` checks every figure for the delegation watermark. |
| `make_chapters.py` | Regenerates chapter scaffolding from the classification TSVs. |

## Transcribing a problem

1. Find the `% TODO transcribe statement` under the problem's `\probhead`.
2. The line above it gives the source id, e.g. `% source id: 2016_TH_T11`. Look
   that problem up in the crop edition, or dump its text:

   ```bash
   python -c "
   import json,pymupdf,os
   m=json.load(open('../source/snippets/manifest.json'))
   for f,p,y0,y1 in m['2016_TH_T11']:
       root=os.environ.get('IOAA_PAPERS_DIR','../../IOAA Source Papers')
       d=pymupdf.open(os.path.join(root,f))
       print(d[p].get_text(clip=pymupdf.Rect(0,y0,1000,y1)))"
   ```

3. Replace the TODO with the statement. Figures are already placed; move the
   `\ioaafig` lines to where they belong in the text.
4. **Check the result against the crop edition.** Subscripts, exponents and
   units are where transcription goes wrong, and a wrong exponent looks
   perfectly plausible on the page.

`make_chapters.py` will not overwrite a chapter once anything in it has been
transcribed — it only regenerates files that are still pure scaffolding. Pass
`--force` to regenerate anyway (this destroys transcription).

## Caveats

- The diagonal "DELEGATION PRINT" watermark of the 2021/2023 delegation-print
  papers is removed in memory whenever either extraction tool opens a source
  paper. Both tools reject any generated or edited figure that still contains
  an active watermark object. Run `python fig_helper.py audit` to check all
  existing figure PDFs at once.
- Figure detection is heuristic (size, position, and whether the region has ink
  beyond a watermark). It errs toward including too much; check a figure before
  relying on it.
- Observation problems have no manifest crops, so they get no auto-extracted
  figures — their sky maps and charts must be pulled from the external
  `IOAA Source Papers/observation/` archive by hand.
- Observation problem labels and titles were read from the papers by hand and
  are less uniform than the theory/data-analysis ones; several are placeholders
  like "Telescope observation task" where the original had no title.
