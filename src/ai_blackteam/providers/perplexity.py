"""Perplexity provider, Agent API.

Perplexity retired Sonar Chat Completions on 2026-09-27 in favour of the Agent
API, which follows the Responses shape rather than Chat Completions:

    messages                      -> input (string, or typed message array)
    system message                -> top-level instructions
    max_tokens                    -> max_output_tokens
    choices[0].message.content    -> output_text
    implicit web search           -> explicit tools=[{"type": "web_search"}]

The endpoint is POST /v1/agent, and /v1/responses is accepted as an alias for
OpenAI SDK compatibility. The OpenAI SDK posts to ``{base_url}/responses``, so
``base_url`` must carry the ``/v1`` suffix or the request lands on the wrong
path.
"""

import time

from ai_blackteam.logging_config import get_logger
from ai_blackteam.providers.base import BaseProvider, PromptResult
from ai_blackteam.registry import register_provider
from ai_blackteam.retry import retry_with_backoff

logger = get_logger("provider.perplexity")

DEFAULT_NAMESPACE = "perplexity"
MAX_OUTPUT_TOKENS = 4096


def _qualify_model(model):
    """Namespace a bare model name.

    The Agent API addresses models as ``<vendor>/<model>``. Existing configs
    and the alias registry still hold bare Sonar names, so those are prefixed
    rather than rejected. An already-qualified name passes through, which keeps
    non-Perplexity models reachable (e.g. ``openai/gpt-5.6-sol``).
    """
    if not model or "/" in model:
        return model
    return f"{DEFAULT_NAMESPACE}/{model}"


@register_provider("perplexity")
class PerplexityProvider(BaseProvider):
    base_url = "https://api.perplexity.ai/v1"
    provider_name = "perplexity"

    def __init__(self, model=None, api_key=None, web_search=True):
        from openai import OpenAI
        super().__init__(model, api_key)
        # Sonar always searched the web. Preserved as the default so migrating
        # does not silently change what a run measures; disable it when you
        # need the model's own knowledge without retrieved context.
        self.web_search = web_search
        self._client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def default_model(self):
        return "sonar-pro"

    def send_prompt(self, prompt, system_prompt=None):
        return self._respond(prompt, system_prompt=system_prompt)

    def send_in_conversation(self, messages, system_prompt=None):
        return self._respond(list(messages), system_prompt=system_prompt)

    def _respond(self, input_payload, system_prompt=None):
        kwargs = {
            "model": _qualify_model(self.model),
            "input": input_payload,
            "max_output_tokens": MAX_OUTPUT_TOKENS,
        }
        if system_prompt:
            kwargs["instructions"] = system_prompt
        if self.web_search:
            kwargs["tools"] = [{"type": "web_search"}]

        logger.debug(f"Sending Agent API request to {kwargs['model']}")
        start = time.time()
        try:
            r = retry_with_backoff(lambda: self._client.responses.create(**kwargs))
        except Exception as e:
            logger.error(f"API call failed: {e}")
            raise
        ms = (time.time() - start) * 1000

        usage = getattr(r, "usage", None)
        return PromptResult(
            response=getattr(r, "output_text", "") or "",
            model=self.model,
            provider=self.provider_name,
            tokens_in=getattr(usage, "input_tokens", None) if usage else None,
            tokens_out=getattr(usage, "output_tokens", None) if usage else None,
            latency_ms=ms,
        )

    def supports_tools(self):
        # The Agent API exposes its own tool surface, which does not match the
        # schema the tool-use engine builds. Unchanged from the Sonar provider.
        return False
