"""Reasoning effort had no route into the Gemini API at all.

`--effort` is passed straight to whichever provider the run selected, so a
provider that does not accept the keyword raises TypeError at construction.
Google was that provider: the flag worked on Anthropic, worked on the
OpenAI-compatible family, and was a hard error on Gemini. A sweep that wanted
to compare the same attack across vendors at the same thinking depth could not
include Google at all.

Google's shape is not an effort string. Thinking is configured inside the
generation config as a thinking_config, and the two variants are mutually
exclusive: the budget family takes a raw token allowance, the newer family
takes a level. Sending a thinking_config to a model that has no thinking stage
is a 400 rather than a graceful degradation, so those models have to be refused
before the request goes out rather than discovered halfway through a sweep.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from ai_blackteam.providers.google import GoogleProvider
from ai_blackteam.reasoning import (
    EFFORT_LEVELS,
    GOOGLE_THINKING_BUDGETS,
    GOOGLE_THINKING_LEVELS,
    google_thinking_config,
)

# A model from each family. The budget family takes thinking_budget; the newer
# family takes thinking_level.
BUDGET_MODEL = "gemini-2.5-pro"
LEVEL_MODEL = "gemini-3.5-flash"


def wired(**kw):
    p = GoogleProvider(api_key="test-not-real", **kw)
    p._client = MagicMock()
    p._client.models.generate_content.return_value = SimpleNamespace(
        text="ok",
        usage_metadata=SimpleNamespace(prompt_token_count=1, candidates_token_count=2),
    )
    return p


def sent_config(p):
    return p._client.models.generate_content.call_args.kwargs["config"]


# ── the config only appears when it was asked for ────────────────────


def test_no_effort_means_no_thinking_config_at_all():
    """Omitting it leaves the vendor default in place, which we do not know."""
    p = wired(model=BUDGET_MODEL)
    p.send_prompt("q")
    assert "thinking_config" not in sent_config(p)


def test_effort_is_sent_inside_the_generation_config():
    p = wired(model=BUDGET_MODEL, effort="low")
    p.send_prompt("q")
    assert "thinking_config" in sent_config(p)


def test_conversations_carry_the_thinking_config_too():
    p = wired(model=BUDGET_MODEL, effort="medium")
    p.send_in_conversation([{"role": "user", "content": "q"}])
    assert "thinking_config" in sent_config(p)


def test_a_system_prompt_and_a_thinking_config_coexist():
    p = wired(model=BUDGET_MODEL, effort="high")
    p.send_prompt("q", system_prompt="be careful")
    config = sent_config(p)
    assert config["system_instruction"] == "be careful"
    assert "thinking_config" in config


# ── the two vendor shapes are mutually exclusive ─────────────────────


def test_a_budget_model_gets_a_token_allowance_and_no_level():
    p = wired(model=BUDGET_MODEL, effort="low")
    p.send_prompt("q")
    thinking = sent_config(p)["thinking_config"]
    assert thinking["thinking_budget"] == GOOGLE_THINKING_BUDGETS["low"]
    assert "thinking_level" not in thinking, "sending both shapes is a 400"


def test_a_level_model_gets_a_level_and_no_token_allowance():
    p = wired(model=LEVEL_MODEL, effort="low")
    p.send_prompt("q")
    thinking = sent_config(p)["thinking_config"]
    assert thinking["thinking_level"] == GOOGLE_THINKING_LEVELS["low"]
    assert "thinking_budget" not in thinking, "sending both shapes is a 400"


# ── the mapping itself ───────────────────────────────────────────────


@pytest.mark.parametrize("level", EFFORT_LEVELS)
def test_every_documented_level_maps_to_something_sendable(level):
    budget = google_thinking_config(level, model=BUDGET_MODEL)
    assert isinstance(budget["thinking_budget"], int)
    assert google_thinking_config(level, model=LEVEL_MODEL)["thinking_level"]


def test_the_budget_ladder_rises_with_effort():
    """A higher effort that bought fewer thinking tokens would be a lie."""
    budgets = [GOOGLE_THINKING_BUDGETS[level] for level in EFFORT_LEVELS]
    assert budgets == sorted(budgets)
    assert len(set(budgets)) == len(budgets), "two levels that spend the same are one level"


def test_no_budget_is_the_dynamic_sentinel():
    """A negative budget hands the choice back to the model.

    That is the vendor default wearing an effort level's name, which would
    report a thinking depth the run never actually requested.
    """
    assert all(b > 0 for b in GOOGLE_THINKING_BUDGETS.values())


def test_the_request_does_not_hand_out_the_shared_mapping():
    """Two requests must not be able to edit each other's config."""
    p = wired(model=BUDGET_MODEL, effort="low")
    p.send_prompt("q")
    first = sent_config(p)["thinking_config"]
    p.send_prompt("q")
    second = sent_config(p)["thinking_config"]
    assert first == second
    assert first is not second


# ── models that cannot take it at all ────────────────────────────────


@pytest.mark.parametrize("model", ["gemini-1.5-pro", "gemini-2.0-flash", "gemma-3-27b-it"])
def test_a_model_with_no_thinking_stage_fails_at_construction(model):
    """The API answers a thinking_config with a 400. Say so before the sweep."""
    with pytest.raises(ValueError, match=model):
        GoogleProvider(api_key="test-not-real", model=model, effort="low")


@pytest.mark.parametrize("model", ["gemini-1.5-pro", "gemini-2.0-flash"])
def test_such_a_model_is_still_usable_without_an_effort_level(model):
    p = wired(model=model)
    assert p.send_prompt("q").response == "ok"


def test_an_unknown_google_model_is_allowed_through():
    """The list of thinking models grows every release; do not pre-block one."""
    p = wired(model="gemini-9-some-future-model", effort="max")
    p.send_prompt("q")
    assert "thinking_config" in sent_config(p)


# ── validation happens before the request, as everywhere else ────────


def test_an_invented_level_is_rejected_before_the_request():
    with pytest.raises(ValueError, match="turbo"):
        GoogleProvider(api_key="test-not-real", model=BUDGET_MODEL, effort="turbo")


def test_a_thinking_mode_is_rejected_as_an_effort_level():
    with pytest.raises(ValueError, match="adaptive"):
        GoogleProvider(api_key="test-not-real", model=BUDGET_MODEL, effort="adaptive")


def test_no_effort_asked_for_means_no_config_rather_than_a_default_one():
    """None is the absence of a request, not a request for the cheapest level."""
    assert google_thinking_config(None, model=BUDGET_MODEL) is None
