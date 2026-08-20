"""Remove the known delegation-print overlay from source PDFs in memory.

The 2021 and 2023 delegation-print papers store the diagonal watermark in a
separate form XObject named ``Tr4``.  Its bounding box is the same in every
affected file.  Restricting removal to both that name and that bounding box
avoids touching unrelated PDF forms.

Source files are never rewritten: callers open a document through
``open_source_pdf`` and use the sanitized in-memory copy for rendering or
figure extraction.
"""

import pymupdf


WATERMARK_NAME = "Tr4"
WATERMARK_BBOX = pymupdf.Rect(111.2, 227.4, 475.5, 600.3)
COORD_TOLERANCE = 1.0


def _is_delegation_watermark(xobject):
    """Return whether an XObject matches the known delegation-print form."""
    _, name, _, bbox = xobject
    if name != WATERMARK_NAME:
        return False
    rect = pymupdf.Rect(bbox)
    return all(
        abs(actual - expected) <= COORD_TOLERANCE
        for actual, expected in zip(rect, WATERMARK_BBOX)
    )


def delegation_watermark_xrefs(document, active_only=False):
    """Find unique watermark-form xrefs in a PyMuPDF document."""
    found = set()
    for page in document:
        for xobject in page.get_xobjects():
            if not _is_delegation_watermark(xobject):
                continue
            xref = xobject[0]
            if active_only:
                stream = document.xref_stream(xref) or b""
                if not stream.strip():
                    continue
            found.add(xref)
    return sorted(found)


def strip_delegation_watermark(document):
    """Blank active delegation-print forms and return how many were removed."""
    xrefs = delegation_watermark_xrefs(document, active_only=True)
    for xref in xrefs:
        document.update_stream(xref, b" ")
    return len(xrefs)


def open_source_pdf(path):
    """Open a source PDF and remove its delegation watermark in memory."""
    document = pymupdf.open(path)
    strip_delegation_watermark(document)
    return document


def assert_no_delegation_watermark(document, path="PDF"):
    """Raise if a document still contains an active delegation watermark."""
    xrefs = delegation_watermark_xrefs(document, active_only=True)
    if xrefs:
        raise ValueError(
            f"{path} contains an active DELEGATION PRINT watermark "
            f"(PDF object{'s' if len(xrefs) != 1 else ''} "
            f"{', '.join(map(str, xrefs))})"
        )
