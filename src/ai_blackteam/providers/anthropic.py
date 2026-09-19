import time
from anthropic import Anthropic
from ai_blackteam.logging_config import get_logger
from ai_blackteam.registry import register_provider
from ai_blackteam.providers.base import BaseProvider, PromptResult, ToolResult
from ai_blackteam.retry import retry_with_backoff

logger = get_logger("provider.anthropic")


def _parse_content(blocks):
    """Split a response into (answer_text, reasoning_trace).

    Reading ``content[0].text`` assumed the answer is the first block. When a
    model thinks, block 0 is a thinking block, which has ``.thinking`` and no
    ``.text``, so the answer came back as an empty string and nothing raised.
    Every block is walked instead, and text blocks are joined rather than
    truncated to the first one.
    """
    answer, thoughts = [], []
    for block in blocks or []:
        btype = getattr(block, "type", None)
        if btype == "thinking":
            thoughts.append(getattr(block, "thinking", "") or "")
        elif btype == "redacted_thinking":
            # The content is encrypted, but the fact that the model thought is
            # itself signal worth keeping.
            thoughts.append("[redacted thinking]")
        elif btype == "text" or (btype is None and hasattr(block, "text")):
            answer.append(getattr(block, "text", "") or "")
    reasoning = "\n".join(t for t in thoughts if t) or None
    return "".join(answer), reasoning



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
    def __init__(self, model=None, api_key=None, effort=None):
        super().__init__(model, api_key)
        from ai_blackteam.reasoning import validate_effort

        self.effort = validate_effort(effort, model=self.model, vendor="the Claude API")
        self._client = Anthropic(api_key=self.api_key) if self.api_key else Anthropic()

    def _with_effort(self, kwargs):
        """Attach output_config only when an effort level was requested.

        Omitting the parameter is not the same as sending "high": the default
        varies by model, and sending it to a model that does not accept it is
        a 400.
        """
        if self.effort:
            kwargs["output_config"] = {"effort": self.effort}
        return kwargs

    def default_model(self):
        return "claude-sonnet-5"

    def send_prompt(self, prompt, system_prompt=None):
        kwargs = {"model": self.model, "max_tokens": 4096,
                  "messages": [{"role": "user", "content": prompt}]}
        if system_prompt:
            kwargs["system"] = system_prompt

        kwargs = self._with_effort(kwargs)
        logger.debug(f"Sending prompt to {self.model} ({len(prompt)} chars)")
        start = time.time()
        try:
            r = retry_with_backoff(lambda: self._client.messages.create(**kwargs))
        except Exception as e:
            logger.error(f"API call failed: {e}")
            raise
        ms = (time.time() - start) * 1000

        text, reasoning = _parse_content(r.content)
        logger.debug(f"Response: {len(text)} chars, {r.usage.input_tokens}+{r.usage.output_tokens} tokens, {ms:.0f}ms")
        stop_reason, stop_details = _stop_signal(r)
        return PromptResult(response=text, model=self.model, provider="anthropic",
                            tokens_in=r.usage.input_tokens, tokens_out=r.usage.output_tokens,
                            latency_ms=ms, stop_reason=stop_reason, stop_details=stop_details,
                            reasoning=reasoning)

    def send_in_conversation(self, messages, system_prompt=None):
        kwargs = {"model": self.model, "max_tokens": 4096, "messages": messages}
        if system_prompt:
            kwargs["system"] = system_prompt
        kwargs = self._with_effort(kwargs)
        logger.debug(f"Sending conversation ({len(messages)} messages) to {self.model}")
        start = time.time()
        try:
            r = retry_with_backoff(lambda: self._client.messages.create(**kwargs))
        except Exception as e:
            logger.error(f"API call failed: {e}")
            raise
        ms = (time.time() - start) * 1000
        text, reasoning = _parse_content(r.content)
        logger.debug(f"Response: {len(text)} chars, {r.usage.input_tokens}+{r.usage.output_tokens} tokens, {ms:.0f}ms")
        stop_reason, stop_details = _stop_signal(r)
        return PromptResult(response=text, model=self.model, provider="anthropic",
                            tokens_in=r.usage.input_tokens, tokens_out=r.usage.output_tokens,
                            latency_ms=ms, stop_reason=stop_reason, stop_details=stop_details,
                            reasoning=reasoning)

    def send_with_tools(self, messages, tools, system_prompt=None):
        kwargs = {"model": self.model, "max_tokens": 4096, "messages": messages, "tools": tools}
        if system_prompt:
            kwargs["system"] = system_prompt
        kwargs = self._with_effort(kwargs)
        logger.debug(f"Sending tool-use request to {self.model} ({len(tools)} tools)")
        start = time.time()
        try:
            r = retry_with_backoff(lambda: self._client.messages.create(**kwargs))
        except Exception as e:
            logger.error(f"API call failed: {e}")
            raise
        ms = (time.time() - start) * 1000

        # Same block-walking as the text paths: a thinking block has no .text,
        # and hasattr(block, "text") was also true for nothing else useful.
        text, reasoning = _parse_content(r.content)
        text = text or None
        calls = [
            {"id": b.id, "tool": b.name, "input": b.input}
            for b in (r.content or []) if getattr(b, "type", None) == "tool_use"
        ]

        stop_reason, stop_details = _stop_signal(r)
        return ToolResult(response=text, tool_calls=calls, model=self.model,
                          provider="anthropic", tokens_in=r.usage.input_tokens,
                          tokens_out=r.usage.output_tokens, latency_ms=ms,
                          stop_reason=stop_reason, stop_details=stop_details,
                          reasoning=reasoning)

    def supports_tools(self):
        return True
