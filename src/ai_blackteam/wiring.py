"""Decisions an entry point has to make before it builds a provider.

An attack knows which output channel it is scored on, and a provider knows
how to produce that channel, but neither can see the other. The CLI sits
between them and used to pass along only model and api_key, so an attack that
needs the reasoning trace was handed a provider that never returns one.

Keeping the rule here rather than inside a click command means every entry
point applies the same one, instead of the twelve construction sites in
cli.py drifting apart.
"""

from __future__ import annotations

from ai_blackteam.signals import SIGNAL_REASONING, resolve_signal


def needs_reasoning_trace(attack):
    """Whether ``attack`` cannot be scored without the model's thinking.

    Only the reasoning channel needs it. A cost attack is scored on the token
    count, which providers report from ordinary usage metadata, so it does not
    require the far more expensive trace itself.
    """
    return resolve_signal(attack) == SIGNAL_REASONING


def provider_kwargs(attack, *, model, api_key, effort=None, reasoning_trace=None):
    """The keyword arguments an entry point should build the provider with.

    ``reasoning_trace`` is tri-state on purpose. None means decide from the
    attack, which is the default and what makes a reasoning attack work
    without the user knowing to ask. True and False are explicit overrides,
    for forcing the path on a normal attack or off when a model rejects it.

    Providers that do not accept a given argument must not be handed it, so
    the caller filters against the provider's signature.
    """
    kwargs = {"model": model, "api_key": api_key}
    if effort:
        kwargs["effort"] = effort
    wants = needs_reasoning_trace(attack) if reasoning_trace is None else reasoning_trace
    if wants:
        kwargs["use_responses"] = True
    return kwargs


def supported_kwargs(provider_cls, kwargs):
    """Drop arguments ``provider_cls`` does not accept.

    Eighteen providers share one call site and they do not share a signature.
    Passing `use_responses` to Anthropic is a TypeError, and an entry point
    crashing on an argument it added for someone else is worse than the
    feature being unavailable there.
    """
    import inspect

    try:
        params = inspect.signature(provider_cls.__init__).parameters
    except (TypeError, ValueError):
        return dict(kwargs)
    if any(p.kind is inspect.Parameter.VAR_KEYWORD for p in params.values()):
        return dict(kwargs)
    return {k: v for k, v in kwargs.items() if k in params}
