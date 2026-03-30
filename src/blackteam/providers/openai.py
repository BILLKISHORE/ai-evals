import time
from openai import OpenAI
from blackteam.registry import register_provider
from blackteam.providers.base import BaseProvider, PromptResult, ToolResult


@register_provider("openai")
class OpenAIProvider(BaseProvider):
    def __init__(self, model=None, api_key=None):
        super().__init__(model, api_key)
        self._client = OpenAI(api_key=self.api_key) if self.api_key else OpenAI()

    def default_model(self):
        return "gpt-5.4"

    def send_prompt(self, prompt, system_prompt=None):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        start = time.time()
        r = self._client.chat.completions.create(model=self.model, messages=messages, max_tokens=4096)
        ms = (time.time() - start) * 1000

        return PromptResult(
            response=r.choices[0].message.content or "",
            model=self.model, provider="openai",
            tokens_in=r.usage.prompt_tokens if r.usage else None,
            tokens_out=r.usage.completion_tokens if r.usage else None,
            latency_ms=ms,
        )

    def send_in_conversation(self, messages, system_prompt=None):
        msgs = messages
        if system_prompt:
            msgs = [{"role": "system", "content": system_prompt}] + list(messages)
        start = time.time()
        r = self._client.chat.completions.create(model=self.model, messages=msgs, max_tokens=4096)
        ms = (time.time() - start) * 1000

        return PromptResult(
            response=r.choices[0].message.content or "",
            model=self.model, provider="openai",
            tokens_in=r.usage.prompt_tokens if r.usage else None,
            tokens_out=r.usage.completion_tokens if r.usage else None,
            latency_ms=ms,
        )

    def send_with_tools(self, messages, tools, system_prompt=None):
        oai_tools = [{"type": "function", "function": {"name": t["name"], "description": t.get("description", ""), "parameters": t["input_schema"]}} for t in tools]
        msgs = messages
        if system_prompt:
            msgs = [{"role": "system", "content": system_prompt}] + list(messages)

        start = time.time()
        r = self._client.chat.completions.create(model=self.model, messages=msgs, tools=oai_tools, max_tokens=4096)
        ms = (time.time() - start) * 1000

        msg = r.choices[0].message
        text = msg.content
        calls = []
        if msg.tool_calls:
            import json
            for tc in msg.tool_calls:
                calls.append({"id": tc.id, "tool": tc.function.name, "input": json.loads(tc.function.arguments)})

        return ToolResult(response=text, tool_calls=calls, model=self.model, provider="openai",
                          tokens_in=r.usage.prompt_tokens if r.usage else None,
                          tokens_out=r.usage.completion_tokens if r.usage else None, latency_ms=ms)

    def supports_tools(self):
        return True
