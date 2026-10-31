# Yearly update prompt: add a new IOAA year to the problem book

How to use this file (not part of the prompt):

1. Wait until the organisers publish the question papers and the solutions,
   usually within a few weeks of the olympiad. Save the official zips, unpacked,
   in `../IOAA <YEAR>/` next to this repository (the 2026 ones were saved there
   as "Question Papers and Answer Sheets - Official English - ..." and
   "Solutions and Marking Scheme - ...").
2. Open Claude Code in this repository and paste everything below the rule,
   with `<YEAR>` and `<HOST>` filled in. For 2026 that is `2026` and
   `Hanoi, Vietnam`. Host cities are in the `HOSTS` dictionaries of
   `source/assemble_book.py` and `latex/make_chapters.py`; add the new one.
3. The run stops before pushing or publishing and asks for a go-ahead.

Estimated size of a run: about 20 problems (12 theory, 2 data analysis, 4 to 8
observation), a few hundred lines of LaTeX per problem including solutions.
Budget a long session; the transcription and verification phases fan out to
subagents.

---

You are updating the IOAA Problem Book in this repository
(`~/Dropbox/tutoring/My Resources/IOAA Problem Book`, GitHub
`ioanazelko/ioaa-problem-book`) with the problems of IOAA <YEAR>, hosted in
<HOST>. Two editions are involved: the crop edition built by
`source/assemble_book.py` from vector crops of the official papers, and the
LaTeX edition built from `latex/book.tex`, in which every statement and
solution is transcribed by hand. Work through the phases in order. Each phase
ends with checks that must pass before the next one starts. Do not push, tag,
or publish anything until the confirmation step in phase 6. Where a phase says
to use subagents, they write only to staging directories; nobody but you edits
`latex/chapters/`, and never two agents on the same file.

Read before starting: `README.md`, `source/README.md`, `latex/README.md`,
`AGENTS.md`, and the memory notes `ioaa-problem-book` and
`ioaa-paper-sources`. Editorial text that you write yourself (italic notes,
errata wording, README prose, commit messages) contains no em-dashes; the
transcribed official text stays verbatim, em-dashes included.

## Phase 0: preflight

- `git status` must be clean apart from the untracked cover PNGs and PDFs.
  If it is not, stop and ask.
- Record the baseline so the final report can show before and after:
  `grep -h '\\probhead' latex/chapters/ch*.tex | wc -l` (402 at the time of
  writing), `ls latex/images/*.pdf | wc -l` (565),
  `grep -c 'noindent.textbf' latex/chapters/errata.tex` (279), the page count
  of `latex/book.pdf` (908), `grep -c 'FIGURE NEEDED' latex/chapters/*.tex`
  (one legacy marker in ch15), and the latest tag from `gh release list`.
- Confirm the tools: `latexmk`, `gs`, `python3 -c "import pymupdf"`,
  `gh auth status`.

## Phase 1: source papers

- Look in `../IOAA <YEAR>/` for the official files. If the folder is missing,
  download the papers using the sources in the `ioaa-paper-sources` memory
  (aoXiv direct file paths first, then the official CDN, then BelAstro). If
  nothing can be found, stop and ask the user.
- Copy the papers into the external archive `../IOAA Source Papers/` with the
  established names: `<YEAR>_th.pdf`, `<YEAR>_th_sol.pdf`, `<YEAR>_da.pdf`,
  `<YEAR>_da_sol.pdf`. Observation rounds go into `observation/` as
  `<YEAR>_PLAN.pdf`, `<YEAR>_PLAN_sol.pdf`, `<YEAR>_SKYMAP.pdf`,
  `<YEAR>_SKYMAP_sol.pdf`, `<YEAR>_TEL.pdf`, `<YEAR>_TEL_sol.pdf`, plus any
  handed-out charts as `<YEAR>_Map-<label>.pdf` (see the 2025 files for the
  pattern). Leave out the team competition, the backup papers, and the answer
  sheets. Keep marking schemes in `../IOAA <YEAR>/` only: the book keeps the
  inline point values from the solutions and omits standalone rubrics. When the
  solutions and the marking scheme are separate files (as in 2026), the
  solution file is the source for the book; use the marking scheme only to
  recover point values that the solution text leaves out.
- Watermark check. Open each new paper with
  `latex/pdf_sanitize.open_source_pdf` and sweep `page.get_xobjects()` on a
  few pages. The known delegation-print overlay is a form XObject named `Tr4`
  and is removed in memory automatically. If a new overlay appears under a
  different name or bounding box, extend `pdf_sanitize.py` to recognise it;
  never rasterise or inpaint a figure to hide a watermark.
- Inventory. For every round, list label, title, and points, reading them
  from the papers. Labels follow the paper's own scheme (2025 used T01 to T12,
  D01 and D02, OP01 and OP02, OM01 to OM03, OT01 and OT02). Note any round
  whose solutions were not published; those slots get an italic note later.

## Phase 2: crop table and classification (in `source/`)

