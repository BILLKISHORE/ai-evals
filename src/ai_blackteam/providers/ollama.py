import time
import ollama as ollama_sdk
from ai_blackteam.registry import register_provider
from ai_blackteam.providers.base import (
    BaseProvider,
    PromptResult,
    split_reasoning_tags,
)
from ai_blackteam.retry import retry_with_backoff


@register_provider("ollama")
class OllamaProvider(BaseProvider):
    def __init__(self, model=None, api_key=None, base_url=None):
        super().__init__(model, api_key)
        self.base_url = base_url or "http://localhost:11434"
        self._client = ollama_sdk.Client(host=self.base_url)

    def default_model(self):
        return "llama4"


    def _result(self, r, ms):
        """Build a PromptResult, pulling the reasoning trace out either way.

        Newer ollama returns the trace on a `thinking` field. The models emit
        it inline as <think>...</think> when that field is absent. Ollama folds
        reasoning tokens into its total eval count, so no separate
        reasoning_tokens is reported here rather than a fabricated one.
        """
        message = r["message"]
        content = message.get("content", "")
        thinking = message.get("thinking")
        if thinking:
            answer, reasoning = content, thinking
        else:
            answer, reasoning = split_reasoning_tags(content)
        return PromptResult(response=answer, model=self.model,
                            provider="ollama", latency_ms=ms, reasoning=reasoning)

    def send_prompt(self, prompt, system_prompt=None):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        start = time.time()
        r = retry_with_backoff(lambda: self._client.chat(model=self.model, messages=messages))
        ms = (time.time() - start) * 1000
        return self._result(r, ms)

    def send_in_conversation(self, messages, system_prompt=None):
        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + list(messages)
        start = time.time()
        r = retry_with_backoff(lambda: self._client.chat(model=self.model, messages=messages))
        ms = (time.time() - start) * 1000
        return self._result(r, ms)
