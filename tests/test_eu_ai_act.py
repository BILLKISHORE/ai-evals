"""EU AI Act mapping, and the ISO/IEC 27090 alignment that sits beside it.

Article 55(1)(a) is the one obligation in the Act that an adversarial testing
tool speaks to directly: it asks a provider of a general-purpose AI model with
systemic risk to conduct and document adversarial testing. Everything else in
Articles 55 and 73 is about incidents, mitigation, cybersecurity and reporting
deadlines, and a red team run is none of those. A test finding is not a
serious incident: no harm occurred, no causal link exists, and no reporting
clock starts. A scorecard that marked Article 73 as satisfied because the
suite ran would be telling a provider they had discharged a reporting duty
they have not even triggered.

So these tests hold two lines. The obligation identifiers must stay inside the
article and paragraph numbering the Act actually uses, and the status of every
obligation the tool cannot evidence must say so in words rather than showing a
green rating.

ISO/IEC 27090 is tested here rather than in a file of its own because the task
that added it assigned only these three test modules. Its whole content is one
claim: an alignment stated at document level, with no clause numbers, because
no clause number was checked against the published standard.
"""

import json
import re
from pathlib import Path

import pytest

import ai_blackteam
from ai_blackteam.standards import eu_ai_act, iso_27090
from ai_blackteam.standards.loader import StandardsDataUnavailable


def _runs(pairs):
    return [{"attack": attack, "verdict": verdict} for attack, verdict in pairs]


_META = {
    "bioweapon-synthesis": {"category": "cbrn-evasion"},
    "encoding-obfuscation": {"category": "encoding"},
    "voter-suppression": {"category": "election-interference"},
    "grooming-script": {"category": "child-safety"},
}


# ── the obligations that exist ───────────────────────────────────────


def test_article_55_carries_the_four_points_of_paragraph_one():
    codes = set(eu_ai_act.obligations())
    for point in "abcd":
        assert f"55(1)({point})" in codes


def test_article_73_paragraphs_are_present():
    codes = set(eu_ai_act.obligations())
    assert {"73(1)", "73(2)", "73(3)", "73(4)", "73(5)", "73(6)"} <= codes


def test_no_obligation_identifier_strays_outside_articles_55_and_73():
    pattern = re.compile(r"^(55|73)\(\d+\)(\([a-z]\))?$")
    for code in eu_ai_act.obligations():
        assert pattern.match(code), f"{code} is not an Article 55 or 73 citation"


def test_every_obligation_names_who_it_binds():
    """55 binds GPAI model providers with systemic risk, 73 binds high-risk providers."""
    for code, entry in eu_ai_act.obligations().items():
        assert entry["scope"].strip(), code
        assert entry["summary"].strip(), code


def test_every_obligation_is_marked_unverified():
    for code, entry in eu_ai_act.obligations().items():
        assert entry["verification"] == "unverified", code


# ── what the tool can evidence ───────────────────────────────────────


def test_adversarial_testing_obligation_is_evidenced_once_runs_exist():
    report = eu_ai_act.build_report(_runs([("encoding-obfuscation", "BLOCKED")]), _META)
    entry = report["obligations"]["55(1)(a)"]
    assert entry["status"] == "EVIDENCED"
    assert entry["runs"] == 1


def test_adversarial_testing_obligation_is_not_evidenced_without_runs():
    report = eu_ai_act.build_report([], _META)
    entry = report["obligations"]["55(1)(a)"]
    assert entry["status"] == "NOT_EVIDENCED"
    assert entry["runs"] == 0


def test_systemic_risk_obligation_counts_only_systemic_risk_findings():
    report = eu_ai_act.build_report(
        _runs(
            [
                ("encoding-obfuscation", "BYPASSED"),
                ("bioweapon-synthesis", "BYPASSED"),
                ("voter-suppression", "BLOCKED"),
            ]
        ),
        _META,
    )
    entry = report["obligations"]["55(1)(b)"]
    assert entry["runs"] == 2, "an encoding bypass is not a systemic risk finding"
    assert entry["bypassed"] == 1


def test_systemic_risk_obligation_is_partial_at_best():
    """Findings inform a risk assessment. Mitigation is not observable here."""
    report = eu_ai_act.build_report(_runs([("bioweapon-synthesis", "BYPASSED")]), _META)
    assert report["obligations"]["55(1)(b)"]["status"] == "PARTIAL"


def test_cybersecurity_obligation_is_out_of_scope_with_a_reason():
    report = eu_ai_act.build_report(_runs([("bioweapon-synthesis", "BYPASSED")]), _META)
    entry = report["obligations"]["55(1)(d)"]
    assert entry["status"] == "OUT_OF_SCOPE"
    assert entry["reason"].strip()
    assert entry["runs"] is None


# ── a test finding is not an incident ────────────────────────────────


@pytest.mark.parametrize("code", ["73(1)", "73(2)", "73(3)", "73(4)", "73(5)", "73(6)"])
def test_no_article_73_obligation_is_ever_marked_evidenced(code):
    report = eu_ai_act.build_report(
        _runs([("bioweapon-synthesis", "BYPASSED"), ("grooming-script", "BYPASSED")]),
        _META,
    )
    entry = report["obligations"][code]
    assert entry["status"] in {"READINESS_ONLY", "OUT_OF_SCOPE"}


def test_incident_reporting_obligation_explains_why_a_finding_is_not_an_incident():
    report = eu_ai_act.build_report(_runs([("bioweapon-synthesis", "BYPASSED")]), _META)
    reason = report["obligations"]["73(1)"]["reason"].lower()
    assert "incident" in reason
    assert "not" in reason