- `build_config.py`: add `job(...)` lines for the problem papers and for the
  solution papers, modelled on the 2025 lines (search for `2025_theory`).
  Choose anchor regexes by printing the actual heading lines with
  `split_pdf.all_lines` and make sure each anchor hits the start of its
  problem, not a contents-page entry (the 2014 bug) and not a heading restated
  inside the previous problem's text. Scanned papers get `pages=[a, b]`,
  0-based inclusive. One-problem-per-file papers get `whole=True`.
- Regenerate and dry-run the crop table:

  ```bash
  cd source && python build_config.py && python split_pdf.py config_all.json snippets --dry
  ```

  No `MISSING` lines. Then render the first, a middle, and the last problem
  and solution of each round with `python ../latex/render_png.py <id>` and look
  at the PNGs: crops must start at the heading and end before the next one.
- Classification. Create `classify_<Y0>_<Y0+4>.tsv` for the current five-year
  block (the first new block is `classify_2026_2030.tsv`), or append to it if
  it exists. Register a new file name in all three TSV lists:
  `load_class()` in `assemble_book.py`, `TSVS` in `latex/make_chapters.py`,
  and `TSVS` in `latex/dump_source.py`. Columns, tab-separated:
  `year, round (TH or DA), label, title, points or -, chapter 1-14, tag,
  secondary chapter or -`. Observation problems go into `classify_obs.tsv`
  with round codes `OBS-PLAN`, `OBS-SKY`, `OBS-TEL`, and the subject chapter
  in the chapter column; the LaTeX edition files them into chapter 15 anyway.
  Read every problem before assigning its chapter. Gravitational-wave problems
  go to chapter 14. When a problem straddles two chapters, choose the chapter
  of the physics it mainly tests and put the other in the secondary column.
  The tag is a short content note like the existing ones.
- Add `<YEAR>: "<HOST>"` to the `HOSTS` dictionaries in `assemble_book.py`
  and `latex/make_chapters.py`.
- Year strings in the crop edition: the front-matter title
  `"Problems by Topic, 2007 - <YEAR>"` and the output file name
  `IOAA_Problems_by_Topic_2007-<YEAR>.pdf` in `assemble_book.py`, the two
  entries in the root `.gitignore` (replace them with the glob
  `/IOAA_Problems_by_Topic_*.pdf` and `/source/IOAA_Problems_by_Topic_*.pdf`
  the first time), and the mentions of the crop-edition file name in
  `latex/README.md` and the comments at the top of `latex/book.tex`.
- `python assemble_book.py`. It exits with `UNMAPPED` if any classified
  problem lacks a manifest entry. Render the pages of two new problems and
  their solutions from the output and look at them. Once the new file is
  verified, delete the old crop PDF (it is untracked).

## Phase 3: LaTeX scaffolding and figures (in `latex/`)

- `make_chapters.py` refuses to touch a chapter that contains transcriptions,
  so do not run it against `chapters/`. Produce the blocks for the new year
  either by running it in a scratch copy (copy the script and
  `images/index.json`, point `OUT` at a scratch directory, run with `--force`,
  then take only the `<YEAR>` blocks) or with a short script that reproduces
  its format exactly:

  ```latex
  \probhead{<ch>.<n>}{<Title>}{<YEAR>}{<HOST>}{TH T01}{10}
  % source id: <YEAR>_TH_T01   tag: <tag>
  % TODO transcribe statement
  \ioaafig{<YEAR>_TH_T01-f1.pdf}
  ```

  and, in the chapter's solutions section,

  ```latex
  \solhead{<ch>.<n>}{<Title>}
  % source id: <YEAR>_TH_T01
  % TODO transcribe solution
  ```

  The `% source id:` lines are what `merge_fragments.py` keys on, and the
  `% TODO transcribe` markers are what it replaces, so both must be present.
- Insert each problem block after the last problem of the same section in its
  chapter: theory problems under `\section*{Theory problems}`, data analysis
  under `\section*{Data-analysis problems}`, observation problems under the
  matching round section of `ch15.tex` (keep its `% subject: Chapter N`
  comment). Insert each solution block at the matching position under
  `\section*{Solutions to Chapter N}`; solutions are in the same order as the
  problems. Add a missing section heading in the same style if a chapter has
  no problems of that round yet.
- Renumber. Numbers run continuously through a chapter in file order, so a new
  theory problem shifts every data-analysis number after it. Reuse
  `renumber.py` if it exists; otherwise write it: for each chapter, assign
  `\probhead{N.i}` in order of appearance, then give the i-th `\solhead` the
  same number, and assert that the counts match and the titles agree pairwise.
  Nothing else depends on the numbers: the cross-links are generated by the
  macros, and `errata.tex` is regenerated in phase 5. `FIGURE_AUDIT.md` is a
  historical record and keeps its old numbers.
