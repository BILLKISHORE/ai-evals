"""Reasoning effort, normalised across vendors.

Every current frontier model reasons before answering, and how much it reasons
is a request parameter. That is a red-team dimension rather than a tuning
knob: effort governs all output tokens including thinking, so the same attack
can land differently at ``low`` than at ``max``. Without a way to set it, a
sweep only ever measures the vendor default, and measures it silently.

The vendor shapes are not interchangeable:

    Anthropic               output_config={"effort": ...}
    OpenAI-compatible       reasoning_effort=...

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

    name = (model or "").lower()
    for hint in _EFFORT_UNSUPPORTED_HINTS:
        if hint in name:
            raise ValueError(
                f"{model} does not accept an effort parameter, so {vendor} would "
                f"reject this request. Drop effort, or choose a model that supports it."
            )
    return value
