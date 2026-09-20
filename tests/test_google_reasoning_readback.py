"""Turning thinking on is only half the job; it has to be read back.

GoogleProvider gained an effort-to-thinking-config mapping, but `_result`
never looked at the thought parts or the thought token count, so every Gemini
run came back with reasoning=None and reasoning_tokens=None no matter how
much thinking was paid for.

Two attacks depend on exactly those two fields. OTora (arXiv 2605.08876) is a
reasoning denial of service whose success signal IS the token count, and PRJA
(arXiv 2604.15725) hides its payload in the trace. Both were unscoreable
against Gemini: not wrong, but silently unmeasurable, which is the failure
mode this codebase keeps producing.

Google's shape differs from OpenAI's in both respects. Thoughts arrive as
parts flagged with `thought=True` inside the normal content parts rather than
in a separate field, and the count is `usage_metadata.thoughts_token_count`
rather than a nested details block. Both are read here.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from ai_blackteam.providers.base import read_reasoning_tokens


def _part(text, thought=False):
    return SimpleNamespace(text=text, thought=thought)


def _response(parts, thoughts_tokens=None, prompt_tokens=10, out_tokens=20):
    usage = SimpleNamespace(
        prompt_token_count=prompt_tokens,
        candidates_token_count=out_tokens,
        thoughts_token_count=thoughts_tokens,
    )
    candidate = SimpleNamespace(content=SimpleNamespace(parts=parts))
    answer = "".join(p.text for p in parts if not p.thought)
    return SimpleNamespace(text=answer, candidates=[candidate], usage_metadata=usage)


def _provider():
    from ai_blackteam.providers.google import GoogleProvider

    p = GoogleProvider.__new__(GoogleProvider)
    p.model = "gemini-3.5-flash"
    p._client = MagicMock()
    return p


# ── the token count ──────────────────────────────────────────────────


def test_the_google_thought_token_count_is_read():
    usage = SimpleNamespace(thoughts_token_count=2048)
    assert read_reasoning_tokens(usage) == 2048


def test_a_google_response_without_thoughts_reads_as_unknown():
    usage = SimpleNamespace(thoughts_token_count=None)
    assert read_reasoning_tokens(usage) is None


def test_a_zero_thought_count_is_kept():
    assert read_reasoning_tokens(SimpleNamespace(thoughts_token_count=0)) == 0


# ── the trace ────────────────────────────────────────────────────────


def test_thought_parts_land_in_reasoning_not_the_answer():
    r = _provider()._result(
        _response([_part("let me work through the synthesis", thought=True),
                   _part("I can't help with that.")]),
        ms=12.0)
    assert "synthesis" in r.reasoning
    assert "synthesis" not in r.response
    assert r.response == "I can't help with that."


def test_several_thought_parts_are_joined():
    r = _provider()._result(
        _response([_part("first ", thought=True), _part("second", thought=True),
                   _part("answer")]),
        ms=1.0)
    assert "first" in r.reasoning and "second" in r.reasoning


def test_no_thought_parts_leaves_reasoning_none():
    """Absent is unknown, never an empty string that reads as a clean trace."""
    r = _provider()._result(_response([_part("just an answer")]), ms=1.0)
    assert r.reasoning is None


def test_the_count_reaches_the_prompt_result():
    r = _provider()._result(
        _response([_part("thinking", thought=True), _part("answer")],
                  thoughts_tokens=4096), ms=1.0)
    assert r.reasoning_tokens == 4096


def test_ordinary_token_counts_still_work():
    r = _provider()._result(_response([_part("a")], prompt_tokens=7, out_tokens=9), ms=1.0)
    assert r.tokens_in == 7
    assert r.tokens_out == 9


# ── asking for the trace at all ──────────────────────────────────────


@pytest.mark.parametrize("effort", ["low", "high", "max"])
def test_the_thinking_config_asks_for_the_thoughts_back(effort):
    """Without include_thoughts Gemini reasons but returns no trace."""
    from ai_blackteam.reasoning import google_thinking_config

    cfg = google_thinking_config(effort, "gemini-2.5-pro")
    assert cfg is not None
    assert cfg.get("include_thoughts") is True, (
        "effort was set but the trace was never requested, so a reasoning "
        "attack has nothing to score"
    )
