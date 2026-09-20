"""Gate the OWASP LLM Top 10 labels that attack modules carry as prose.

Every attack class hand-writes strings like ``"LLM01:2026 Prompt Injection"``,
and ``scorecard.OWASP_LLM_2026`` hand-writes the same ten category names a
second time. Nothing compared the two, and nothing compared either of them to
OWASP. A renamed category, a typo, or a bumped release year produced a report
that cites OWASP and disagrees with it, and the suite stayed green.

These tests make one vendored file the single source for the category ids,
names and release, and fail the moment a hand-written label drifts from it.
"""

import json

import pytest

import ai_blackteam.attacks
from ai_blackteam import crosswalks
from ai_blackteam.registry import attack_registry
from ai_blackteam.scorecard import OWASP_LLM_2026

attack_registry.discover(ai_blackteam.attacks)

_REGISTERED = sorted(attack_registry.list())


def _write_crosswalk(path, release="2026", categories=None, extra=None):
    doc = {
        "schema_version": 1,
        "standard": "OWASP Top 10 for Large Language Model Applications",
        "release": release,
        "source": {"provenance": "local-fixture"},
        "categories": categories
        if categories is not None
        else {"LLM01": {"name": "Prompt Injection"}},
        "framework_crosswalks": {"status": "not_vendored", "entries": None},
    }
    if extra:
        doc.update(extra)
    path.write_text(json.dumps(doc))
    return path


# ── the vendored file ────────────────────────────────────────────────


def test_the_crosswalk_file_is_present():
    assert crosswalks.crosswalk_path() is not None, (
        "no crosswalk file on any search path; the label gate cannot run"
    )


def test_the_crosswalk_carries_all_ten_categories():
    assert len(crosswalks.llm_categories()) == 10


def test_every_category_code_is_well_formed():
    bad = [c for c in crosswalks.llm_categories() if not crosswalks.CATEGORY_CODE.match(c)]
    assert not bad, f"codes that are not LLMnn: {bad}"


def test_category_codes_run_from_one_to_ten():
    assert sorted(crosswalks.llm_categories()) == [f"LLM{n:02d}" for n in range(1, 11)]


# ── loader behaviour ─────────────────────────────────────────────────


def test_a_missing_crosswalk_raises_instead_of_reporting_no_categories(tmp_path, monkeypatch):
    """An absent file is an error, never an empty mapping.

    Returning ``{}`` would turn a broken install into a passing label gate
    that checks nothing.
    """
    monkeypatch.setattr(crosswalks, "CROSSWALK_SEARCH_PATHS", (tmp_path / "gone.json",))
    assert crosswalks.crosswalk_path() is None
    with pytest.raises(crosswalks.CrosswalkUnavailable):
        crosswalks.llm_categories()


def test_the_loader_uses_the_first_search_path_that_exists(tmp_path, monkeypatch):
    first = _write_crosswalk(tmp_path / "first.json", release="1111")
    second = _write_crosswalk(tmp_path / "second.json", release="2222")
    monkeypatch.setattr(crosswalks, "CROSSWALK_SEARCH_PATHS", (first, second))
    assert crosswalks.load_crosswalk()["release"] == "1111"


def test_the_loader_falls_through_to_a_later_search_path(tmp_path, monkeypatch):
    second = _write_crosswalk(tmp_path / "second.json", release="2222")
    monkeypatch.setattr(
        crosswalks, "CROSSWALK_SEARCH_PATHS", (tmp_path / "absent.json", second)
    )
    assert crosswalks.load_crosswalk()["release"] == "2222"


def test_a_crosswalk_missing_its_categories_raises(tmp_path, monkeypatch):
    broken = tmp_path / "broken.json"
    broken.write_text(json.dumps({"schema_version": 1, "release": "2026"}))
    monkeypatch.setattr(crosswalks, "CROSSWALK_SEARCH_PATHS", (broken,))
    with pytest.raises(crosswalks.CrosswalkUnavailable) as err:
        crosswalks.load_crosswalk()
    assert "categories" in str(err.value)


def test_a_crosswalk_that_is_not_json_raises(tmp_path, monkeypatch):
    broken = tmp_path / "broken.json"
    broken.write_text("not json at all")
    monkeypatch.setattr(crosswalks, "CROSSWALK_SEARCH_PATHS", (broken,))
    with pytest.raises(crosswalks.CrosswalkUnavailable):
        crosswalks.load_crosswalk()


def test_a_crosswalk_from_an_unknown_schema_version_raises(tmp_path, monkeypatch):
    future = _write_crosswalk(tmp_path / "future.json", extra={"schema_version": 99})
    monkeypatch.setattr(crosswalks, "CROSSWALK_SEARCH_PATHS", (future,))
    with pytest.raises(crosswalks.CrosswalkUnavailable) as err:
        crosswalks.load_crosswalk()
    assert "schema_version" in str(err.value)


# ── label construction and parsing ───────────────────────────────────


def test_the_canonical_label_is_built_from_the_crosswalk():
    assert crosswalks.owasp_llm_label("LLM01") == "LLM01:2026 Prompt Injection"


