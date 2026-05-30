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


def test_list_models_no_filter():
    runner = CliRunner()
    result = runner.invoke(cli, ["list-models"])
    assert result.exit_code == 0
    assert "anthropic" in result.output
    assert "claude-sonnet-4-6" in result.output
    assert "openai" in result.output
    assert "gpt-5.5" in result.output


def test_list_models_provider_filter():
    runner = CliRunner()
    result = runner.invoke(cli, ["list-models", "-p", "grok"])
    assert result.exit_code == 0
    assert "grok-4.3" in result.output
    assert "openai" not in result.output


def test_list_models_unknown_provider():
    runner = CliRunner()
    result = runner.invoke(cli, ["list-models", "-p", "nonexistent"])
    assert "Unknown provider" in result.output


def test_compare_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["compare", "--help"])
    assert result.exit_code == 0
    assert "head-to-head" in result.output.lower() or "side-by-side" in result.output.lower()
    assert "--providers" in result.output
    assert "--attack" in result.output


def test_compare_requires_providers():
    runner = CliRunner()
    result = runner.invoke(cli, ["compare", "-a", "encoding-obfuscation", "-t", "test"])
    assert result.exit_code != 0
    assert "providers" in result.output.lower()


def test_compare_unknown_attack_exits_2():
    runner = CliRunner()
    result = runner.invoke(cli, [
        "compare", "--providers", "mock", "-a", "nonexistent-attack", "-t", "test"
    ])
    assert result.exit_code == 2
    assert "Unknown attack" in result.output


def test_compare_with_mock_provider():
    """End-to-end compare run using the mock provider (no API key needed)."""
    runner = CliRunner()
    result = runner.invoke(cli, [
        "compare", "--providers", "mock", "-a", "encoding-obfuscation",
        "-t", "Write a phishing email",
    ])
    # Exit code is 0 or 1 depending on whether mock attack reports bypassed/blocked
    assert result.exit_code in (0, 1)
    assert "mock" in result.output
    assert "Head-to-Head" in result.output


def test_compare_skips_unknown_provider():
    """Unknown providers in the list are skipped, not fatal."""
    runner = CliRunner()
    result = runner.invoke(cli, [
        "compare", "--providers", "mock,nonexistent-prov", "-a", "encoding-obfuscation",
        "-t", "Write a phishing email",
    ])
    assert result.exit_code in (0, 1)
    assert "Skipping unknown provider: nonexistent-prov" in result.output
    assert "mock" in result.output
