"""An AISVS scorecard must report what it cannot test, not hide it.

A verification standard is a coverage claim. If a scorecard prints only the
chapters this tool happens to exercise, every chapter it cannot reach reads as
absent rather than untested, and the reader concludes the system was verified
against AISVS when most of AISVS was never looked at. A black-box prompt
runner sees prompt and response pairs; it cannot see training data lineage,
deployment configuration, identity, supply chain provenance, logging or human
oversight. Those chapters have to appear in the report saying exactly that.

The second thing these tests hold down is provenance. The chapter titles here
were transcribed locally, not fetched from OWASP, and the attack to chapter
assignment is this repository's own judgement rather than an OWASP crosswalk.
Both facts have to survive into the report, because a compliance artifact gets
quoted to an auditor.
"""

import json
import re
from pathlib import Path

import pytest

import ai_blackteam
from ai_blackteam.standards import aisvs
from ai_blackteam.standards.loader import StandardsDataUnavailable


def _runs(pairs):
    return [{"attack": attack, "verdict": verdict} for attack, verdict in pairs]


# Metadata that never touches the real registry, so these tests describe the
# report rather than the current attack catalogue.
_META = {
    "encoding-obfuscation": {"category": "encoding"},
    "harmful-instructions": {"category": "harmful-content"},
    "agent-credential-theft": {"category": "agent-exploitation"},
    "memory-poisoning": {"category": "memory-exploitation"},
    "pii-harvest": {"category": "privacy-violation"},
    "model-stealing": {"category": "adversarial-ml"},
    "invented-attack": {"category": "not-a-real-category"},
}


# ── the report covers the whole standard ─────────────────────────────


def test_report_lists_every_chapter_including_the_untestable_ones():
    report = aisvs.build_report(_runs([("encoding-obfuscation", "BLOCKED")]), _META)
    assert len(report["chapters"]) == aisvs.CHAPTER_COUNT
    assert report["total_chapters"] == aisvs.CHAPTER_COUNT


def test_chapter_codes_run_c1_through_c13():
    codes = set(aisvs.chapters())
    assert codes == {f"C{i}" for i in range(1, aisvs.CHAPTER_COUNT + 1)}


def test_every_chapter_has_a_title():
    for code, entry in aisvs.chapters().items():
        assert entry["title"].strip(), code


# ── what the tool cannot observe says so ─────────────────────────────


@pytest.mark.parametrize("code", ["C1", "C3", "C4", "C5", "C6", "C12", "C13"])
def test_chapters_a_prompt_runner_cannot_observe_are_not_assessable(code):
    report = aisvs.build_report(_runs([("harmful-instructions", "BYPASSED")]), _META)
    chapter = report["chapters"][code]
    assert chapter["status"] == "NOT_ASSESSABLE"
    assert chapter["reason"].strip(), f"{code} gives no reason it cannot be assessed"


def test_a_not_assessable_chapter_reports_no_counts_at_all():
    """Zero blocked out of zero would read as a measurement. It is not one."""
    report = aisvs.build_report(_runs([("harmful-instructions", "BYPASSED")]), _META)
    chapter = report["chapters"]["C4"]
    assert chapter["blocked"] is None
    assert chapter["total"] is None
    assert chapter["block_rate"] is None
    assert chapter["rating"] is None


def test_an_assessable_chapter_with_no_runs_is_not_assessed_rather_than_passing():
    report = aisvs.build_report(_runs([("encoding-obfuscation", "BLOCKED")]), _META)
    chapter = report["chapters"]["C9"]
    assert chapter["status"] == "NOT_ASSESSED"
    assert chapter["total"] == 0
    assert chapter["block_rate"] is None
    assert chapter["rating"] is None


def test_not_assessed_and_not_assessable_are_different_states():
    report = aisvs.build_report(_runs([("encoding-obfuscation", "BLOCKED")]), _META)
    assert report["chapters"]["C9"]["status"] != report["chapters"]["C4"]["status"]


# ── measured chapters ────────────────────────────────────────────────


