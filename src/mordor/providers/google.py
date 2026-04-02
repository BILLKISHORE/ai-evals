import time
from google import genai
from mordor.registry import register_provider
from mordor.providers.base import BaseProvider, PromptResult
from mordor.retry import retry_with_backoff


@register_provider("google")
class GoogleProvider(BaseProvider):
    def __init__(self, model=None, api_key=None):
        super().__init__(model, api_key)
        self._client = genai.Client(api_key=self.api_key) if self.api_key else genai.Client()

    def default_model(self):
        return "gemini-3.1-pro"

    def send_prompt(self, prompt, system_prompt=None):
        config = {}
        if system_prompt:
            config["system_instruction"] = system_prompt

        start = time.time()
        r = retry_with_backoff(lambda: self._client.models.generate_content(model=self.model, contents=prompt, config=config))
        ms = (time.time() - start) * 1000

        return PromptResult(
            response=r.text or "",
            model=self.model, provider="google",
            tokens_in=r.usage_metadata.prompt_token_count if r.usage_metadata else None,
            tokens_out=r.usage_metadata.candidates_token_count if r.usage_metadata else None,
            latency_ms=ms,
        )

    def send_in_conversation(self, messages, system_prompt=None):
        config = {}
        if system_prompt:
            config["system_instruction"] = system_prompt

        contents = []
        for msg in messages:
            role = "model" if msg["role"] == "assistant" else "user"
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})

        start = time.time()
        r = retry_with_backoff(lambda: self._client.models.generate_content(model=self.model, contents=contents, config=config))
        ms = (time.time() - start) * 1000

        return PromptResult(
            response=r.text or "",
            model=self.model, provider="google",
            tokens_in=r.usage_metadata.prompt_token_count if r.usage_metadata else None,
            tokens_out=r.usage_metadata.candidates_token_count if r.usage_metadata else None,
            latency_ms=ms,
        )
