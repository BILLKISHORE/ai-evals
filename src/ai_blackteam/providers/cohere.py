from ai_blackteam.registry import register_provider
from ai_blackteam.providers.base import OpenAICompatibleProvider


@register_provider("cohere")
class CohereProvider(OpenAICompatibleProvider):
    base_url = "https://api.cohere.com/compatibility/v1"
    provider_name = "cohere"
    supports_tools_flag = True

    def default_model(self):
        return "command-r-plus"
