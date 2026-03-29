import time
from huggingface_hub import InferenceClient
from blackteam.registry import register_provider
from blackteam.providers.base import BaseProvider, PromptResult


@register_provider("huggingface")
class HuggingFaceProvider(BaseProvider):
    def __init__(self, model=None, api_key=None):
        super().__init__(model, api_key)
        self._client = InferenceClient(token=self.api_key) if self.api_key else InferenceClient()

    def default_model(self):
        return "meta-llama/Llama-3.2-3B-Instruct"

    def send_prompt(self, prompt, system_prompt=None):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        start = time.time()
        r = self._client.chat_completion(messages=messages, model=self.model, max_tokens=4096)
        ms = (time.time() - start) * 1000

        text = r.choices[0].message.content or ""
        return PromptResult(
            response=text, model=self.model, provider="huggingface",
            tokens_in=r.usage.prompt_tokens if r.usage else None,
            tokens_out=r.usage.completion_tokens if r.usage else None,
            latency_ms=ms,
        )

    def send_in_conversation(self, messages):
        start = time.time()
        r = self._client.chat_completion(messages=messages, model=self.model, max_tokens=4096)
        ms = (time.time() - start) * 1000

        text = r.choices[0].message.content or ""
        return PromptResult(
            response=text, model=self.model, provider="huggingface",
            tokens_in=r.usage.prompt_tokens if r.usage else None,
            tokens_out=r.usage.completion_tokens if r.usage else None,
            latency_ms=ms,
        )
