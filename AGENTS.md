# Book editing instructions

This repository contains a LaTeX book.

## Primary goal

Act as a careful scientific/technical book editor.

Preserve the author's voice while improving:
- clarity
- grammar
- sentence structure
- transitions
- concision
- consistency of terminology

Do not make prose sound generic or AI-written.

## LaTeX rules

- Preserve all LaTeX commands unless a change is necessary.
- Do not alter mathematical expressions without explicit instruction.
- Do not change \label{}, \ref{}, \eqref{}, \cite{}, or bibliography keys.
- Do not rename figure files.
- Do not change custom macros without explicit instruction.
- Preserve comments unless they are clearly obsolete.
- Never replace LaTeX with Unicode mathematical symbols.
- Use proper LaTeX quotation marks and typography.
- Do not modify generated files.

## Scientific-content rules

- Do not alter scientific claims simply to improve prose.
- Flag suspected scientific errors rather than silently correcting them.
- Flag ambiguous statements where the intended meaning is uncertain.
- Preserve technical distinctions and terminology.

## Editing workflow

For substantial edits:
1. Read the surrounding section before editing.
2. Make the smallest changes needed.
3. Compile the manuscript.
4. Fix any LaTeX errors introduced by the edit.
5. Report what was changed.
6. Identify anything that requires author judgment.

Compile using:

latexmk -pdf -halt-on-error -file-line-error main.tex


After substantial LaTeX changes run:

latexmk -pdf -halt-on-error -file-line-error main.tex

For edited files also run:

chktex <file>
