import time
from anthropic import Anthropic
from blackteam.registry import register_provider
from blackteam.providers.base import BaseProvider, PromptResult, ToolResult


@register_provider("anthropic")
class AnthropicProvider(BaseProvider):
    def __init__(self, model=None, api_key=None):
        super().__init__(model, api_key)
        self._client = Anthropic(api_key=self.api_key) if self.api_key else Anthropic()

    def default_model(self):
        return "claude-sonnet-4-6"

    def send_prompt(self, prompt, system_prompt=None):
        kwargs = {"model": self.model, "max_tokens": 4096,
                  "messages": [{"role": "user", "content": prompt}]}
        if system_prompt:
            kwargs["system"] = system_prompt

        start = time.time()
        r = self._client.messages.create(**kwargs)
        ms = (time.time() - start) * 1000

        text = r.content[0].text if r.content and hasattr(r.content[0], "text") else ""
        return PromptResult(response=text, model=self.model, provider="anthropic",
                            tokens_in=r.usage.input_tokens, tokens_out=r.usage.output_tokens,
                            latency_ms=ms)

    def send_in_conversation(self, messages):
        start = time.time()
        r = self._client.messages.create(model=self.model, max_tokens=4096, messages=messages)
        ms = (time.time() - start) * 1000
        text = r.content[0].text if r.content and hasattr(r.content[0], "text") else ""
        return PromptResult(response=text, model=self.model, provider="anthropic",
                            tokens_in=r.usage.input_tokens, tokens_out=r.usage.output_tokens,
                            latency_ms=ms)

    def send_with_tools(self, messages, tools):
        start = time.time()
        r = self._client.messages.create(model=self.model, max_tokens=4096,
                                         messages=messages, tools=tools)
        ms = (time.time() - start) * 1000

        text = None
        calls = []
        for block in r.content:
            if hasattr(block, "text"):
                text = block.text
            elif block.type == "tool_use":
                calls.append({"id": block.id, "tool": block.name, "input": block.input})

        return ToolResult(response=text, tool_calls=calls, model=self.model,
                          provider="anthropic", tokens_in=r.usage.input_tokens,
                          tokens_out=r.usage.output_tokens, latency_ms=ms)

    def supports_tools(self):
        return True
