from click.testing import CliRunner
from blackteam.cli import cli


def test_scorecard_compliance_runs():
    runner = CliRunner()
    result = runner.invoke(cli, ["scorecard", "--standard", "compliance"])
    assert result.exit_code == 0


def test_scorecard_help_shows_compliance():
    runner = CliRunner()
    result = runner.invoke(cli, ["scorecard", "--help"])
    assert "compliance" in result.output
