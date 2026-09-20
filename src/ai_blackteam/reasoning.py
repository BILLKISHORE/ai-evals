"""Reasoning effort, normalised across vendors.

Every current frontier model reasons before answering, and how much it reasons
is a request parameter. That is a red-team dimension rather than a tuning
knob: effort governs all output tokens including thinking, so the same attack
can land differently at ``low`` than at ``max``. Without a way to set it, a
sweep only ever measures the vendor default, and measures it silently.

The vendor shapes are not interchangeable:

    Anthropic               output_config={"effort": ...}
    OpenAI-compatible       reasoning_effort=...
    OpenAI Responses        reasoning={"effort": ...}
    Google                  generation_config.thinking_config

Google is the odd one: it takes no effort string at all. Thinking is a nested
block inside the generation config, and the block itself has two mutually
exclusive shapes, one counted in tokens and one named as a level. The
normalised levels are mapped onto it here so a sweep can ask for the same
thinking depth everywhere and get it.

Sending the wrong shape, or any shape to a model that does not accept it, is a
400 rather than a graceful degradation, so validation happens up front.
"""

from __future__ import annotations

# Documented levels, in increasing order of token spend. "high" is the API
# default and behaves identically to omitting the parameter.
EFFORT_LEVELS = ("low", "medium", "high", "xhigh", "max")

# A thinking mode, not an effort level. Easy to confuse because both describe
# how much the model thinks, and the docs call the mistake out explicitly.
_NOT_AN_EFFORT_LEVEL = ("adaptive", "enabled", "disabled")

# Model families known not to accept an effort parameter. Deliberately a
# denylist, not an allowlist: an allowlist goes stale every release and would
# make the tool refuse to test a model that works. Being wrong here costs one
# clear API error; being wrong the other way costs coverage.
_EFFORT_UNSUPPORTED_HINTS = ("haiku",)


GOOGLE_VENDOR = "the Gemini API"

# Google's thinking budget is a token allowance rather than a level, and the
# ceiling differs across the family. This ladder stays inside the narrowest
# documented range so one mapping is valid on every thinking model instead of
# 400ing on the smallest one.
#
# Every value is positive on purpose. The API reads a negative budget as
# "decide for yourself", which is the vendor default wearing an effort level's
# name: the run would report a thinking depth it never actually asked for.
GOOGLE_THINKING_BUDGETS = {
    "low": 1024,
    "medium": 4096,
    "high": 8192,
    "xhigh": 16384,
    "max": 24576,
}

# The newer family takes a named level instead of a token count and rejects the
# count. There are fewer levels than there are normalised ones, so the top of
# the ladder folds onto the highest. Folding loses resolution; it does not
# invent a level the vendor does not document.
GOOGLE_THINKING_LEVELS = {
    "low": "low",
    "medium": "medium",
    "high": "high",
    "xhigh": "high",
    "max": "high",
}

# Gemini families with no thinking stage at all. A thinking_config sent to one
# of these is rejected outright. Denylisted for the same reason as above: a new
# thinking model must stay testable the day it ships.
_GOOGLE_THINKING_UNSUPPORTED_HINTS = ("gemini-1.0", "gemini-1.5", "gemini-2.0", "gemma", "palm")

# Families that take a level rather than a token allowance. The same denylist
# argument in reverse: only the ones known to differ are named, so an unknown
# model gets the shape the rest of the family uses.
_GOOGLE_THINKING_LEVEL_HINTS = ("gemini-3",)


def validate_effort(effort, model=None, vendor="this model"):
    """Check an effort level up front. Returns it unchanged, or raises.

    Failing at construction turns what would be a 400 partway through a sweep
    into an immediate, readable error.
    """
    if effort is None:
        return None

    value = str(effort).lower()
    if value in _NOT_AN_EFFORT_LEVEL:
        raise ValueError(
            f"{value!r} is a thinking mode, not an effort level; "
            f"expected one of {', '.join(EFFORT_LEVELS)}"
        )
    if value not in EFFORT_LEVELS:
        raise ValueError(
            f"unknown effort level {value!r}; expected one of {', '.join(EFFORT_LEVELS)}"
        )

    if _matches_hint(model, _EFFORT_UNSUPPORTED_HINTS):
        raise ValueError(
            f"{model} does not accept an effort parameter, so {vendor} would "
            f"reject this request. Drop effort, or choose a model that supports it."
        )
    return value


def _matches_hint(model, hints):
    """Whether a model name contains any of a family's denylist hints."""
    name = (model or "").lower()
    return any(hint in name for hint in hints)


def google_thinking_config(effort, model=None):
    """The Gemini thinking_config for a normalised effort level, or None.

    None means no effort was requested, which is not the same as requesting
    none: the caller gets whatever the vendor decides, and this does not
    pretend to know what that was. Raises for a model that has no thinking
    stage, because omitting the block silently would report a run as having
    used an effort level it never got.
    """
    if effort is None:
        return None

    level = validate_effort(effort, model=model, vendor=GOOGLE_VENDOR)
    if _matches_hint(model, _GOOGLE_THINKING_UNSUPPORTED_HINTS):
        raise ValueError(
            f"{model} has no thinking stage, so {GOOGLE_VENDOR} would reject a "
            f"thinking_config. Drop effort, or choose a model that thinks."
        )
    # include_thoughts is what makes the trace come back. Without it Gemini
    # still reasons and still bills for it, but returns no thought parts, so
    # a reasoning-layer attack has nothing to score and the run looks clean.
    if _matches_hint(model, _GOOGLE_THINKING_LEVEL_HINTS):
        return {"thinking_level": GOOGLE_THINKING_LEVELS[level],
                "include_thoughts": True}
    return {"thinking_budget": GOOGLE_THINKING_BUDGETS[level],
            "include_thoughts": True}
