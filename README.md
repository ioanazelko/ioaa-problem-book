# IOAA Problem Book

The LaTeX collection of all IOAA problems and solutions, organized by topic.

The collection covers the 2007--2025 olympiads in 14 subject chapters. Problem
statements are transcribed as real LaTeX so they can be searched, restyled, and
reused in worksheets. Figures are cropped from the publicly available source
papers rather than redrawn.

This project is not affiliated with or endorsed by the IOAA. The official
papers remain the authoritative source and are available from the
[IOAA problem archive](https://ioaastrophysics.org/resources/problems-from-past-ioaa).

## Download PDF

[Download the latest release of the book](https://github.com/ioanazelko/ioaa-problem-book/releases/latest/download/ioaa-problem-book-2007-2025.pdf).
The release PDF uses the `ebook` optimization profile. Lossless and
print-oriented editions can be produced from the repository sources.

## Status

- 402 of 402 problem statements transcribed
- All available official solution material transcribed
- 385 problems with substantive official solutions
- 565 figure assets
- 14 topic-based chapters plus an errata appendix

The other 17 solution slots contain explanatory notes, not omitted
transcriptions. For 16 problems, no usable official solution was published or
survives in the available archives. The official key for one further problem,
a 2012 timed laser-pointing task, exists but contains no answer material.

## Building the book

The build requires a working TeX installation with `latexmk`, Python 3, and
[PyMuPDF](https://pymupdf.readthedocs.io/):

```bash
python -m pip install pymupdf
cd latex
python build_book.py
```

The generated file is `latex/book.pdf`. Generated PDFs are intentionally not
tracked in Git.

For a smaller distribution copy, pass an optional optimization profile:

```bash
python build_book.py --optimize ebook
```

Available profiles are `lossless`, `print`, `ebook`, and `screen`. The last
three require Ghostscript. The `ebook` profile is the recommended balance
between image quality and file size.

## Repository layout

- `latex/book.tex` is the master document.
- `latex/chapters/` contains the transcribed chapters and errata appendix.
- `latex/images/` contains the cropped figure assets used by the book.
- `latex/build_book.py` runs the normal build and optional PDF optimization.
- `optimize_pdf.py` implements the verified PDF optimization profiles.
- `source/` contains the tooling and classification data used for the separate
  crop-based edition. Original source papers are not included.

See [`latex/README.md`](latex/README.md) for transcription details, build
caveats, and the role of each file.

## Contributing

Corrections are welcome. Please compare numerical values, mathematical
notation, figures, and wording against the official paper before submitting a
change. Preserve LaTeX labels, references, citations, bibliography keys, and
custom macros unless a change specifically requires modifying them.

## Rights and attribution

No project-wide open-source license is granted. The olympiad problems,
solutions, and extracted figures are third-party material and remain subject to
the rights of their respective authors and organizers. See
[`NOTICE.md`](NOTICE.md) before copying or redistributing repository content.
