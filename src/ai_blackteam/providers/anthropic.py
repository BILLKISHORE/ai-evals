import time
from anthropic import Anthropic
from ai_blackteam.logging_config import get_logger
from ai_blackteam.registry import register_provider
from ai_blackteam.providers.base import BaseProvider, PromptResult, ToolResult
from ai_blackteam.retry import retry_with_backoff

logger = get_logger("provider.anthropic")


def _stop_signal(r):
    """Anthropic reports refusals in-band: stop_reason "refusal" on a normal
    HTTP 200, with stop_details naming the policy category that fired. Older
    SDKs have no stop_details attribute at all, so read both defensively."""
    details = getattr(r, "stop_details", None)
    if details is not None and not isinstance(details, dict):
        details = getattr(details, "model_dump", lambda: None)() or None
    return getattr(r, "stop_reason", None), details



@register_provider("anthropic")
class AnthropicProvider(BaseProvider):
    def __init__(self, model=None, api_key=None):
        super().__init__(model, api_key)
        self._client = Anthropic(api_key=self.api_key) if self.api_key else Anthropic()

    def default_model(self):
        return "claude-sonnet-5"

    def send_prompt(self, prompt, system_prompt=None):
        kwargs = {"model": self.model, "max_tokens": 4096,
                  "messages": [{"role": "user", "content": prompt}]}
        if system_prompt:
            kwargs["system"] = system_prompt

        logger.debug(f"Sending prompt to {self.model} ({len(prompt)} chars)")
        start = time.time()
        try:
            r = retry_with_backoff(lambda: self._client.messages.create(**kwargs))
        except Exception as e:
            logger.error(f"API call failed: {e}")
            raise
        ms = (time.time() - start) * 1000

        text = r.content[0].text if r.content and hasattr(r.content[0], "text") else ""
        logger.debug(f"Response: {len(text)} chars, {r.usage.input_tokens}+{r.usage.output_tokens} tokens, {ms:.0f}ms")
        stop_reason, stop_details = _stop_signal(r)
        return PromptResult(response=text, model=self.model, provider="anthropic",
                            tokens_in=r.usage.input_tokens, tokens_out=r.usage.output_tokens,
                            latency_ms=ms, stop_reason=stop_reason, stop_details=stop_details)

    def send_in_conversation(self, messages, system_prompt=None):
        kwargs = {"model": self.model, "max_tokens": 4096, "messages": messages}
        if system_prompt:
            kwargs["system"] = system_prompt
        logger.debug(f"Sending conversation ({len(messages)} messages) to {self.model}")
        start = time.time()
        try:
            r = retry_with_backoff(lambda: self._client.messages.create(**kwargs))
        except Exception as e:
            logger.error(f"API call failed: {e}")
            raise
        ms = (time.time() - start) * 1000
        text = r.content[0].text if r.content and hasattr(r.content[0], "text") else ""
        logger.debug(f"Response: {len(text)} chars, {r.usage.input_tokens}+{r.usage.output_tokens} tokens, {ms:.0f}ms")
        stop_reason, stop_details = _stop_signal(r)
        return PromptResult(response=text, model=self.model, provider="anthropic",
                            tokens_in=r.usage.input_tokens, tokens_out=r.usage.output_tokens,
                            latency_ms=ms, stop_reason=stop_reason, stop_details=stop_details)

    def send_with_tools(self, messages, tools, system_prompt=None):
        kwargs = {"model": self.model, "max_tokens": 4096, "messages": messages, "tools": tools}
        if system_prompt:
            kwargs["system"] = system_prompt
        logger.debug(f"Sending tool-use request to {self.model} ({len(tools)} tools)")
        start = time.time()
        try:
            r = retry_with_backoff(lambda: self._client.messages.create(**kwargs))
        except Exception as e:
            logger.error(f"API call failed: {e}")
            raise
        ms = (time.time() - start) * 1000

        text = None
        calls = []
        for block in r.content:
            if hasattr(block, "text"):
                text = block.text
            elif block.type == "tool_use":
                calls.append({"id": block.id, "tool": block.name, "input": block.input})

        stop_reason, stop_details = _stop_signal(r)
        return ToolResult(response=text, tool_calls=calls, model=self.model,
                          provider="anthropic", tokens_in=r.usage.input_tokens,
                          tokens_out=r.usage.output_tokens, latency_ms=ms,
                          stop_reason=stop_reason, stop_details=stop_details)

    def supports_tools(self):
        return True
