"""Read the OWASP LLM Top 10 category table from data instead of from prose.

Every attack module hand-writes its OWASP labels as strings, for example
``owasp_llm = ["LLM01:2026 Prompt Injection"]``, and ``scorecard`` hand-writes
the same ten names a second time. Over a thousand copies of a table that OWASP
owns and periodically renames. Nothing compared the copies to each other, and
nothing compared any of them to OWASP, so a renamed category or a bumped
release year drifted into reports that cite OWASP while disagreeing with it,
and the suite stayed green through all of it.

This module makes one vendored file the source for the ids, names and release,
builds the canonical label from that file, and parses a written label back into
its parts. ``tests/test_crosswalks.py`` is the consumer that matters: it walks
every registered attack and fails the moment a hand-written label stops
matching the file.

What is deliberately absent: OWASP also publishes crosswalks from these
categories out to MITRE ATLAS, NIST AI RMF and ISO/IEC 42001. That artifact is
not in this checkout. ``framework_crosswalks`` therefore reports
``not_vendored`` with ``entries`` of ``None``, because "nobody fetched it yet"
and "OWASP maps this to nothing" are different facts and must not collapse into
the same empty dict. When the real artifact is vendored, ``entries`` takes the
shape ``{"LLM01": {"<framework>": ["<control id>", ...]}}`` and the provenance
in the file has to say it came from OWASP, not from here.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

CROSSWALK_FILENAME = "owasp-crosswalk.json"

# Search order: the copy that ships inside the installed package first, then
# the checkout's top-level data directory. An installed wheel only ever has
# the first; a source checkout today only has the second.
CROSSWALK_SEARCH_PATHS = (
    Path(__file__).parent / "data" / CROSSWALK_FILENAME,
    Path(__file__).resolve().parents[2] / "data" / CROSSWALK_FILENAME,
)

SUPPORTED_SCHEMA_VERSION = 1

# An OWASP LLM Top 10 category code, for example "LLM01".
CATEGORY_CODE = re.compile(r"^LLM\d{2}$")

# A written label: code, release year, then the category name.
_LABEL = re.compile(r"^(LLM\d{2}):(\d{4}) (.+)$")

_REQUIRED_KEYS = ("release", "source", "categories", "framework_crosswalks")
_PROVENANCE = ("local-fixture", "owasp-published")


class CrosswalkUnavailable(RuntimeError):
    """The crosswalk could not be read, so no category question can be answered.

    Raised rather than returning an empty table: a caller handed ``{}`` would
    report a clean result from a control that never ran.
    """


def crosswalk_path():
    """Return the first search path holding a crosswalk file, or None."""
    for candidate in CROSSWALK_SEARCH_PATHS:
        if candidate.is_file():
            return candidate
    return None


def load_crosswalk():
    """Return the vendored crosswalk document, validated.

    Raises:
        CrosswalkUnavailable: no file on any search path, unreadable JSON, an
            unsupported schema version, a missing required key, or a file whose
            declared provenance does not support the entries it carries.
    """
    path = crosswalk_path()
    if path is None:
        searched = ", ".join(str(p) for p in CROSSWALK_SEARCH_PATHS)
        raise CrosswalkUnavailable(f"no {CROSSWALK_FILENAME} on any search path: {searched}")

    try:
        doc = json.loads(path.read_text())
    except (OSError, ValueError) as exc:
        raise CrosswalkUnavailable(f"{path} could not be read as JSON: {exc}") from exc

    _validate(doc, path)
    return doc



# Mirrors standards/loader._check_verification_claims. A category id nobody
# checked against OWASP must not be presented as checked: this file feeds the
# OWASP citation on every one of the attack modules, so an unearned
# "verified" marker would propagate into every report the tool produces.
VERIFICATION_VALUES = ("verified", "unverified")


def _check_verification_claims(doc, path):
    verified_against = (doc.get("source") or {}).get("verified_against")
    for code, entry in (doc.get("categories") or {}).items():
        value = entry.get("verification")
        if value is None:
            raise CrosswalkUnavailable(
                f"{path}: category {code} carries no verification marker; "
                f"every category must declare one of {VERIFICATION_VALUES}"
            )
        if value not in VERIFICATION_VALUES:
            raise CrosswalkUnavailable(
                f"{path}: category {code} declares verification {value!r}, "
                f"expected one of {VERIFICATION_VALUES}"
            )
        if value == "verified" and not verified_against:
            raise CrosswalkUnavailable(
                f"{path}: category {code} claims verification, but "
                f"source.verified_against is empty. An identifier that nobody "
                f"checked must not be presented as checked."
            )


def _validate(doc, path):
    if not isinstance(doc, dict):
        raise CrosswalkUnavailable(f"{path} is not a JSON object")

    version = doc.get("schema_version")
    if version != SUPPORTED_SCHEMA_VERSION:
        raise CrosswalkUnavailable(
            f"{path} has schema_version {version!r}, this code reads {SUPPORTED_SCHEMA_VERSION}"
        )

    missing = [key for key in _REQUIRED_KEYS if key not in doc]
    if missing:
        raise CrosswalkUnavailable(f"{path} is missing required keys: {', '.join(missing)}")

    categories = doc["categories"]
    if not isinstance(categories, dict) or not categories:
        raise CrosswalkUnavailable(f"{path} has no categories")
    for code, entry in categories.items():
        if not isinstance(entry, dict) or not entry.get("name"):
            raise CrosswalkUnavailable(f"{path}: category {code} has no name")

    provenance = doc["source"].get("provenance")
    if provenance not in _PROVENANCE:
        raise CrosswalkUnavailable(
            f"{path} declares provenance {provenance!r}, expected one of {_PROVENANCE}"
        )

    crosswalks = doc["framework_crosswalks"]
    if crosswalks.get("status") == "vendored" and provenance == "local-fixture":
        raise CrosswalkUnavailable(
            f"{path} carries vendored crosswalk entries but its provenance is local-fixture; "
            "entries that did not come from OWASP must not claim they did"
        )

    _check_verification_claims(doc, path)


def llm_categories():
    """Return ``{code: name}`` for the OWASP LLM Top 10 the file describes."""
    return {code: entry["name"] for code, entry in load_crosswalk()["categories"].items()}


def llm_category_name(code):
    """Return the category name for a code, or None when the code is unknown."""
    entry = load_crosswalk()["categories"].get(code)
    if entry is None:
        return None
    return entry["name"]


def owasp_llm_label(code):
    """Return the canonical ``CODE:RELEASE Name`` label, or None if unknown.

    This is the string an attack module is expected to carry verbatim.
    """
    doc = load_crosswalk()
    entry = doc["categories"].get(code)
    if entry is None:
        return None
    return f"{code}:{doc['release']} {entry['name']}"


def parse_owasp_llm_label(label):
    """Split a written label into code, release and name.

    Returns None for anything that is not a well-formed OWASP LLM Top 10
    label. Nothing here guesses a code or a release from partial prose, so an
    unrecognised string stays unrecognised instead of becoming a plausible
    category.
    """
    if not isinstance(label, str):
        return None
    match = _LABEL.match(label)
    if match is None:
        return None
    return {"code": match.group(1), "release": match.group(2), "name": match.group(3)}


def framework_crosswalk_status():
    """Return the status of the out-to-other-frameworks crosswalk.

    ``"not_vendored"`` means OWASP's published artifact is not in this
    checkout. It does not mean OWASP publishes no relations.
    """
    return load_crosswalk()["framework_crosswalks"]["status"]


def framework_crosswalk_entries():
    """Return the crosswalk entries, or None when none have been vendored."""
    crosswalks = load_crosswalk()["framework_crosswalks"]
    if crosswalks["status"] != "vendored":
        return None
    return crosswalks["entries"]
