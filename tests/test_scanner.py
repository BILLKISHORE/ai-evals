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
