"""Gemini requests, including the thinking knob the other providers already had.

Reasoning effort reaches a provider as a constructor keyword, so a provider
that does not accept it turns `--effort` into a TypeError for that vendor
alone. Google was that vendor. A sweep comparing the same attack across
vendors at the same thinking depth had to leave Gemini out, and nothing in the
output said why.

Google's knob is a thinking_config nested inside the generation config rather
than an effort string, and it is only valid on a model that has a thinking
stage. Sending it to one that does not is a 400, so the mapping is resolved
once at construction and the request carries it only when it was asked for.
"""

import time
from google import genai
from ai_blackteam.reasoning import GOOGLE_VENDOR, google_thinking_config, validate_effort
from ai_blackteam.registry import register_provider
from ai_blackteam.providers.base import (
    BaseProvider,
    PromptResult,
    read_reasoning_tokens,
)
from ai_blackteam.retry import retry_with_backoff



def _thought_text(response):
    """The model's thinking, or None when it returned none.

    Gemini does not separate the trace into its own field. Thought parts sit
    among the ordinary content parts, distinguished only by a `thought` flag,
    and `response.text` concatenates the non-thought parts. Anything that
    reads parts positionally picks up whichever came first.

    None rather than "" when there is no trace: an empty string would read as
    a model that thought about nothing, which is a different claim from a
    model whose thinking was never returned.
    """
    chunks = []
    for candidate in getattr(response, "candidates", None) or []:
        content = getattr(candidate, "content", None)
        for part in getattr(content, "parts", None) or []:
            if getattr(part, "thought", False) and getattr(part, "text", None):
                chunks.append(part.text)
    return "".join(chunks) or None


@register_provider("google")
class GoogleProvider(BaseProvider):
    def __init__(self, model=None, api_key=None, effort=None):
        super().__init__(model, api_key)
        self.effort = validate_effort(effort, model=self.model, vendor=GOOGLE_VENDOR)
        # Resolved here rather than per request so a model that cannot think
        # fails immediately instead of a hundred prompts into a sweep.
        self._thinking_config = google_thinking_config(self.effort, model=self.model)
        self._client = genai.Client(api_key=self.api_key) if self.api_key else genai.Client()

    def default_model(self):
        return "gemini-3.5-flash"

    def _build_config(self, system_prompt=None):
        """The generation config for one request.

        The thinking block is copied rather than shared: a config handed out
        twice lets one request edit another's settings.
        """
        config = {}
        if system_prompt:
            config["system_instruction"] = system_prompt
        if self._thinking_config:
            config["thinking_config"] = dict(self._thinking_config)
        return config

    def _result(self, r, ms):
        usage = getattr(r, "usage_metadata", None)
        return PromptResult(
            response=r.text or "",
            model=self.model, provider="google",
            tokens_in=usage.prompt_token_count if usage else None,
            tokens_out=usage.candidates_token_count if usage else None,
            latency_ms=ms,
            reasoning=_thought_text(r),
            reasoning_tokens=read_reasoning_tokens(usage),
        )

    def send_prompt(self, prompt, system_prompt=None):
        config = self._build_config(system_prompt)

        start = time.time()
        r = retry_with_backoff(lambda: self._client.models.generate_content(model=self.model, contents=prompt, config=config))
        ms = (time.time() - start) * 1000

        return self._result(r, ms)

    def send_in_conversation(self, messages, system_prompt=None):
        config = self._build_config(system_prompt)

        contents = []
        for msg in messages:
            role = "model" if msg["role"] == "assistant" else "user"
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})

        start = time.time()
        r = retry_with_backoff(lambda: self._client.models.generate_content(model=self.model, contents=contents, config=config))
        ms = (time.time() - start) * 1000

        return self._result(r, ms)
