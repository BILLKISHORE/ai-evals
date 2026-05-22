from click.testing import CliRunner
from ai_blackteam.cli import cli


def test_scorecard_help_shows_standard_option():
    runner = CliRunner()
    result = runner.invoke(cli, ["scorecard", "--help"])
    assert "--standard" in result.output


def test_scorecard_agentic_standard_runs():
    runner = CliRunner()
    result = runner.invoke(cli, ["scorecard", "--standard", "agentic"])
    # exit 0 if runs exist, exit 2 if no runs (both are valid)
    assert result.exit_code in (0, 2)


def test_scorecard_llm_standard_runs():
    runner = CliRunner()
    result = runner.invoke(cli, ["scorecard", "--standard", "llm"])
    assert result.exit_code in (0, 2)


def test_scorecard_invalid_standard_fails():
    runner = CliRunner()
    result = runner.invoke(cli, ["scorecard", "--standard", "invalid"])
    assert result.exit_code != 0
