from ai_blackteam.registry import register_provider
from ai_blackteam.providers.base import OpenAICompatibleProvider


@register_provider("perplexity")
class PerplexityProvider(OpenAICompatibleProvider):
    base_url = "https://api.perplexity.ai"
    provider_name = "perplexity"

    def default_model(self):
        return "sonar-pro"
