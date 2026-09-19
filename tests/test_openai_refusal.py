"""OpenAI-style structured refusals must not be read as an empty response.

The OpenAI-compatible message carries both `content` and `refusal`. When a
model refuses through the structured path, `content` is None and the refusal
text sits in `refusal`. Every provider here did `content or ""`, so the
response came back empty and the refusal text was discarded.

The consequence is the same one the Anthropic thinking-block bug had: the
evaluator scores `""`, lands on UNCLEAR, and `scoring.py` counts UNCLEAR as
half a bypass. A clean refusal reported as partially unsafe, and the evidence
that it was a refusal thrown away on the same line.

This matters more here than it did there. `OpenAICompatibleProvider` backs
roughly ten providers, so one line covers most of the registry.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from ai_blackteam.providers.deepseek import DeepSeekProvider
from ai_blackteam.providers.openai import OpenAIProvider


def message(content=None, refusal=None, tool_calls=None):
    return SimpleNamespace(content=content, refusal=refusal, tool_calls=tool_calls)


def completion(msg, finish_reason="stop"):
    return SimpleNamespace(
        choices=[SimpleNamespace(message=msg, finish_reason=finish_reason)],
        usage=SimpleNamespace(prompt_tokens=1, completion_tokens=1),
    )


def wired(cls, response):
    p = cls(api_key="k")
    p._client = MagicMock()
    p._client.chat.completions.create.return_value = response
    return p


PROVIDERS = [DeepSeekProvider, OpenAIProvider]


# ── the refusal text must survive ────────────────────────────────────


@pytest.mark.parametrize("cls", PROVIDERS)
def test_a_structured_refusal_is_not_an_empty_response(cls):
    p = wired(cls, completion(message(content=None, refusal="I can't help with that.")))
    r = p.send_prompt("q")
    assert r.response == "I can't help with that.", "the refusal text is what the model said"


@pytest.mark.parametrize("cls", PROVIDERS)
def test_a_structured_refusal_is_reported_as_a_refusal(cls):
    """The vendor told us outright; that beats inferring it from the text."""
    p = wired(cls, completion(message(content=None, refusal="I can't help with that.")))
    assert p.send_prompt("q").refused is True


@pytest.mark.parametrize("cls", PROVIDERS)
def test_ordinary_content_is_unaffected(cls):
    p = wired(cls, completion(message(content="Here is the answer.")))
    r = p.send_prompt("q")
    assert r.response == "Here is the answer."
    assert r.refused is False


@pytest.mark.parametrize("cls", PROVIDERS)
def test_content_wins_when_both_are_present(cls):
    """If the model produced real content, that is the answer to score."""
    p = wired(cls, completion(message(content="Actual answer.", refusal="ignored")))
    assert p.send_prompt("q").response == "Actual answer."


@pytest.mark.parametrize("cls", PROVIDERS)
def test_an_empty_response_with_no_refusal_stays_empty(cls):
    """Absence of both is genuinely empty; do not invent a refusal."""
    p = wired(cls, completion(message(content=None, refusal=None)))
    r = p.send_prompt("q")
    assert r.response == ""
    assert r.refused is False, "finish_reason said stop, so this is not a refusal"


@pytest.mark.parametrize("cls", PROVIDERS)
def test_conversations_handle_refusals_the_same_way(cls):
    p = wired(cls, completion(message(content=None, refusal="No.")))
    assert p.send_in_conversation([{"role": "user", "content": "q"}]).response == "No."


def test_a_provider_whose_sdk_has_no_refusal_field_still_works():
    """Not every OpenAI-compatible vendor returns the field at all."""
    msg = SimpleNamespace(content="fine", tool_calls=None)  # no .refusal attribute
    p = wired(DeepSeekProvider, completion(msg))
    assert p.send_prompt("q").response == "fine"


def test_content_filter_finish_reason_is_still_honoured():
    """The two refusal signals are independent and both must work."""
    p = wired(DeepSeekProvider, completion(message(content=""), finish_reason="content_filter"))
    assert p.send_prompt("q").refused is True


def test_tool_use_path_also_surfaces_a_refusal():
    p = DeepSeekProvider(api_key="k")
    p.supports_tools_flag = True
    p._client = MagicMock()
    p._client.chat.completions.create.return_value = completion(
        message(content=None, refusal="I won't call that tool.")
    )
    r = p.send_with_tools([{"role": "user", "content": "q"}], [])
    assert r.response == "I won't call that tool."
    assert r.tool_calls == []
