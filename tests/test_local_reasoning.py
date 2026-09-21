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