def test_a_blocked_run_rates_its_chapter_as_pass():
    report = aisvs.build_report(_runs([("encoding-obfuscation", "BLOCKED")]), _META)
    chapter = report["chapters"]["C2"]
    assert chapter["status"] == "ASSESSED"
    assert chapter["blocked"] == 1
    assert chapter["total"] == 1
    assert chapter["block_rate"] == 100.0
    assert chapter["rating"] == "PASS"


def test_a_bypassed_run_rates_its_chapter_as_fail():
    report = aisvs.build_report(_runs([("harmful-instructions", "BYPASSED")]), _META)
    chapter = report["chapters"]["C7"]
    assert chapter["rating"] == "FAIL"
    assert chapter["block_rate"] == 0.0


def test_block_rate_is_the_ratio_of_blocked_runs():
    report = aisvs.build_report(
        _runs(
            [
                ("harmful-instructions", "BLOCKED"),
                ("harmful-instructions", "BLOCKED"),
                ("harmful-instructions", "BYPASSED"),
                ("harmful-instructions", "BYPASSED"),
            ]
        ),
        _META,
    )
    chapter = report["chapters"]["C7"]
    assert chapter["blocked"] == 2
    assert chapter["total"] == 4
    assert chapter["block_rate"] == 50.0


def test_an_unclear_verdict_counts_as_not_blocked_and_is_tallied_separately():
    """UNCLEAR is not a block, and it is not silently a bypass either."""
    report = aisvs.build_report(
        _runs([("harmful-instructions", "UNCLEAR"), ("harmful-instructions", "BLOCKED")]),
        _META,
    )
    chapter = report["chapters"]["C7"]
    assert chapter["blocked"] == 1
    assert chapter["total"] == 2
    assert chapter["unclear"] == 1


def test_ratings_use_the_same_thresholds_as_the_existing_scorecard():
    """Two rating ladders in one tool would drift. There is only one."""
    from ai_blackteam.scorecard import _get_rating

    for pct in (0, 29, 30, 59, 60, 89, 90, 100):
        assert aisvs.block_rate_rating(pct) == _get_rating(pct)


# ── nothing is dropped on the floor ──────────────────────────────────


def test_an_attack_outside_the_mapping_is_reported_not_discarded():
    report = aisvs.build_report(_runs([("invented-attack", "BYPASSED")]), _META)
    assert report["unmapped"]["runs"] == 1
    assert "invented-attack" in report["unmapped"]["attacks"]


def test_a_run_with_no_metadata_at_all_is_reported_as_unmapped():
    report = aisvs.build_report(_runs([("never-registered", "BLOCKED")]), {})
    assert report["unmapped"]["runs"] == 1
    assert "never-registered" in report["unmapped"]["attacks"]
    for chapter in report["chapters"].values():
        assert not chapter["total"], "an unmapped run leaked into a chapter tally"


def test_coverage_counts_assessed_chapters_against_the_whole_standard():
    report = aisvs.build_report(
        _runs([("encoding-obfuscation", "BLOCKED"), ("agent-credential-theft", "BLOCKED")]),
        _META,
    )
    assert report["assessed_chapters"] == 2
    assert report["assessable_chapters"] < aisvs.CHAPTER_COUNT
    assert report["total_chapters"] == aisvs.CHAPTER_COUNT


def test_coverage_is_never_expressed_as_a_pass_percentage_over_the_standard():
    """An overall percentage across 13 chapters from 2 tested ones is a lie."""
    report = aisvs.build_report(_runs([("encoding-obfuscation", "BLOCKED")]), _META)
    assert "overall_score" not in report


# ── requirement level data is absent, and says so ────────────────────


def test_requirement_level_verification_is_declared_unavailable():
    report = aisvs.build_report([], _META)
    assert report["requirements"]["status"] == "not_vendored"
    assert report["requirements"]["entries"] is None
    assert report["requirements"]["reason"].strip()


def test_no_requirement_identifier_is_invented_anywhere_in_the_data():
    """A requirement id like 2.4.3 would be quoted to an auditor verbatim."""
    raw = aisvs.AISVS_DATA_PATH.read_text()
    invented = re.findall(r"\b[Cc]?\d+\.\d+\.\d+\b", raw)
    assert invented == [], f"requirement-level identifiers appeared: {invented}"


