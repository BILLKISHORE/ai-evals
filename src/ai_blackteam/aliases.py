"""Model aliases that resolve to current frontier model IDs per provider.

Users can pass `--model latest`, `--model fast`, or `--model balanced` instead
of memorizing the exact current model string. Aliases are versioned in this
file alongside the provider defaults so they stay in sync.
"""

# Provider name -> alias -> concrete model ID
MODEL_ALIASES: dict[str, dict[str, str]] = {
    "anthropic": {
        "latest": "claude-opus-4-8",
        "fast": "claude-haiku-4-5",
        "balanced": "claude-sonnet-4-6",
    },
    "openai": {
        "latest": "gpt-5.5-pro",
        "fast": "gpt-5.5-instant",
        "balanced": "gpt-5.5",
    },
    "azure": {
        # Azure aliases map to deployment-name conventions; users still need to
        # set up the deployment with this name in their Azure resource.
        "latest": "gpt-5.5-pro",
        "fast": "gpt-5.5-instant",
        "balanced": "gpt-5.5",
    },
    "google": {
        "latest": "gemini-3.5-flash",
        "fast": "gemini-3.5-flash",
        "balanced": "gemini-3.1-pro",
    },
    "grok": {
        "latest": "grok-4.3",
        "fast": "grok-3-mini",
        "balanced": "grok-3.5",
    },
    "deepseek": {
        "latest": "deepseek-v4",
        "fast": "deepseek-chat",
        "balanced": "deepseek-v4",
    },
    "mistral": {
        "latest": "mistral-large-latest",
        "fast": "mistral-small-latest",
        "balanced": "mistral-medium-3.5",
    },
    "groq": {
        "latest": "llama-3.3-70b-versatile",
        "fast": "llama-3.1-8b-instant",
        "balanced": "llama-3.3-70b-versatile",
    },
    "together": {
        "latest": "meta-llama/Llama-4-Maverick-17B-128E-Instruct",
        "fast": "meta-llama/Llama-4-Scout-17B-16E-Instruct",
        "balanced": "meta-llama/Llama-4-Scout-17B-16E-Instruct",
    },
    "perplexity": {
        "latest": "sonar-reasoning-pro",
        "fast": "sonar",
        "balanced": "sonar-pro",
    },
    "cohere": {
        "latest": "command-r-plus",
        "fast": "command-r7b",
        "balanced": "command-r",
    },
    "fireworks": {
        "latest": "accounts/fireworks/models/deepseek-v4",
        "fast": "accounts/fireworks/models/llama-v3p3-70b-instruct",
        "balanced": "accounts/fireworks/models/qwen3p5-72b-instruct",
    },
    "ai21": {
        "latest": "jamba-1.6-large",
        "fast": "jamba-1.6-mini",
        "balanced": "jamba-1.6-large",
    },
    "bedrock": {
        "latest": "anthropic.claude-3-5-sonnet-20241022-v2:0",
        "fast": "anthropic.claude-3-haiku-20240307-v1:0",
        "balanced": "anthropic.claude-3-5-sonnet-20241022-v2:0",
    },
    "ollama": {
        "latest": "llama4",
        "fast": "llama3.3",
        "balanced": "llama4",
    },
    "huggingface": {
        "latest": "meta-llama/Llama-4-Scout-17B-16E-Instruct",
        "fast": "meta-llama/Llama-3.3-70B-Instruct",
        "balanced": "meta-llama/Llama-4-Scout-17B-16E-Instruct",
    },
}

ALIAS_KEYWORDS = {"latest", "fast", "balanced"}


def resolve_alias(provider_name: str, model: str | None) -> str | None:
    """Resolve a model alias to a concrete model ID.

    Returns the input unchanged if it isn't an alias keyword.
    """
    if model is None or model not in ALIAS_KEYWORDS:
        return model
    aliases_for_provider = MODEL_ALIASES.get(provider_name, {})
    return aliases_for_provider.get(model, model)
