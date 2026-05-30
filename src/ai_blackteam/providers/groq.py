from ai_blackteam.registry import register_provider
from ai_blackteam.providers.base import OpenAICompatibleProvider


@register_provider("groq")
class GroqProvider(OpenAICompatibleProvider):
    base_url = "https://api.groq.com/openai/v1"
    provider_name = "groq"

    def default_model(self):
        return "llama-3.3-70b-versatile"