def test_an_unknown_code_has_no_label():
    assert crosswalks.owasp_llm_label("LLM99") is None


def test_the_category_name_for_an_unknown_code_is_none():
    assert crosswalks.llm_category_name("LLM99") is None


def test_a_canonical_label_parses_back_into_its_parts():
    parsed = crosswalks.parse_owasp_llm_label("LLM03:2026 Excessive Agency")
    assert parsed == {"code": "LLM03", "release": "2026", "name": "Excessive Agency"}


@pytest.mark.parametrize(
    "label",
    [
        "",
        "Prompt Injection",
        "LLM01 Prompt Injection",
        "LLM1:2026 Prompt Injection",
        "LLM01:2026",
        "ASI01:2026 Agent Goal Hijack",
    ],
)
def test_prose_that_is_not_a_label_parses_to_none(label):
    """Unknown stays unknown; nothing here guesses a code or a release."""
    assert crosswalks.parse_owasp_llm_label(label) is None


def test_every_category_round_trips_through_label_and_parse():
    for code, name in crosswalks.llm_categories().items():
        parsed = crosswalks.parse_owasp_llm_label(crosswalks.owasp_llm_label(code))
        assert parsed["code"] == code
        assert parsed["name"] == name


# ── the divergence gates ─────────────────────────────────────────────


def test_attack_owasp_llm_labels_match_the_crosswalk():
    """The gate. One report naming every attack whose label has drifted."""
    unparsable = []
    unknown_code = []
    drifted = []
    for attack_id in _REGISTERED:
        for label in attack_registry.get(attack_id)().owasp_llm:
            parsed = crosswalks.parse_owasp_llm_label(label)
            if parsed is None:
                unparsable.append((attack_id, label))
                continue
            canonical = crosswalks.owasp_llm_label(parsed["code"])
            if canonical is None:
                unknown_code.append((attack_id, parsed["code"]))
            elif label != canonical:
                drifted.append((attack_id, label, canonical))
    assert not unparsable, f"labels that are not CODE:RELEASE Name: {unparsable}"
    assert not unknown_code, f"codes outside the OWASP LLM Top 10: {unknown_code}"
    assert not drifted, f"labels that no longer match the crosswalk: {drifted}"


def test_the_registry_actually_has_attacks_to_gate():
    """Without this, an empty registry would make the gate above vacuous."""
    assert len(_REGISTERED) > 900


def test_at_least_one_attack_carries_every_category():
    used = set()
    for attack_id in _REGISTERED:
        for label in attack_registry.get(attack_id)().owasp_llm:
            parsed = crosswalks.parse_owasp_llm_label(label)
            if parsed:
                used.add(parsed["code"])
    assert used == set(crosswalks.llm_categories()), (
        f"categories no attack references: {sorted(set(crosswalks.llm_categories()) - used)}"
    )


def test_the_scorecard_category_table_matches_the_crosswalk():
    """The second hand-written copy of the same ten names."""
    assert OWASP_LLM_2026 == crosswalks.llm_categories()


# ── provenance honesty ───────────────────────────────────────────────


def test_an_unvendored_framework_crosswalk_is_none_not_empty():
    """"Not fetched yet" and "OWASP maps this to nothing" are different facts."""
    assert crosswalks.framework_crosswalk_status() == "not_vendored"
    assert crosswalks.framework_crosswalk_entries() is None


def test_a_local_fixture_may_not_claim_published_crosswalk_entries(tmp_path, monkeypatch):
    """Stops a future edit from filling in relations OWASP never published."""
    lying = _write_crosswalk(tmp_path / "lying.json")
    doc = json.loads(lying.read_text())
    doc["framework_crosswalks"] = {"status": "vendored", "entries": {"LLM01": {}}}
    lying.write_text(json.dumps(doc))
    monkeypatch.setattr(crosswalks, "CROSSWALK_SEARCH_PATHS", (lying,))
    with pytest.raises(crosswalks.CrosswalkUnavailable) as err:
        crosswalks.load_crosswalk()
    assert "local-fixture" in str(err.value)


def test_vendored_entries_are_returned_when_provenance_backs_them(tmp_path, monkeypatch):
    real = _write_crosswalk(tmp_path / "real.json")
    doc = json.loads(real.read_text())
    doc["source"]["provenance"] = "owasp-published"
    doc["framework_crosswalks"] = {
        "status": "vendored",
        "entries": {"LLM01": {"mitre_atlas": ["AML.T0051"]}},
    }
    real.write_text(json.dumps(doc))
    monkeypatch.setattr(crosswalks, "CROSSWALK_SEARCH_PATHS", (real,))
    assert crosswalks.framework_crosswalk_status() == "vendored"
    assert crosswalks.framework_crosswalk_entries() == {"LLM01": {"mitre_atlas": ["AML.T0051"]}}


def test_the_file_says_where_its_contents_came_from():
    source = crosswalks.load_crosswalk()["source"]
    assert source["provenance"] in {"local-fixture", "owasp-published"}
    assert source["url"].startswith("https://")
