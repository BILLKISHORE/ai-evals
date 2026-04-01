from click.testing import CliRunner
from blackteam.cli import cli


def test_scorecard_help_shows_standard_option():
    runner = CliRunner()
    result = runner.invoke(cli, ["scorecard", "--help"])
    assert "--standard" in result.output


def test_scorecard_agentic_standard_runs():
    runner = CliRunner()
    result = runner.invoke(cli, ["scorecard", "--standard", "agentic"])
    assert result.exit_code == 0


def test_scorecard_llm_standard_runs():
    runner = CliRunner()
    result = runner.invoke(cli, ["scorecard", "--standard", "llm"])
    assert result.exit_code == 0


def test_scorecard_invalid_standard_fails():
    runner = CliRunner()
    result = runner.invoke(cli, ["scorecard", "--standard", "invalid"])
    assert result.exit_code != 0
