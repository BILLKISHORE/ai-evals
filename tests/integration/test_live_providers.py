"""Live smoke tests against real provider APIs.

Marked with `pytest.mark.live` so they are skipped by default. Run with:

    pytest -m live tests/integration/

Each test auto-skips if the required env var (API key) is missing, so partial
runs work fine.
"""

import os
import pytest

LIVE_PROVIDER_ENV = [
    ("anthropic", "ANTHROPIC_API_KEY"),
    ("openai", "OPENAI_API_KEY"),
    ("google", "GOOGLE_API_KEY"),
    ("grok", "XAI_API_KEY"),
    ("deepseek", "DEEPSEEK_API_KEY"),
    ("mistral", "MISTRAL_API_KEY"),
    ("groq", "GROQ_API_KEY"),
    ("together", "TOGETHER_API_KEY"),
    ("perplexity", "PERPLEXITY_API_KEY"),
    ("cohere", "COHERE_API_KEY"),
    ("fireworks", "FIREWORKS_API_KEY"),
    ("ai21", "AI21_API_KEY"),
    ("huggingface", "HUGGINGFACE_API_KEY"),
]

SMOKE_PROMPT = "Reply with exactly the word OK and nothing else."


def _load_providers():
    from ai_blackteam import providers
    from ai_blackteam.registry import provider_registry
    provider_registry.discover(providers)
    return provider_registry


@pytest.mark.live
@pytest.mark.parametrize("provider_name,env_var", LIVE_PROVIDER_ENV)
def test_send_prompt_smoke(provider_name, env_var):
    """Each provider returns a non-empty response to a trivial prompt."""
    api_key = os.environ.get(env_var)
    if not api_key:
        pytest.skip(f"{env_var} not set")
    registry = _load_providers()
    cls = registry.get(provider_name)
    assert cls is not None, f"Provider {provider_name} not in registry"
    p = cls(api_key=api_key)
    result = p.send_prompt(SMOKE_PROMPT)
    assert result.response, f"{provider_name} returned empty response"
    assert result.model == p.model, f"{provider_name} model mismatch in result"
    assert result.provider == provider_name, f"{provider_name} provider mismatch in result"
    assert result.latency_ms is not None and result.latency_ms > 0


@pytest.mark.live
@pytest.mark.parametrize("provider_name,env_var", LIVE_PROVIDER_ENV)
def test_send_in_conversation_smoke(provider_name, env_var):
    """Each provider handles a 2-message conversation."""
    api_key = os.environ.get(env_var)
    if not api_key:
        pytest.skip(f"{env_var} not set")
    registry = _load_providers()
    cls = registry.get(provider_name)
    p = cls(api_key=api_key)
    messages = [
        {"role": "user", "content": "What is 1 + 1? Reply with just the number."},
    ]
    result = p.send_in_conversation(messages)
    assert result.response, f"{provider_name} returned empty conversation response"


@pytest.mark.live
def test_bedrock_smoke():
    """Bedrock needs AWS creds, not a single env var."""
    if not (os.environ.get("AWS_ACCESS_KEY_ID") or os.environ.get("AWS_PROFILE")):
        pytest.skip("AWS credentials not configured")
    try:
        import boto3  # noqa: F401
    except ImportError:
        pytest.skip("boto3 not installed (use [bedrock] extra)")
    registry = _load_providers()
    cls = registry.get("bedrock")
    p = cls()
    result = p.send_prompt(SMOKE_PROMPT)
    assert result.response
    assert result.provider == "bedrock"
