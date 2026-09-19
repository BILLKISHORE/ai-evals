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
    # Derived from the alias registry so a model refresh does not need a test
    # edit; a hardcoded id here is what went stale last time.
    from ai_blackteam.aliases import MODEL_ALIASES
    assert MODEL_ALIASES["anthropic"]["balanced"] in result.output
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


def test_aliases_module_has_three_keywords():
    from ai_blackteam.aliases import ALIAS_KEYWORDS
    assert ALIAS_KEYWORDS == {"latest", "fast", "balanced"}


def test_resolve_alias_anthropic_latest():
    from ai_blackteam.aliases import resolve_alias
    assert resolve_alias("anthropic", "latest") == "claude-opus-5"
    assert resolve_alias("anthropic", "fast") == "claude-haiku-4-5"
    assert resolve_alias("anthropic", "balanced") == "claude-sonnet-5"


def test_aliases_do_not_point_at_legacy_claude_generations():
    """latest/balanced are meant to track the frontier, not drift into legacy.

    Anthropic's model overview lists Opus 4.8, Opus 4.7, Opus 4.6, Sonnet 4.6
    and Sonnet 4.5 as legacy. They still serve, so a stale alias fails silently
    rather than erroring, which is exactly why this needs pinning.
    """
    from ai_blackteam.aliases import MODEL_ALIASES
    legacy = ("claude-opus-4-", "claude-sonnet-4-", "claude-3-")
    for provider in ("anthropic", "bedrock"):
        for tier, model in MODEL_ALIASES[provider].items():
            assert not any(m in model for m in legacy), (
                f"{provider}.{tier} points at legacy model {model!r}"
            )


def test_resolve_alias_passthrough():
    """Non-alias strings pass through unchanged."""
    from ai_blackteam.aliases import resolve_alias
    assert resolve_alias("anthropic", "claude-sonnet-4-6") == "claude-sonnet-4-6"
    assert resolve_alias("anthropic", None) is None
    assert resolve_alias("anthropic", "some-future-model-id") == "some-future-model-id"


def test_resolve_alias_unknown_provider():
    """Unknown providers with aliases just return the alias keyword unchanged."""
    from ai_blackteam.aliases import resolve_alias
    assert resolve_alias("nonexistent-provider", "latest") == "latest"


def test_list_models_shows_aliases():
    runner = CliRunner()
    result = runner.invoke(cli, ["list-models", "-p", "anthropic"])
    assert result.exit_code == 0
    assert "latest" in result.output
    assert "balanced" in result.output
    assert "fast" in result.output
    from ai_blackteam.aliases import MODEL_ALIASES
    assert MODEL_ALIASES["anthropic"]["latest"] in result.output


# ── undefined-name regressions ───────────────────────────────────────


def test_compare_actually_runs_the_providers():
    """`compare` referenced an undefined name and skipped every provider.

    The enclosing command takes `providers` (plural); the construction line
    used `provider`. The NameError was swallowed by a broad `except
    Exception` that printed "Skipping <name>", so the command rendered an
    empty table and exited successfully. In a script that reads as "nothing
    to report" rather than as a crash.
    """
    runner = CliRunner()
    result = runner.invoke(cli, [
        "compare", "--providers", "mock", "-a", "encoding-obfuscation", "-t", "test",
    ])
    assert "NameError" not in result.output, result.output
    assert "Skipping mock" not in result.output, result.output
    assert "mock" in result.output, "the provider row should be in the table"


def test_no_module_has_an_undefined_name():
    """Guards the class of bug that shipped an unusable Azure tool-use path.

    A scripted edit added a line referencing names defined in a sibling
    method. Nothing caught it: the provider had no tests, and the runtime
    error only surfaces on the one code path. A static check covers every
    module at once, including the ones with no tests at all.
    """
    import subprocess

    proc = subprocess.run(
        ["ruff", "check", "--select", "F821", "--no-cache", "--output-format", "concise",
         "src/ai_blackteam"],
        capture_output=True, text=True,
    )
    if proc.returncode != 0 and "F821" in proc.stdout:
        raise AssertionError(f"undefined names found:\n{proc.stdout}")


def test_expand_run_reports_attacks_that_errored(monkeypatch):
    """Failed attacks were dropped from the counts and from the total.

    `except Exception: pass` around each attack meant a run where half the
    suite crashed printed a summary over the surviving half, with the same
    shape as a clean run. A code bug and a network timeout vanished
    identically, and the total was the number that happened to succeed rather
    than the number attempted.

    Same principle as the scoring fix: an error is not a safety signal, so it
    is counted and shown rather than silently discarded.
    """
    from ai_blackteam.engine import Engine

    calls = {"n": 0}

    def flaky(self, provider, attack, target, **kw):
        calls["n"] += 1
        if calls["n"] % 2 == 0:
            raise RuntimeError("provider blew up")
        return [{"verdict": "BLOCKED", "run_id": 1, "confidence": 0.9,
                 "prompt": "p", "response_preview": "r"}]

    monkeypatch.setattr(Engine, "run", flaky)

    runner = CliRunner()
    result = runner.invoke(cli, [
        "expand", "run", "-p", "mock", "--category", "phishing", "--limit", "4",
    ])
    assert "ERROR" in result.output or "errored" in result.output.lower(), (
        f"errored attacks must be visible in the summary:\n{result.output}"
    )
