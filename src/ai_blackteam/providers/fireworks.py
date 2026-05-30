from ai_blackteam.registry import register_provider
from ai_blackteam.providers.base import OpenAICompatibleProvider


@register_provider("fireworks")
class FireworksProvider(OpenAICompatibleProvider):
    base_url = "https://api.fireworks.ai/inference/v1"
    provider_name = "fireworks"
    supports_tools_flag = True

    def default_model(self):
        return "accounts/fireworks/models/llama-v3p3-70b-instruct"
