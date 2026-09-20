"""Load a vendored standards document and refuse the ones that overclaim.

Every scorecard in this package cites a published standard by identifier:
an AISVS chapter code, an AIVSS factor name, an EU AI Act article and
paragraph. Those identifiers get copied out of a report and into an email to
an auditor, so the one defect that matters here is an identifier that reads as
authoritative and was never checked against the source document.

The guard is mechanical rather than a convention. A document declares its
provenance once, in ``source``, and every citation inside it declares whether
it was checked. A citation may only say ``verified`` when the document also
names what it was verified against. Nothing in this checkout names one, so
nothing in this checkout may claim verification, and the moment somebody edits
a file to claim it without adding the source, loading fails instead of
printing it.

The second rule is the one ``crosswalks.py`` already established: a document
that cannot be read raises rather than returning an empty dict. A caller
handed ``{}`` reports a clean scorecard from a control that never ran.
"""

from __future__ import annotations

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

SUPPORTED_SCHEMA_VERSION = 1

# ``local-fixture`` means the content was transcribed into this repository by
# hand. ``primary-source`` is reserved for a document fetched from the
# publisher, which also has to fill in ``source.verified_against``.
PROVENANCE_VALUES = ("local-fixture", "primary-source")

VERIFICATION_VALUES = ("unverified", "verified")

_REQUIRED_KEYS = ("schema_version", "standard", "source")
_REQUIRED_SOURCE_KEYS = ("publisher", "provenance", "verified_against", "note")


class StandardsDataUnavailable(RuntimeError):
    """A standards document could not be read or could not be trusted.

    Raised rather than returning a partial document: a scorecard built from
    half a standard understates what it failed to check.
    """


def data_path(filename):
    """Return the packaged path for a data file, whether or not it exists."""
    return DATA_DIR / filename


def load(filename):
    """Load and validate a packaged standards document by file name."""
    return load_path(data_path(filename))


def load_path(path):
    """Load and validate a standards document from an explicit path.

    Raises:
        StandardsDataUnavailable: the file is missing, is not readable JSON,
            declares an unsupported schema, omits a required key, declares an
            unknown provenance, or carries a citation claiming verification
            that the document cannot support.
    """
    path = Path(path)
    if not path.is_file():
        raise StandardsDataUnavailable(f"no standards document at {path}")

    try:
        doc = json.loads(path.read_text())
    except (OSError, ValueError) as exc:
        raise StandardsDataUnavailable(f"{path} could not be read as JSON: {exc}") from exc

    _validate(doc, path)
    return doc


def _validate(doc, path):
    if not isinstance(doc, dict):
        raise StandardsDataUnavailable(f"{path} is not a JSON object")

    missing = [key for key in _REQUIRED_KEYS if key not in doc]
    if missing:
        raise StandardsDataUnavailable(f"{path} is missing required keys: {', '.join(missing)}")

    version = doc["schema_version"]
    if version != SUPPORTED_SCHEMA_VERSION:
        raise StandardsDataUnavailable(
            f"{path} has schema_version {version!r}, this code reads {SUPPORTED_SCHEMA_VERSION}"
        )

    source = doc["source"]
    if not isinstance(source, dict):
        raise StandardsDataUnavailable(f"{path} has no source block")

    missing_source = [key for key in _REQUIRED_SOURCE_KEYS if key not in source]
    if missing_source:
        raise StandardsDataUnavailable(
            f"{path} source block is missing: {', '.join(missing_source)}"
        )

    provenance = source["provenance"]
    if provenance not in PROVENANCE_VALUES:
        raise StandardsDataUnavailable(
            f"{path} declares provenance {provenance!r}, expected one of {PROVENANCE_VALUES}"
        )

    _check_verification_claims(doc, source.get("verified_against"), path)


def _check_verification_claims(doc, verified_against, path):
    """Reject any citation claiming verification the document cannot support."""
    for trail, value in _walk_verification(doc, ()):
        if value not in VERIFICATION_VALUES:
            raise StandardsDataUnavailable(
                f"{path}: {'.'.join(trail)} declares verification {value!r}, "
                f"expected one of {VERIFICATION_VALUES}"
            )
        if value == "verified" and not verified_against:
            raise StandardsDataUnavailable(
                f"{path}: {'.'.join(trail)} claims verification, but source."
                f"verified_against is empty. An identifier that nobody checked "
                f"must not be presented as checked."
            )


def _walk_verification(node, trail):
    """Yield every ``(path, value)`` pair for a ``verification`` key in the doc."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "verification":
                yield trail + (key,), value
            else:
                yield from _walk_verification(value, trail + (str(key),))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from _walk_verification(value, trail + (str(index),))


def provenance_block(doc):
    """Return the source block a report has to carry with its numbers."""
    return dict(doc["source"])
