"""Reading the answer out of a reasoning model's response, and keeping the trace.

`anthropic.py` read `r.content[0].text`. When a model thinks, block 0 is a
thinking block, which has `.thinking` and no `.text`, so the guard fell through
and the response was captured as an empty string. Nothing raised. The evaluator
then scored `""`, which lands on UNCLEAR, which `scoring.py` counts as half a
bypass. Every run against a thinking model would have reported a middling
safety number computed on no text at all.

That went from latent to live when the aliases moved to claude-opus-5 and
claude-sonnet-5, both adaptive-thinking models.

The trace itself is worth keeping rather than discarding: the reasoning-layer
attacks in the 2026 literature (PRJA, OTora) turn on what happens inside the
thinking block while the final answer stays clean, so a harness that only sees
the answer cannot score them at all.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

from ai_blackteam.providers.anthropic import AnthropicProvider


def thinking_block(text="Let me work through this."):
    return SimpleNamespace(type="thinking", thinking=text, signature="sig")


def text_block(text="The answer."):
    return SimpleNamespace(type="text", text=text)


def provider_returning(blocks, stop_reason="end_turn"):
    p = AnthropicProvider(api_key="sk-test", model="claude-opus-5")
    p._client = MagicMock()
    p._client.messages.create.return_value = SimpleNamespace(
        content=blocks,
        usage=SimpleNamespace(input_tokens=1, output_tokens=2),
        stop_reason=stop_reason,
    )
    return p


# ── the answer must survive a thinking block ─────────────────────────


def test_answer_is_read_past_a_leading_thinking_block():
    p = provider_returning([thinking_block(), text_block("The answer.")])
    assert p.send_prompt("q").response == "The answer."


def test_answer_is_read_when_there_is_no_thinking_block():
    p = provider_returning([text_block("Just an answer.")])
    assert p.send_prompt("q").response == "Just an answer."


def test_multiple_text_blocks_are_joined_rather_than_truncated():
    """Taking only the first block silently drops the rest of the answer."""
    p = provider_returning([thinking_block(), text_block("Part one."), text_block("Part two.")])
    r = p.send_prompt("q")
    assert "Part one." in r.response and "Part two." in r.response


def test_a_response_that_is_only_thinking_yields_empty_text_not_a_crash():
    p = provider_returning([thinking_block()])
    r = p.send_prompt("q")
    assert r.response == ""
    assert r.reasoning, "the trace is still the only thing we got; keep it"


def test_conversations_read_the_answer_the_same_way():
    p = provider_returning([thinking_block(), text_block("Conversational answer.")])
    assert p.send_in_conversation([{"role": "user", "content": "q"}]).response == \
        "Conversational answer."


# ── the trace is captured ────────────────────────────────────────────


def test_reasoning_trace_is_kept_separately_from_the_answer():
    p = provider_returning([thinking_block("Step one, then step two."), text_block("Answer.")])
    r = p.send_prompt("q")
    assert r.reasoning == "Step one, then step two."
    assert r.reasoning not in r.response, "the trace must not contaminate the answer"


def test_reasoning_is_none_when_the_model_did_not_think():
    p = provider_returning([text_block("Answer.")])
    assert p.send_prompt("q").reasoning is None


def test_multiple_thinking_blocks_are_joined():
    p = provider_returning([thinking_block("First."), thinking_block("Second."), text_block("A.")])
    r = p.send_prompt("q")
    assert "First." in r.reasoning and "Second." in r.reasoning


def test_redacted_thinking_is_recorded_rather_than_dropped():
    """Encrypted or redacted thinking still tells you the model thought."""
    redacted = SimpleNamespace(type="redacted_thinking", data="AAAA")
    p = provider_returning([redacted, text_block("Answer.")])
    r = p.send_prompt("q")
    assert r.response == "Answer."
    assert r.reasoning is not None


def test_tool_use_results_also_carry_the_trace():
    tool = SimpleNamespace(type="tool_use", id="t1", name="read_file", input={"path": "x"})
    p = provider_returning([thinking_block("I should read the file."), tool])
    r = p.send_with_tools([{"role": "user", "content": "q"}], [])
    assert r.tool_calls[0]["tool"] == "read_file"
    assert r.reasoning == "I should read the file."


def test_prompt_result_defaults_reasoning_to_none():
    from ai_blackteam.providers.base import PromptResult, ToolResult

    assert PromptResult(response="x", model="m", provider="p").reasoning is None
    assert ToolResult(response="x", model="m", provider="p").reasoning is None


# ── the engine persists the trace ────────────────────────────────────


def test_engine_stores_the_reasoning_trace_alongside_the_answer():
    """Captured on the result but dropped before the store would be pointless."""
    from ai_blackteam.engine import Engine
    from ai_blackteam.providers.base import PromptResult

    class Thinker:
        model = "claude-opus-5"

        def get_model_info(self):
            return {"provider": "anthropic", "model": self.model}

        def send_prompt(self, prompt, system_prompt=None):
            return PromptResult(
                response="I can't help with that.", model=self.model, provider="anthropic",
                tokens_in=1, tokens_out=1, stop_reason="end_turn",
                reasoning="The user is asking for X. Policy says refuse.",
            )

    class Attack:
        technique_id = "t"
        mode = "single-turn"

        def generate_prompts(self, target):
            return ["p"]

    e = Engine(db_path=":memory:")
    e.run(Thinker(), Attack(), "make a weapon")
    run_id = e.storage.list_runs()[0]["id"]
    roles = {t["role"]: t["content"] for t in e.storage.get_turns(run_id)}
    assert roles["assistant"] == "I can't help with that."
    assert roles["reasoning"] == "The user is asking for X. Policy says refuse."


def test_engine_stores_no_reasoning_turn_when_the_model_did_not_think():
    from ai_blackteam.engine import Engine
    from ai_blackteam.providers.base import PromptResult

    class Plain:
        model = "m"

        def get_model_info(self):
            return {"provider": "p", "model": self.model}

        def send_prompt(self, prompt, system_prompt=None):
            return PromptResult(response="answer", model="m", provider="p")

    class Attack:
        technique_id = "t"
        mode = "single-turn"

        def generate_prompts(self, target):
            return ["p"]

    e = Engine(db_path=":memory:")
    e.run(Plain(), Attack(), "t")
    run_id = e.storage.list_runs()[0]["id"]
    assert "reasoning" not in {t["role"] for t in e.storage.get_turns(run_id)}
