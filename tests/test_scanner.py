"""Tests for the AI code security scanner."""

from pathlib import Path
from ai_blackteam.scanner import scan_file, scan_directory, scan_summary, RULES

FIXTURES = Path(__file__).parent / "fixtures"
VULNERABLE = str(FIXTURES / "vulnerable_app.py")
SAFE = str(FIXTURES / "safe_app.py")


def test_rules_count():
    assert len(RULES) == 11


def test_rules_have_required_fields():
    required = ["id", "name", "severity", "owasp", "description", "patterns", "file_types", "message"]
    for rule in RULES:
        for field in required:
            assert field in rule, f"Rule {rule.get('id', '?')} missing field: {field}"


def test_rules_have_valid_severity():
    valid = {"critical", "high", "medium", "low"}
    for rule in RULES:
        assert rule["severity"] in valid, f"Rule {rule['id']} has invalid severity: {rule['severity']}"


def test_scan_vulnerable_file_finds_issues():
    findings = scan_file(VULNERABLE)
    assert len(findings) > 0


def test_scan_vulnerable_finds_prompt_injection():
    findings = scan_file(VULNERABLE)
    rule_ids = {f["rule_id"] for f in findings}
    assert "BTSC-001" in rule_ids, "Should detect prompt injection (user input in system prompt)"


def test_scan_vulnerable_finds_code_execution():
    findings = scan_file(VULNERABLE)
    rule_ids = {f["rule_id"] for f in findings}
    assert "BTSC-003" in rule_ids, "Should detect LLM output passed to dangerous function"


def test_scan_vulnerable_finds_sql_injection():
    findings = scan_file(VULNERABLE)
    rule_ids = {f["rule_id"] for f in findings}
    assert "BTSC-005" in rule_ids, "Should detect LLM output in SQL query"


def test_scan_vulnerable_finds_long_system_prompt():
    findings = scan_file(VULNERABLE)
    rule_ids = {f["rule_id"] for f in findings}
    assert "BTSC-009" in rule_ids, "Should detect hardcoded system prompt with sensitive content"


def test_scan_safe_file_no_critical():
    findings = scan_file(SAFE)
    critical = [f for f in findings if f["severity"] == "critical"]
    assert len(critical) == 0, f"Safe file should have no critical findings, got: {critical}"


def test_scan_nonexistent_file():
    findings = scan_file("/nonexistent/path.py")
    assert findings == []


def test_scan_directory():
    findings = scan_directory(str(FIXTURES))
    assert len(findings) > 0
    files = {f["file"] for f in findings}
    assert any("vulnerable_app.py" in f for f in files)


def test_findings_have_line_numbers():
    findings = scan_file(VULNERABLE)
    for f in findings:
        assert "line" in f
        assert isinstance(f["line"], int)
        assert f["line"] > 0


def test_findings_have_code_snippet():
    findings = scan_file(VULNERABLE)
    for f in findings:
        assert "code" in f
        assert len(f["code"]) > 0


def test_findings_have_owasp_mapping():
    findings = scan_file(VULNERABLE)
    for f in findings:
        assert "owasp" in f
        assert f["owasp"].startswith("LLM")


def test_scan_summary():
    findings = scan_file(VULNERABLE)
    summary = scan_summary(findings)
    assert summary["total"] > 0
    assert "by_severity" in summary
    assert "by_rule" in summary
    assert "by_owasp" in summary
    assert summary["files_affected"] == 1


def test_scan_summary_empty():
    summary = scan_summary([])
    assert summary["total"] == 0


def test_scan_cli_help():
    from click.testing import CliRunner
    from ai_blackteam.cli import cli
    runner = CliRunner()
    result = runner.invoke(cli, ["scan", "--help"])
    assert result.exit_code == 0
    assert "AI security vulnerabilities" in result.output
    assert "--severity" in result.output


def test_scan_cli_fixtures():
    from click.testing import CliRunner
    from ai_blackteam.cli import cli
    runner = CliRunner()
    result = runner.invoke(cli, ["scan", str(FIXTURES)])
    assert "BTSC-" in result.output


def test_api_scan():
    from ai_blackteam.api import Blackteam
    bt = Blackteam(db_path=":memory:")
    result = bt.scan(str(FIXTURES))
    assert result["summary"]["total"] > 0
    assert len(result["findings"]) > 0


# ── OWASP codes must follow the 2026 numbering ───────────────────────
#
# The 2026 migration renumbered the Top 10 but missed this module, so eight of
# the eleven rules kept emitting their 2025 codes. Under 2026 numbering those
# codes now name entirely different risks: LLM05 became Data and Model
# Poisoning, LLM06 became Unbounded Consumption, LLM10 became Improper Output
# Handling.

EXPECTED_OWASP = {
    "BTSC-001": "LLM01",  # Prompt Injection (unchanged)
    "BTSC-002": "LLM02",  # Sensitive Information Disclosure (unchanged)
    "BTSC-003": "LLM10",  # output executed as code -> Improper Output Handling
    "BTSC-004": "LLM10",  # output rendered as HTML -> Improper Output Handling
    "BTSC-005": "LLM10",  # output in SQL -> Improper Output Handling
    "BTSC-006": "LLM03",  # unrestricted shell -> Excessive Agency
    "BTSC-007": "LLM03",  # unrestricted file access -> Excessive Agency
    "BTSC-008": "LLM06",  # missing max_tokens -> Unbounded Consumption
    "BTSC-009": "LLM08",  # system prompt contents -> Hidden Context Exposure
    "BTSC-010": "LLM01",  # no input validation (unchanged)
    "BTSC-011": "LLM09",  # RAG without access control -> Vector and Embedding
}


def test_every_rule_maps_to_a_real_2026_category():
    from ai_blackteam.scorecard import OWASP_LLM_2026
    for rule in RULES:
        assert rule["owasp"] in OWASP_LLM_2026, (
            f"{rule['id']} emits {rule['owasp']}, which is not an OWASP 2026 category"
        )


def test_rule_owasp_codes_match_2026_semantics():
    actual = {r["id"]: r["owasp"] for r in RULES}
    assert actual == EXPECTED_OWASP


def test_output_handling_rules_are_not_labelled_data_poisoning():
    """LLM05 means Data and Model Poisoning in 2026, not Improper Output Handling."""
    by_id = {r["id"]: r for r in RULES}
    for rid in ("BTSC-003", "BTSC-004", "BTSC-005"):
        assert by_id[rid]["owasp"] != "LLM05"


def test_excessive_agency_rules_are_not_labelled_unbounded_consumption():
    """LLM06 means Unbounded Consumption in 2026, not Excessive Agency."""
    by_id = {r["id"]: r for r in RULES}
    for rid in ("BTSC-006", "BTSC-007"):
        assert by_id[rid]["owasp"] != "LLM06"
