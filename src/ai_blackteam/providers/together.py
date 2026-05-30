from ai_blackteam.registry import register_provider
from ai_blackteam.providers.base import OpenAICompatibleProvider


@register_provider("together")
class TogetherProvider(OpenAICompatibleProvider):
    base_url = "https://api.together.xyz/v1"
    provider_name = "together"
    supports_tools_flag = True

    def default_model(self):
        return "meta-llama/Llama-4-Scout-17B-16E-Instruct"