def test_bypassed_findings_never_start_a_reporting_clock():
    """Running more attacks must not move Article 73 toward satisfied."""
    quiet = eu_ai_act.build_report([], _META)
    loud = eu_ai_act.build_report(
        _runs([("bioweapon-synthesis", "BYPASSED")] * 50), _META
    )
    for code in ("73(1)", "73(2)", "73(3)", "73(4)", "73(5)", "73(6)"):
        assert quiet["obligations"][code]["status"] == loud["obligations"][code]["status"]


def test_report_warns_that_applicability_is_a_legal_determination():
    report = eu_ai_act.build_report([], _META)
    warning = report["scope_warning"].lower()
    assert "legal" in warning
    assert "general-purpose" in warning or "high-risk" in warning


# ── nothing is dropped, nothing is invented ──────────────────────────


def test_a_run_with_no_metadata_does_not_become_a_systemic_risk_finding():
    report = eu_ai_act.build_report(_runs([("never-registered", "BYPASSED")]), {})
    assert report["obligations"]["55(1)(b)"]["runs"] == 0
    assert report["unmapped"]["runs"] == 1


def test_an_unmapped_run_still_counts_as_adversarial_testing_performed():
    """55(1)(a) asks whether testing happened, not which harm it targeted."""
    report = eu_ai_act.build_report(_runs([("never-registered", "BYPASSED")]), {})
    assert report["obligations"]["55(1)(a)"]["runs"] == 1


def test_report_carries_the_provenance_of_its_citations():
    report = eu_ai_act.build_report([], _META)
    assert report["provenance"]["provenance"] == "local-fixture"
    assert report["provenance"]["verified_against"] is None


def test_an_obligation_claiming_verified_without_a_source_is_rejected(tmp_path):
    doc = json.loads(eu_ai_act.EU_AI_ACT_DATA_PATH.read_text())
    doc["obligations"]["55(1)(a)"]["verification"] = "verified"
    bad = tmp_path / "eu-bad.json"
    bad.write_text(json.dumps(doc))

    from ai_blackteam.standards import loader

    with pytest.raises(StandardsDataUnavailable):
        loader.load_path(bad)


def test_report_renders_a_table_with_one_row_per_obligation():
    report = eu_ai_act.build_report(_runs([("encoding-obfuscation", "BLOCKED")]), _META)
    table = report["tables"][0]
    assert len(table["rows"]) == len(report["obligations"])
    for row in table["rows"]:
        assert len(row) == len(table["columns"])


def test_the_data_file_ships_inside_the_package():
    package_root = Path(ai_blackteam.__file__).parent
    assert package_root in eu_ai_act.EU_AI_ACT_DATA_PATH.parents


# ── ISO/IEC 27090 ────────────────────────────────────────────────────


def test_iso_27090_alignment_states_no_clause_numbers():
    alignment = iso_27090.alignment()
    assert alignment["clauses"] is None
    assert alignment["clauses_reason"].strip()


def test_iso_27090_alignment_is_stated_at_document_level():
    assert iso_27090.alignment()["level"] == "document"


def test_iso_27090_data_contains_no_clause_like_identifier():
    """A clause number here would be fabricated, and would be quoted as real."""
    raw = iso_27090.ISO_27090_DATA_PATH.read_text()
    clause_like = re.findall(r"\b\d+\.\d+(?:\.\d+)*\b", raw)
    assert clause_like == [], f"clause-like identifiers appeared: {clause_like}"


def test_iso_27090_names_the_standard_it_aligns_to():
    alignment = iso_27090.alignment()
    assert alignment["standard"] == "ISO/IEC 27090"


def test_iso_27090_title_is_marked_unverified():
    alignment = iso_27090.alignment()
    assert alignment["title_verification"] == "unverified"


def test_iso_27090_lists_the_activities_it_claims_relate_to_the_standard():
    activities = iso_27090.alignment()["related_activities"]
    assert activities
    for activity in activities:
        assert activity["activity"].strip()
        assert activity["relation"].strip()


def test_iso_27090_does_not_claim_conformance():
    """Guidance is aligned with, not certified against."""
    alignment = iso_27090.alignment()
    assert alignment["claims_conformance"] is False
    joined = json.dumps(alignment).lower()
    assert "certif" not in joined


def test_iso_27090_data_ships_inside_the_package():
    package_root = Path(ai_blackteam.__file__).parent
    assert package_root in iso_27090.ISO_27090_DATA_PATH.parents


# ── rendering and the CLI ────────────────────────────────────────────


def test_markdown_render_carries_the_scope_warning():
    from ai_blackteam.standards import report_to_markdown

    report = eu_ai_act.build_report(_runs([("encoding-obfuscation", "BLOCKED")]), _META)
    rendered = report_to_markdown(report)
    assert "55(1)(a)" in rendered
    assert "73(1)" in rendered
    assert report["scope_warning"] in rendered


def test_json_render_keeps_none_for_an_out_of_scope_obligation():
    from ai_blackteam.standards import report_to_json

    report = eu_ai_act.build_report(_runs([("encoding-obfuscation", "BLOCKED")]), _META)
    payload = json.loads(report_to_json(report))
    assert payload["obligations"]["55(1)(d)"]["runs"] is None
    assert payload["obligations"]["55(1)(a)"]["runs"] == 1


def test_cli_offers_the_eu_ai_act_standard():
    from click.testing import CliRunner
    from ai_blackteam.cli import cli

    result = CliRunner().invoke(cli, ["scorecard", "--help"])
    assert "eu-ai-act" in result.output


def test_cli_accepts_the_eu_ai_act_standard():
    from click.testing import CliRunner
    from ai_blackteam.cli import cli

    result = CliRunner().invoke(cli, ["scorecard", "--standard", "eu-ai-act"])
    assert result.exit_code in (0, 2)
