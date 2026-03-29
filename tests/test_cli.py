from click.testing import CliRunner
from blackteam.cli import cli


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