- Figures. Back up `images/index.json` first: `extract_images.py` rewrites
  the index with only the ids it was given. Run it once for all new
  theory and data-analysis ids, merge the resulting entries back into the
  backup, and restore the merged file. Render every extracted figure to PNG
  and look at it; the heuristic produces banners, header crops, constants
  tables, and crops of the wrong problem. Delete junk and recrop by hand with
  `python fig_helper.py grid <pdf> <page>` followed by `crop`. Observation
  problems have no manifest entries, so their charts are cropped by hand from
  the observation PDFs. Solution figures are named `<id>-sN.pdf`. Finish with
  `python fig_helper.py audit`.

## Phase 4: transcription with subagents

- Give each agent 3 to 5 problems. Agents write fragments only:
  `staging/<id>.tex` for a statement and `staging_sol/<id>.tex` for a
  solution. They read the source with `python dump_source.py <id>` and
  `python render_png.py <id>`, and when text extraction scrambles the maths
  they read the PNG. For observation problems they open the observation PDF
  directly. Point them at two finished examples of the same kind in the
  chapters (for instance the 2025 problems in `ch14.tex` and `ch10.tex`).
- Statement conventions: verbatim wording; parts as
  `\begin{description}\item[(T01.1)] ... \hfill[points]`; thin-space units
  (`10\,km`); decimal points, not commas; tables with `tabular` or
  `booktabs`; no Unicode maths; `\ioaafig{...}` where the paper has the
  figure (a fragment that contains `\ioaafig` lines replaces the scaffold's
  auto-placed ones); `% sic: ...` on a genuine error in the official text,
  transcribed as printed; `% FIGURE NEEDED: <description>` for a figure not
  yet extracted; an italic `\textit{[...]}` note for material that was never
  digitised, such as a chart handed out separately.
- Solution conventions: the official reasoning with inline point values
  (`\hfill(1 point)`), no standalone rubric tables, `% sic:` on errors,
  `% FIGURE NEEDED:` on solution diagrams. If a round's solutions were not
  published, the slot gets an italic note saying so, in the style of the 2016
  and 2017 observation slots in `ch15.tex`.
- Merge centrally: `python merge_fragments.py` and
  `python merge_fragments.py --solutions`. Both print `UNUSED` fragments; that
  list must be empty, and `grep -c 'TODO transcribe' chapters/*.tex` must
  return zero everywhere.
- Verification pass. A second set of agents checks every new statement and
  solution digit by digit against the rendered PNGs (subscripts, exponents,
  units, and numerical values are where transcriptions go wrong) and records
  fixes as `OLD<<<...>>>` `NEW<<<...>>>` blocks in
  `staging_verify/ch<NN>_<YEAR>.md`. Apply them with
  `python apply_verify.py <logs> chapters/ch<NN>.tex` and re-read any block
  that reports no match.
- Resolve every new `% FIGURE NEEDED` marker with `fig_helper.py`, or with an
  italic note when the source was never digitised. The marker count must
  return to the phase 0 baseline.

## Phase 5: book text and build

- Year strings: `latex/book.tex` (the header comment, the crop-edition
  comment, and the inner title `2007--<YEAR>`), `latex/cover.tex` (the
  `2007--<YEAR>` label), `README.md` (the coverage sentence, the release link,
  and the Status counts), and the counts in `latex/README.md` and
  `source/README.md`. If the year needs a caveat (unpublished solutions, a
  scanned paper), add it to the "About this edition" page in `book.tex` in
  the existing tone.
- `python build_errata.py` regenerates `chapters/errata.tex` from the
  `% sic` comments.
- `python build_book.py`. The `.latexmkrc` figure audit must pass. Grep
  `book.log` for `undefined`, `multiply defined`, and `Overfull`; the first
  two must be absent and the third must not grow beyond the baseline. The page
  count must increase. Render the pages of every new problem and solution from
  `book.pdf` and look at them: headers, figure sizes, and the
  "solution p. N" links landing on the right page.
- Update the README status counts from the real numbers: `\probhead` count,
  `ls images/*.pdf | wc -l`, errata entries, and the number of problems with
  substantive solutions.

## Phase 6: commit, confirm, release

- Commit on `main` with a message such as `Add the IOAA <YEAR> problems and
  solutions`, ending with the attribution line the session requires. Do not
  push yet.
- Build the release copy with `python build_book.py --optimize ebook`, copy
  `latex/book.pdf` to the scratchpad as `ioaa-problem-book-2007-<YEAR>.pdf`,
  and compute its SHA-256. The asset name carries the year range, so the
  README release link must already name the new file; commit that before
  tagging.
- Show the user a summary and ask for a go-ahead: the table of new problems
  with their chapter assignments (flag any you are unsure of), the counts
  before and after, the page count, and anything unresolved. Only after a yes:
  `git push`, then `gh release create v1.<minor+1>.0 <pdf>` with a title like
  `IOAA Problem Book 2007–<YEAR>` and notes in the style of v1.0.1 (page
  count, year range, chapter layout, optimisation profile, SHA-256).
- Update the memory note `ioaa-problem-book` with the new state: counts,
  release tag, the year added, and anything left for next year.

## Final report

List what was added, the chapter assignment table with uncertain assignments
flagged, solutions that are missing or carry notes, figures that still need
hand work, and the files changed. Report any check that failed and was left
failing, with its output.
