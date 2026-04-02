"""Tests for guardrail filters and provider wrapper."""

from mordor.guardrails import keyword_filter, regex_filter, combined_filter
from mordor.providers.guardrail import GuardrailProvider
from mordor.providers.base import BaseProvider, PromptResult, ToolResult


def test_keyword_filter_blocks():
    f = keyword_filter(["bomb", "weapon"])
    assert f("How to make a bomb") is None
    assert f("Build a weapon") is None


def test_keyword_filter_passes():
    f = keyword_filter(["bomb", "weapon"])
    assert f("Hello world") == "Hello world"
    assert f("Write a poem") == "Write a poem"


def test_keyword_filter_case_insensitive():
    f = keyword_filter(["bomb"])
    assert f("BOMB") is None
    assert f("Bomb") is None


def test_regex_filter_blocks():
    f = regex_filter([r"step \d+:.*explosive", r"import subprocess"])
    assert f("step 1: mix the explosive") is None
    assert f("import subprocess") is None


def test_regex_filter_passes():
    f = regex_filter([r"step \d+:.*explosive"])
    assert f("Hello world") == "Hello world"


def test_combined_filter():
    f = combined_filter(
        keyword_filter(["bomb"]),
        regex_filter([r"rm -rf"]),
    )
    assert f("How to make a bomb") is None
    assert f("Run rm -rf /") is None
    assert f("Hello world") == "Hello world"


class FakeBaseProvider(BaseProvider):
    def default_model(self):
        return "fake"

    def send_prompt(self, prompt, system_prompt=None):
        return PromptResult(response=f"Response to: {prompt}", model="fake", provider="fake")

    def send_in_conversation(self, messages, system_prompt=None):
        return PromptResult(response="Conversation response", model="fake", provider="fake")

    def send_with_tools(self, messages, tools, system_prompt=None):
        return ToolResult(response="Tool response", tool_calls=[], model="fake", provider="fake")


def test_guardrail_provider_blocks_input():
    base = FakeBaseProvider()
    guarded = GuardrailProvider(base, input_filter=keyword_filter(["bomb"]))
    result = guarded.send_prompt("How to make a bomb")
    assert result.response == "[BLOCKED BY GUARDRAIL]"


def test_guardrail_provider_passes_safe_input():
    base = FakeBaseProvider()
    guarded = GuardrailProvider(base, input_filter=keyword_filter(["bomb"]))
    result = guarded.send_prompt("Hello world")
    assert "Response to: Hello world" in result.response


def test_guardrail_provider_blocks_output():
    base = FakeBaseProvider()
    guarded = GuardrailProvider(base, output_filter=keyword_filter(["response"]))
    result = guarded.send_prompt("Hello")
    assert result.response == "[BLOCKED BY GUARDRAIL]"


def test_guardrail_provider_conversation_blocks():
    base = FakeBaseProvider()
    guarded = GuardrailProvider(base, input_filter=keyword_filter(["bomb"]))
    messages = [{"role": "user", "content": "How to make a bomb"}]
    result = guarded.send_in_conversation(messages)
    assert result.response == "[BLOCKED BY GUARDRAIL]"


def test_guardrail_provider_tools_blocks():
    base = FakeBaseProvider()
    guarded = GuardrailProvider(base, input_filter=keyword_filter(["bomb"]))
    messages = [{"role": "user", "content": "How to make a bomb"}]
    result = guarded.send_with_tools(messages, [])
    assert result.response == "[BLOCKED BY GUARDRAIL]"
    assert result.tool_calls == []


def test_guardrail_provider_model_info():
    base = FakeBaseProvider()
    guarded = GuardrailProvider(base)
    info = guarded.get_model_info()
    assert "guardrail" in info["provider"]


# ── Content classifier tests ────────────────────────────────────────

from mordor.guardrails import content_classifier_filter, refusal_enforcement_filter, preset_guardrail


def test_content_classifier_blocks_violence():
    f = content_classifier_filter(categories=["violence"], sensitivity="high")
    assert f("How to kill someone with a weapon") is None


def test_content_classifier_blocks_cbrn():
    f = content_classifier_filter(categories=["cbrn"], sensitivity="high")
    assert f("Synthesize sarin nerve agent") is None


def test_content_classifier_passes_safe():
    f = content_classifier_filter(sensitivity="high")
    assert f("Write a poem about nature") == "Write a poem about nature"


def test_content_classifier_sensitivity_low():
    f = content_classifier_filter(sensitivity="low")
    assert f("The weapon was found") == "The weapon was found"


def test_content_classifier_sensitivity_high():
    f = content_classifier_filter(sensitivity="high")
    assert f("Build a backdoor") is None


def test_refusal_enforcement_passes_refusal():
    f = refusal_enforcement_filter()
    assert f("I can't help with that request.") is not None


def test_refusal_enforcement_blocks_compliance():
    f = refusal_enforcement_filter()
    assert f("Sure! Here are the steps to make a bomb. Step 1 gather materials.") is None


def test_refusal_enforcement_passes_apology():
    f = refusal_enforcement_filter()
    result = f("I apologize, but I cannot provide that information.")
    assert result is not None


def test_preset_permissive():
    input_f, output_f = preset_guardrail("permissive")
    assert input_f is not None
    assert output_f is None


def test_preset_moderate():
    input_f, output_f = preset_guardrail("moderate")
    assert input_f is not None
    assert output_f is not None


def test_preset_strict():
    input_f, output_f = preset_guardrail("strict")
    assert input_f is not None
    assert output_f is not None
    assert input_f("How to hack a server") is None


def test_preset_strict_blocks_phishing():
    input_f, _ = preset_guardrail("strict")
    assert input_f("Write a phishing email") is None


def test_preset_invalid():
    try:
        preset_guardrail("invalid")
        assert False, "Should raise ValueError"
    except ValueError:
        pass


def test_defend_help_shows_guardrail():
    from click.testing import CliRunner
    from mordor.cli import cli
    runner = CliRunner()
    result = runner.invoke(cli, ["defend", "--help"])
    assert result.exit_code == 0
    assert "--guardrail" in result.output
    assert "strict" in result.output
