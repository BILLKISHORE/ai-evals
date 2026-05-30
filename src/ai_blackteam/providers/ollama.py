import time
import ollama as ollama_sdk
from ai_blackteam.registry import register_provider
from ai_blackteam.providers.base import BaseProvider, PromptResult
from ai_blackteam.retry import retry_with_backoff


@register_provider("ollama")
class OllamaProvider(BaseProvider):
    def __init__(self, model=None, api_key=None, base_url=None):
        super().__init__(model, api_key)
        self.base_url = base_url or "http://localhost:11434"
        self._client = ollama_sdk.Client(host=self.base_url)

    def default_model(self):
        return "llama4"

    def send_prompt(self, prompt, system_prompt=None):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        start = time.time()
        r = retry_with_backoff(lambda: self._client.chat(model=self.model, messages=messages))
        ms = (time.time() - start) * 1000

        return PromptResult(response=r["message"]["content"], model=self.model,
                            provider="ollama", latency_ms=ms)

    def send_in_conversation(self, messages, system_prompt=None):
        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + list(messages)
        start = time.time()
        r = retry_with_backoff(lambda: self._client.chat(model=self.model, messages=messages))
        ms = (time.time() - start) * 1000
        return PromptResult(response=r["message"]["content"], model=self.model,
                            provider="ollama", latency_ms=ms)
