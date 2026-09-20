"""State the ISO/IEC 27090 alignment at document level, and stop there.

ISO/IEC 27090 covers guidance on addressing security threats to AI systems,
which is what this tool exists to exercise, so saying the two are aligned is
worth saying. Saying which clause a result satisfies is not, because the
published text is not in this checkout and its clause numbering was never
read.

A fabricated clause number is the worst defect this package could ship. It is
indistinguishable from a real citation, it survives copy and paste into an
audit response, and the reader has no way to check it without buying the
standard. An alignment with no clause numbers is weaker and true. This module
therefore exposes exactly one claim, with ``clauses`` permanently ``None`` and
a reason attached, and the test suite fails if a clause-shaped identifier ever
appears in the data file.
"""

from __future__ import annotations

from ai_blackteam.standards.loader import data_path, load, provenance_block

ISO_27090_DATA_FILENAME = "iso-27090.json"
ISO_27090_DATA_PATH = data_path(ISO_27090_DATA_FILENAME)

__all__ = ["ISO_27090_DATA_PATH", "alignment", "iso_27090_document"]


def iso_27090_document():
    """Return the vendored alignment document, validated."""
    return load(ISO_27090_DATA_FILENAME)


def alignment():
    """Return the document-level alignment statement.

    ``clauses`` is ``None`` and stays ``None`` until somebody reads the
    published standard and records what they checked it against.
    """
    doc = iso_27090_document()
    entry = doc["alignment"]
    return {
        "standard": doc["standard"],
        "level": entry["level"],
        "title": entry["title"],
        "title_verification": entry["title_verification"],
        "title_note": entry["title_note"],
        "claims_conformance": entry["claims_conformance"],
        "conformance_note": entry["conformance_note"],
        "clauses": entry["clauses"],
        "clauses_reason": entry["clauses_reason"],
        "related_activities": [dict(item) for item in entry["related_activities"]],
        "provenance": provenance_block(doc),
    }
