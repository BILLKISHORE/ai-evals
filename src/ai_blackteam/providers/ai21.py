from ai_blackteam.registry import register_provider
from ai_blackteam.providers.base import OpenAICompatibleProvider


@register_provider("ai21")
class AI21Provider(OpenAICompatibleProvider):
    base_url = "https://api.ai21.com/studio/v1"
    provider_name = "ai21"
    supports_tools_flag = False

    def default_model(self):
        return "jamba-1.6-large"
