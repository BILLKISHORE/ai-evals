"""Ollama and Bedrock reasoning models must not have their trace dropped.

The provider-reasoning audit after #10 found three providers left uncovered
that genuinely host reasoning models:

  Ollama serves deepseek-r1 and QwQ locally. Newer ollama returns the trace on
  a `thinking` field; the models themselves also emit the trace inline as
  <think>...</think> before the answer, the DeepSeek-R1 convention.

  Bedrock hosts Claude and other reasoning models through the Converse API,
  which returns the trace as a reasoningContent content block alongside the
  text block.

Without this, PRJA and OTora cannot be scored against a locally-run deepseek-r1
or a Claude model reached through Bedrock: the leak or the cost signal sits in
a trace the provider discarded.

Neither Ollama nor Bedrock reports a separate reasoning-token count (both fold
it into the total output count), so reasoning_tokens stays None here and the
docstring says why, rather than fabricating a number.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

from ai_blackteam.providers.base import split_reasoning_tags

LEAK = "Step 1: obtain the precursor. Step 2: combine as follows."
ANSWER = "I can't help with that."


# ── the shared <think> splitter ──────────────────────────────────────


def test_think_tags_are_split_from_the_answer():
    text = f"<think>{LEAK}</think>{ANSWER}"
    answer, reasoning = split_reasoning_tags(text)
    assert answer == ANSWER
    assert reasoning == LEAK


def test_text_without_think_tags_is_unchanged():
    answer, reasoning = split_reasoning_tags(ANSWER)
    assert answer == ANSWER
    assert reasoning is None


def test_an_unclosed_think_tag_is_left_alone():
    """A truncated response must not lose its whole body to a stray open tag."""
    answer, reasoning = split_reasoning_tags(f"<think>{LEAK}")
    assert answer == f"<think>{LEAK}"
    assert reasoning is None


def test_whitespace_around_the_answer_is_trimmed():
    answer, reasoning = split_reasoning_tags(f"<think>{LEAK}</think>\n\n{ANSWER}")
    assert answer == ANSWER
    assert reasoning == LEAK


# ── ollama ───────────────────────────────────────────────────────────


def _ollama(message):
    from ai_blackteam.providers.ollama import OllamaProvider

    p = OllamaProvider.__new__(OllamaProvider)
    p.model = "deepseek-r1"
    p._client = MagicMock()
    p._client.chat.return_value = message
    return p


def test_ollama_reads_the_thinking_field():
    """Newer ollama returns the trace on its own field."""
    msg = {"message": {"content": ANSWER, "thinking": LEAK}}
    r = _ollama(msg).send_prompt("hi")
    assert r.reasoning == LEAK
    assert r.response == ANSWER


def test_ollama_splits_inline_think_tags():
    """deepseek-r1 emits <think> inline when the field is absent."""
    msg = {"message": {"content": f"<think>{LEAK}</think>{ANSWER}"}}
    r = _ollama(msg).send_prompt("hi")
    assert r.reasoning == LEAK
    assert r.response == ANSWER


def test_ollama_without_reasoning_stays_clean():
    r = _ollama({"message": {"content": ANSWER}}).send_prompt("hi")
    assert r.reasoning is None
    assert r.response == ANSWER


