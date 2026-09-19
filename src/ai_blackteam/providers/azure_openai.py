import os
import time
from ai_blackteam.registry import register_provider
from ai_blackteam.providers.base import BaseProvider, PromptResult, ToolResult
from ai_blackteam.providers.base import read_openai_message
from ai_blackteam.retry import retry_with_backoff


@register_provider("azure")
class AzureOpenAIProvider(BaseProvider):
    """Azure-hosted OpenAI models.

    Requires three values, supplied either via constructor args or env vars:
      - api_key            (AZURE_OPENAI_API_KEY)
      - azure_endpoint     (AZURE_OPENAI_ENDPOINT)        e.g. https://my-resource.openai.azure.com
      - api_version        (AZURE_OPENAI_API_VERSION)     e.g. 2024-10-21

    `model` should be your Azure deployment name (not the underlying model ID).
    """

    def __init__(self, model=None, api_key=None, azure_endpoint=None, api_version=None):
        from openai import AzureOpenAI
        super().__init__(model, api_key)
        self.azure_endpoint = azure_endpoint or os.environ.get("AZURE_OPENAI_ENDPOINT", "")
        self.api_version = api_version or os.environ.get("AZURE_OPENAI_API_VERSION", "2024-10-21")
        self._client = AzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.azure_endpoint,
            api_version=self.api_version,
        )

    def default_model(self):
        return "gpt-5.5"

    def supports_tools(self):
        return True

    def _chat(self, messages, tools=None):
        kwargs = {"model": self.model, "messages": messages, "max_tokens": 4096}
        if tools:
            kwargs["tools"] = tools
        start = time.time()
        r = retry_with_backoff(lambda: self._client.chat.completions.create(**kwargs))
        ms = (time.time() - start) * 1000
        return r, ms

    def send_prompt(self, prompt, system_prompt=None):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        r, ms = self._chat(messages)
        choice = r.choices[0]
        text, refused = read_openai_message(choice.message)
        return PromptResult(
            response=text,
            model=self.model, provider="azure",
            tokens_in=r.usage.prompt_tokens if r.usage else None,
            tokens_out=r.usage.completion_tokens if r.usage else None,
            latency_ms=ms,
            # A structured refusal is the vendor saying so outright, which
            # is stronger than whatever finish_reason carries.
            stop_reason="refusal" if refused else getattr(choice, "finish_reason", None),
        )

    def send_in_conversation(self, messages, system_prompt=None):
        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + list(messages)
        r, ms = self._chat(messages)
        choice = r.choices[0]
        text, refused = read_openai_message(choice.message)
        return PromptResult(
            response=text,
            model=self.model, provider="azure",
            tokens_in=r.usage.prompt_tokens if r.usage else None,
            tokens_out=r.usage.completion_tokens if r.usage else None,
            latency_ms=ms,
            # A structured refusal is the vendor saying so outright, which
            # is stronger than whatever finish_reason carries.
            stop_reason="refusal" if refused else getattr(choice, "finish_reason", None),
        )

    def send_with_tools(self, messages, tools, system_prompt=None):
        import json
        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + list(messages)
        oai_tools = [
            {"type": "function", "function": {
                "name": t["name"],
                "description": t.get("description", ""),
                "parameters": t["input_schema"],
            }}
            for t in tools
        ]
        r, ms = self._chat(messages, tools=oai_tools)
        msg = r.choices[0].message
        calls = []
        if msg.tool_calls:
            for tc in msg.tool_calls:
                calls.append({"id": tc.id, "tool": tc.function.name, "input": json.loads(tc.function.arguments)})
        return ToolResult(
            response=msg.content,
            tool_calls=calls,
            model=self.model, provider="azure",
            tokens_in=r.usage.prompt_tokens if r.usage else None,
            tokens_out=r.usage.completion_tokens if r.usage else None,
            latency_ms=ms,
            # A structured refusal is the vendor saying so outright, which
            # is stronger than whatever finish_reason carries.
            stop_reason="refusal" if refused else getattr(choice, "finish_reason", None),
        )
