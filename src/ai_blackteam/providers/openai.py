import time
from openai import OpenAI
from ai_blackteam.registry import register_provider
from ai_blackteam.providers.base import BaseProvider, PromptResult, ToolResult
from ai_blackteam.retry import retry_with_backoff


@register_provider("openai")
class OpenAIProvider(BaseProvider):
    def __init__(self, model=None, api_key=None, user_id=None):
        super().__init__(model, api_key)
        self._client = OpenAI(api_key=self.api_key) if self.api_key else OpenAI()
        self._user_id = user_id or "ai_blackteam-safety-eval"

    def default_model(self):
        return "gpt-5.5"

    def send_prompt(self, prompt, system_prompt=None):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        start = time.time()
        r = retry_with_backoff(lambda: self._client.chat.completions.create(model=self.model, messages=messages, max_completion_tokens=4096, user=self._user_id))
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
        r = retry_with_backoff(lambda: self._client.chat.completions.create(model=self.model, messages=msgs, max_completion_tokens=4096, user=self._user_id))
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
        r = retry_with_backoff(lambda: self._client.chat.completions.create(model=self.model, messages=msgs, tools=oai_tools, max_completion_tokens=4096, user=self._user_id))
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
