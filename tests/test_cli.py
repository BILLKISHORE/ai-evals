from click.testing import CliRunner
from ai_blackteam.cli import cli


def test_list_providers():
    runner = CliRunner()
    result = runner.invoke(cli, ["list-providers"])
    assert result.exit_code == 0
    assert "anthropic" in result.output


def test_list_attacks():
    runner = CliRunner()
    result = runner.invoke(cli, ["list-attacks"])
    assert result.exit_code == 0
    assert "encoding-obfuscation" in result.output


def test_taxonomy_shows_atlas():
    runner = CliRunner()
    result = runner.invoke(cli, ["taxonomy"])
    assert result.exit_code == 0
    assert "AML.T" in result.output


def test_mlcommons_command():
    runner = CliRunner()
    result = runner.invoke(cli, ["mlcommons"])
    assert result.exit_code == 0
    assert "Violent Crimes" in result.output
    assert "ncr" in result.output
    assert "Harm Category Alignment" in result.output


def test_atlas_command():
    runner = CliRunner()
    result = runner.invoke(cli, ["atlas"])
    assert result.exit_code == 0
    assert "LLM Jailbreak" in result.output
    assert "AML.T0068" in result.output


def test_scorecard_command_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["scorecard", "--help"])
    assert result.exit_code == 0
    assert "OWASP" in result.output
    assert "--format" in result.output
    assert "--model" in result.output


def test_report_export_flag_exists():
    runner = CliRunner()
    result = runner.invoke(cli, ["report", "--help"])
    assert "--export" in result.output
    assert "promptfoo" in result.output
    assert "garak" in result.output


def test_expand_count():
    runner = CliRunner()
    result = runner.invoke(cli, ["expand", "count"])
    assert result.exit_code == 0
    assert "Techniques:" in result.output
    assert "Categories:" in result.output
    assert "Total attacks:" in result.output


def test_expand_list():
    runner = CliRunner()
    result = runner.invoke(cli, ["expand", "list", "--category", "phishing", "--limit", "5"])
    assert result.exit_code == 0
    assert "phishing" in result.output
