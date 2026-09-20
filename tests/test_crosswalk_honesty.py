"""The OWASP category table must not read as checked when nobody checked it.

`crosswalks.py` exists to stop hand-copied OWASP labels drifting into reports
that cite OWASP while disagreeing with it. But the vendored file states its own
contents were "transcribed from the labels this repository already carried",
so the gate in tests/test_crosswalks.py compares the repo's labels against a
file derived from those same labels. It can only prove the 1000+ hand-written
labels agree with each other, which is the state the module says already held.
Real drift from OWASP, the failure it claims to close, stays undetectable.

That is acceptable as a first step; pretending otherwise is not. Every file
under standards/data carries a `verification` marker and a `verified_against`
source, and loader._check_verification_claims refuses a document that claims
verification it cannot support. The newest compliance data file had no such
guard at all while feeding every attack's OWASP citation.

This test holds it to the same standard the sibling package already meets.
"""

import json
from pathlib import Path

import pytest

import ai_blackteam
from ai_blackteam.crosswalks import CROSSWALK_FILENAME, load_crosswalk

DOC = json.loads(
    (Path(ai_blackteam.__file__).parent / "data" / CROSSWALK_FILENAME).read_text()
)


def test_the_source_block_declares_its_provenance():
    assert DOC["source"]["provenance"] in {"local-fixture", "owasp-published"}


def test_a_local_fixture_does_not_claim_a_verification_source():
    """verified_against is the claim that someone checked it against OWASP."""
    source = DOC["source"]
    if source["provenance"] == "local-fixture":
        assert not source.get("verified_against"), (
            "a locally transcribed file must not name a verification source"
        )


def test_every_category_carries_a_verification_marker():
    """Matches the convention every standards/data file already follows."""
    for code, entry in DOC["categories"].items():
        assert "verification" in entry, f"{code} has no verification marker"
        assert entry["verification"] in {"verified", "unverified"}, (
            f"{code} declares verification {entry['verification']!r}"
        )


def test_nothing_claims_verification_the_file_cannot_support():
    """The rule loader._check_verification_claims enforces for standards/."""
    if DOC["source"].get("verified_against"):
        return
    claiming = [c for c, e in DOC["categories"].items()
                if e.get("verification") == "verified"]
    assert not claiming, (
        f"categories claim verification with no verified_against source: {claiming}"
    )


def test_the_loader_rejects_an_unsupported_verification_claim(tmp_path, monkeypatch):
    """The guard has to bite, not just be documented."""
    from ai_blackteam import crosswalks

    bad = json.loads(json.dumps(DOC))
    bad["source"]["verified_against"] = None
    first = next(iter(bad["categories"]))
    bad["categories"][first]["verification"] = "verified"

    path = tmp_path / CROSSWALK_FILENAME
    path.write_text(json.dumps(bad))
    monkeypatch.setattr(crosswalks, "CROSSWALK_SEARCH_PATHS", (path,))
    crosswalks.load_crosswalk.cache_clear() if hasattr(
        crosswalks.load_crosswalk, "cache_clear") else None

    with pytest.raises(Exception, match="verif"):
        crosswalks.load_crosswalk()


def test_loading_still_works():
    assert load_crosswalk()["categories"]
