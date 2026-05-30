from ai_blackteam.registry import register_provider
from ai_blackteam.providers.base import OpenAICompatibleProvider


@register_provider("groq")
class GroqProvider(OpenAICompatibleProvider):
    base_url = "https://api.groq.com/openai/v1"
    provider_name = "groq"
    supports_tools_flag = True

    def default_model(self):
        return "llama-3.3-70b-versatile"
