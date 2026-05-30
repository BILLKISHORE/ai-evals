from ai_blackteam.registry import register_provider
from ai_blackteam.providers.base import OpenAICompatibleProvider


@register_provider("grok")
class GrokProvider(OpenAICompatibleProvider):
    base_url = "https://api.x.ai/v1"
    provider_name = "grok"
    supports_tools_flag = True

    def default_model(self):
        return "grok-4.3"
