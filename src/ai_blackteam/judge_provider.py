"""Resolve the provider used for LLM-as-judge work.

The judge, the guardrail filter and the exploit verifier each constructed an
Anthropic client directly. For a tool that sells vendor neutrality that is an
easy criticism, but the practical cost is larger: a judge locked to one vendor
cannot be pointed at a second one to check whether a verdict is an artefact of
one model's opinion, which is the entire argument for the ensemble judge.

Everything goes through the provider registry instead, so any registered
provider can judge. Anthropic stays the default so existing behaviour and
existing results are unchanged.
"""

from __future__ import annotations

DEFAULT_JUDGE_PROVIDER = "anthropic"


def resolve_judge_provider(provider=None, model=None, api_key=None):
    """Return a provider instance to judge with.

    ``provider`` may be a registered provider name, an already-constructed
    provider (returned untouched, so callers holding one are not forced to
    re-resolve), or None for the default.
    """
    if provider is not None and not isinstance(provider, str):
        return provider

    from ai_blackteam.registry import provider_registry

    name = provider or DEFAULT_JUDGE_PROVIDER
    _ensure_providers_loaded()
    cls = provider_registry.get(name)
    if cls is None:
        available = ", ".join(sorted(provider_registry.list())) or "none registered"
        raise ValueError(f"unknown judge provider {name!r}; available: {available}")
    return cls(model=model, api_key=api_key)


def _ensure_providers_loaded():
    """Import the provider package so the registry decorators have run.

    The judge can be called from a library context that never went through the
    CLI's plugin loading, in which case the registry would otherwise be empty.
    """
    from ai_blackteam.registry import provider_registry

    if provider_registry.list():
        return
    import ai_blackteam.providers as providers_pkg

    provider_registry.discover(providers_pkg)


def ask_judge(provider, prompt):
    """Send a judge prompt and return its text.

    Going through ``send_prompt`` rather than a vendor client means the reply
    arrives as a PromptResult, so a judge that is itself refusing surfaces as a
    stop reason instead of an unparsable score.
    """
    result = provider.send_prompt(prompt)
    if getattr(result, "refused", None) is True:
        raise ValueError(
            f"judge {getattr(provider, 'model', '?')} refused to score this response "
            f"(stop_reason={result.stop_reason!r})"
        )
    return (result.response or "").strip()
