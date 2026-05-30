from ai_blackteam.registry import register_provider
from ai_blackteam.providers.base import OpenAICompatibleProvider


@register_provider("mistral")
class MistralProvider(OpenAICompatibleProvider):
    base_url = "https://api.mistral.ai/v1"
    provider_name = "mistral"

    def default_model(self):
        return "mistral-large-latest"