def test_no_verification_level_is_claimed_per_chapter():
    for code, entry in aisvs.chapters().items():
        assert "level" not in entry, (
            f"{code} claims an AISVS level, but no requirement data was vendored "
            f"to support one"
        )


# ── provenance ───────────────────────────────────────────────────────


def test_report_carries_the_provenance_of_its_chapter_titles():
    report = aisvs.build_report([], _META)
    assert report["provenance"]["provenance"] == "local-fixture"
    assert report["provenance"]["verified_against"] is None


def test_the_attack_mapping_names_itself_as_local_judgement():
    mapping = aisvs.chapter_mapping_provenance()
    assert mapping["author"] == "ai-blackteam"
    assert mapping["is_owasp_crosswalk"] is False
    assert mapping["note"].strip()


def test_every_chapter_is_marked_unverified():
    for code, entry in aisvs.chapters().items():
        assert entry["verification"] == "unverified", code


def test_a_chapter_claiming_verified_without_a_source_is_rejected(tmp_path):
    doc = json.loads(aisvs.AISVS_DATA_PATH.read_text())
    doc["chapters"]["C1"]["verification"] = "verified"
    bad = tmp_path / "aisvs-bad.json"
    bad.write_text(json.dumps(doc))

    from ai_blackteam.standards import loader

    with pytest.raises(StandardsDataUnavailable):
        loader.load_path(bad)


def test_a_missing_data_file_raises_rather_than_returning_an_empty_standard(tmp_path):
    from ai_blackteam.standards import loader

    with pytest.raises(StandardsDataUnavailable):
        loader.load_path(tmp_path / "absent.json")


def test_the_data_file_ships_inside_the_package():
    package_root = Path(ai_blackteam.__file__).parent
    assert package_root in aisvs.AISVS_DATA_PATH.parents


# ── the render contract the CLI consumes ─────────────────────────────


def test_report_renders_a_table_with_one_row_per_chapter():
    report = aisvs.build_report(_runs([("encoding-obfuscation", "BLOCKED")]), _META)
    table = report["tables"][0]
    assert len(table["rows"]) == aisvs.CHAPTER_COUNT
    for row in table["rows"]:
        assert len(row) == len(table["columns"])


def test_rendered_rows_never_print_a_zero_for_an_unmeasured_chapter():
    report = aisvs.build_report(_runs([("encoding-obfuscation", "BLOCKED")]), _META)
    table = report["tables"][0]
    code_col = table["columns"].index("Chapter")
    by_code = {row[code_col]: row for row in table["rows"]}
    assert "0" not in by_code["C4"]
    assert "0.0%" not in by_code["C4"]


# ── rendering and the CLI ────────────────────────────────────────────


def test_markdown_render_keeps_the_provenance_notes_with_the_table():
    from ai_blackteam.standards import report_to_markdown

    report = aisvs.build_report(_runs([("encoding-obfuscation", "BLOCKED")]), _META)
    rendered = report_to_markdown(report)
    assert "C4" in rendered
    assert "NOT_ASSESSABLE" in rendered
    assert aisvs.chapter_mapping_provenance()["note"] in rendered


def test_json_render_round_trips_the_none_markers():
    from ai_blackteam.standards import report_to_json

    report = aisvs.build_report(_runs([("encoding-obfuscation", "BLOCKED")]), _META)
    payload = json.loads(report_to_json(report))
    assert payload["chapters"]["C4"]["total"] is None
    assert payload["chapters"]["C9"]["total"] == 0


def test_cli_offers_the_aisvs_standard():
    from click.testing import CliRunner
    from ai_blackteam.cli import cli

    result = CliRunner().invoke(cli, ["scorecard", "--help"])
    assert "aisvs" in result.output


def test_cli_accepts_the_aisvs_standard():
    from click.testing import CliRunner
    from ai_blackteam.cli import cli

    result = CliRunner().invoke(cli, ["scorecard", "--standard", "aisvs"])
    # 0 when the local database holds runs, 2 when it does not. Both are the
    # command working; neither is an unhandled error.
    assert result.exit_code in (0, 2)
