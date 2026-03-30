import time
from openai import OpenAI
from blackteam.registry import register_provider
from blackteam.providers.base import BaseProvider, PromptResult


@register_provider("deepseek")
class DeepSeekProvider(BaseProvider):
    def __init__(self, model=None, api_key=None):
        super().__init__(model, api_key)
        self._client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")

    def default_model(self):
        return "deepseek-v3"

    def send_prompt(self, prompt, system_prompt=None):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        start = time.time()
        r = self._client.chat.completions.create(model=self.model, messages=messages, max_tokens=4096)
        ms = (time.time() - start) * 1000

        return PromptResult(
            response=r.choices[0].message.content or "",
            model=self.model, provider="deepseek",
            tokens_in=r.usage.prompt_tokens if r.usage else None,
            tokens_out=r.usage.completion_tokens if r.usage else None,
            latency_ms=ms,
        )

    def send_in_conversation(self, messages):
        start = time.time()
        r = self._client.chat.completions.create(model=self.model, messages=messages, max_tokens=4096)
        ms = (time.time() - start) * 1000

        return PromptResult(
            response=r.choices[0].message.content or "",
            model=self.model, provider="deepseek",
            tokens_in=r.usage.prompt_tokens if r.usage else None,
            tokens_out=r.usage.completion_tokens if r.usage else None,
            latency_ms=ms,
        )
