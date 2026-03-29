"""Anthropic Claude provider."""

import os
import time

from anthropic import Anthropic

from .base import BaseProvider, PromptResult


class AnthropicProvider(BaseProvider):

    def __init__(self, model: str | None = None):
        self._client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        super().__init__(model)

    def default_model(self) -> str:
        return "claude-sonnet-4-20250514"

    def send_prompt(self, prompt: str, system_prompt: str | None = None) -> PromptResult:
        kwargs = {
            "model": self.model,
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            kwargs["system"] = system_prompt

        start = time.time()
        response = self._client.messages.create(**kwargs)
        latency = (time.time() - start) * 1000

        return PromptResult(
            response=response.content[0].text,
            model=self.model,
            provider="anthropic",
            tokens_in=response.usage.input_tokens,
            tokens_out=response.usage.output_tokens,
            latency_ms=latency,
            raw=response.model_dump(),
        )

    def get_model_info(self) -> dict:
        return {
            "name": self.model,
            "provider": "anthropic",
            "context_window": "200k",
        }
