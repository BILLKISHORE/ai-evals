from ai_blackteam.registry import register_provider
from ai_blackteam.providers.base import OpenAICompatibleProvider


@register_provider("deepseek")
class DeepSeekProvider(OpenAICompatibleProvider):
    base_url = "https://api.deepseek.com"
    provider_name = "deepseek"
    supports_tools_flag = True

    def default_model(self):
        return "deepseek-v4"
