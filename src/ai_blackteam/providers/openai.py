import os
import time
from openai import OpenAI
from ai_blackteam.registry import register_provider
from ai_blackteam.providers.base import read_reasoning_tokens, BaseProvider, PromptResult, ToolResult
from ai_blackteam.providers.base import read_openai_message
from ai_blackteam.retry import retry_with_backoff


@register_provider("openai")
class OpenAIProvider(BaseProvider):
    def __init__(self, model=None, api_key=None, user_id=None, base_url=None):
        super().__init__(model, api_key)
        client_kwargs = {}
        if self.api_key:
            client_kwargs["api_key"] = self.api_key
        resolved_base_url = base_url or os.environ.get("OPENAI_BASE_URL")
        if resolved_base_url:
            client_kwargs["base_url"] = resolved_base_url
        self._client = OpenAI(**client_kwargs)
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

        choice = r.choices[0]
        text, refused = read_openai_message(choice.message)
        return PromptResult(
            response=text,
            model=self.model, provider="openai",
            tokens_in=r.usage.prompt_tokens if r.usage else None,
            tokens_out=r.usage.completion_tokens if r.usage else None,
            reasoning_tokens=read_reasoning_tokens(r.usage),
            latency_ms=ms,
            # A structured refusal is the vendor saying so outright, which
            # is stronger than whatever finish_reason carries.
            stop_reason="refusal" if refused else getattr(choice, "finish_reason", None),
        )

    def send_in_conversation(self, messages, system_prompt=None):
        msgs = messages
        if system_prompt:
            msgs = [{"role": "system", "content": system_prompt}] + list(messages)
        start = time.time()
        r = retry_with_backoff(lambda: self._client.chat.completions.create(model=self.model, messages=msgs, max_completion_tokens=4096, user=self._user_id))
        ms = (time.time() - start) * 1000

        choice = r.choices[0]
        text, refused = read_openai_message(choice.message)
        return PromptResult(
            response=text,
            model=self.model, provider="openai",
            tokens_in=r.usage.prompt_tokens if r.usage else None,
            tokens_out=r.usage.completion_tokens if r.usage else None,
            reasoning_tokens=read_reasoning_tokens(r.usage),
            latency_ms=ms,
            # A structured refusal is the vendor saying so outright, which
            # is stronger than whatever finish_reason carries.
            stop_reason="refusal" if refused else getattr(choice, "finish_reason", None),
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
                          tokens_out=r.usage.completion_tokens if r.usage else None,
                          reasoning_tokens=read_reasoning_tokens(r.usage), latency_ms=ms)

    def supports_tools(self):
        return True
