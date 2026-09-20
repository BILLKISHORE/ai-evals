"""Which channel of a model's output carries an attack's success signal.

Until the 2026 reasoning-layer attacks there was only one answer, so it was
never written down: harm appeared in the reply, and `evaluate(response)` was
the whole story.

Reasoning models broke that assumption. PRJA (arXiv 2604.15725) deliberately
keeps the reply clean and puts the payload in the thinking, so scoring the
reply reports a refusal for a model that complied in full. The channel an
attack targets is therefore part of the attack's definition, not a property
of the engine.

Attacks declare it with a ``success_signal`` class attribute. Anything that
does not declare one is scored on the response exactly as before, so the
existing corpus is unaffected.
"""

from __future__ import annotations

# The final answer the model returns to the user.
SIGNAL_RESPONSE = "response"

# The model's thinking, kept apart from the answer by the provider layer.
SIGNAL_REASONING = "reasoning"

VALID_SIGNALS = frozenset({SIGNAL_RESPONSE, SIGNAL_REASONING})

# What an attack that says nothing is scored on. Every pre-2026 attack.
DEFAULT_SIGNAL = SIGNAL_RESPONSE


def resolve_signal(attack):
    """The channel ``attack`` is scored on.

    Attacks are plugins, so reading an attribute that may be absent is a real
    boundary and a default is appropriate here. An unrecognised value is not:
    silently scoring a reasoning attack on the response is the exact failure
    this module exists to prevent, so it raises instead.
    """
    signal = getattr(attack, "success_signal", DEFAULT_SIGNAL)
    if signal not in VALID_SIGNALS:
        raise ValueError(
            f"{type(attack).__name__} declares success_signal={signal!r}; "
            f"expected one of {sorted(VALID_SIGNALS)}"
        )
    return signal


def has_content(text):
    """Whether a channel actually carried something.

    Whitespace is not a trace. A provider that returned an empty thinking
    block has told us nothing, which must not read as a clean result.
    """
    return bool(text and text.strip())
