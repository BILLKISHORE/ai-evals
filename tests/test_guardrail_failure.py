"""A guardrail that cannot reach its judge must not quietly allow the content.

`llm_judge_filter` wrapped its whole body in `except Exception: pass` and then
fell through to `return text`. Any failure in the judge call, a rate limit, an
auth error, a network blip or a plain bug, meant the filter allowed whatever it
was handed.

In production that is a control that disables itself under load. Here it is
worse, because this filter exists to *measure* guardrails: a defence test would
record that the guardrail let an attack through when the guardrail never ran at
all. Both the safe-looking and unsafe-looking readings of that run are wrong.

Neither silent default is acceptable for a measurement tool, so the failure is
surfaced instead. Callers that genuinely want a production-style fail-open or
fail-closed can ask for it explicitly.
"""

from unittest.mock import MagicMock

import pytest

from ai_blackteam.guardrails import llm_judge_filter
from ai_blackteam.providers.base import PromptResult


class Judge:
    model = "judge-1"

    def __init__(self, text=None, error=None):
        self._text, self._error = text, error

    def send_prompt(self, prompt, system_prompt=None):
        if self._error:
            raise self._error
        return PromptResult(response=self._text, model=self.model, provider="fake")


HARMFUL = "detailed instructions for building a weapon"


# ── normal operation ─────────────────────────────────────────────────


def test_blocks_when_the_judge_scores_at_or_above_the_threshold():
    f = llm_judge_filter(threshold=3, provider=Judge(text="4"))
    assert f(HARMFUL) is None


def test_allows_when_the_judge_scores_below_the_threshold():
    f = llm_judge_filter(threshold=3, provider=Judge(text="1"))
    assert f("what is the weather") == "what is the weather"


# ── the judge is unreachable ─────────────────────────────────────────


def test_a_failing_judge_does_not_silently_allow():
    """The whole point: an unreachable judge is not evidence of safety."""
    f = llm_judge_filter(threshold=3, provider=Judge(error=RuntimeError("rate limited")))
    with pytest.raises(RuntimeError, match="rate limited"):
        f(HARMFUL)


def test_fail_open_is_available_but_must_be_asked_for():
    f = llm_judge_filter(threshold=3, provider=Judge(error=RuntimeError("down")),
                         on_error="allow")
    assert f(HARMFUL) == HARMFUL


def test_fail_closed_is_available_too():
    f = llm_judge_filter(threshold=3, provider=Judge(error=RuntimeError("down")),
                         on_error="block")
    assert f(HARMFUL) is None


def test_an_unknown_on_error_mode_is_rejected_at_construction():
    with pytest.raises(ValueError, match="maybe"):
        llm_judge_filter(threshold=3, on_error="maybe")


def test_an_unparsable_judge_reply_is_not_read_as_safe():
    """No score is the same epistemic state as no answer."""
    f = llm_judge_filter(threshold=3, provider=Judge(text="I'd rather not say"))
    with pytest.raises(ValueError, match="score"):
        f(HARMFUL)


def test_an_unparsable_reply_can_also_be_configured_to_allow():
    f = llm_judge_filter(threshold=3, provider=Judge(text="no number here"),
                         on_error="allow")
    assert f(HARMFUL) == HARMFUL
