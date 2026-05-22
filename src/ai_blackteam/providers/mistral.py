import time
from openai import OpenAI
from ai_blackteam.registry import register_provider
from ai_blackteam.providers.base import BaseProvider, PromptResult
from ai_blackteam.retry import retry_with_backoff


@register_provider("mistral")
class MistralProvider(BaseProvider):
    def __init__(self, model=None, api_key=None):
        super().__init__(model, api_key)
        self._client = OpenAI(api_key=self.api_key, base_url="https://api.mistral.ai/v1")

    def default_model(self):
        return "mistral-large-latest"

    def send_prompt(self, prompt, system_prompt=None):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        start = time.time()
        r = retry_with_backoff(lambda: self._client.chat.completions.create(model=self.model, messages=messages, max_tokens=4096))
        ms = (time.time() - start) * 1000

        return PromptResult(
            response=r.choices[0].message.content or "",
            model=self.model, provider="mistral",
            tokens_in=r.usage.prompt_tokens if r.usage else None,
            tokens_out=r.usage.completion_tokens if r.usage else None,
            latency_ms=ms,
        )

    def send_in_conversation(self, messages, system_prompt=None):
        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + list(messages)
        start = time.time()
        r = retry_with_backoff(lambda: self._client.chat.completions.create(model=self.model, messages=messages, max_tokens=4096))
        ms = (time.time() - start) * 1000

        return PromptResult(
            response=r.choices[0].message.content or "",
            model=self.model, provider="mistral",
            tokens_in=r.usage.prompt_tokens if r.usage else None,
            tokens_out=r.usage.completion_tokens if r.usage else None,
            latency_ms=ms,
        )
