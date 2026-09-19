"""Guardrail provider wrapper for defense testing.

Wraps any provider with input/output filters to test guardrail effectiveness.

Usage:
    from ai_blackteam.providers.guardrail import GuardrailProvider
    from ai_blackteam.guardrails import keyword_filter

    base = AnthropicProvider(model="claude-sonnet-5")
    guarded = GuardrailProvider(
        base_provider=base,
        input_filter=keyword_filter(["bomb", "weapon"]),
    )

    # Now run attacks against the guarded provider
    engine.run(guarded, attack, target)
"""

from ai_blackteam.providers.base import BaseProvider, PromptResult, ToolResult


class GuardrailProvider(BaseProvider):
    """Provider wrapper that applies guardrail filters before/after the base provider."""

    def __init__(self, base_provider, input_filter=None, output_filter=None):
        super().__init__(model=base_provider.model, api_key=base_provider.api_key)
        self.base = base_provider
        self.input_filter = input_filter
        self.output_filter = output_filter

    def default_model(self):
        return self.base.default_model()

    def _check_input(self, text):
        if self.input_filter:
            result = self.input_filter(text)
            if result is None:
                return None
        return text

    def _check_output(self, result):
        if self.output_filter and result.response:
            filtered = self.output_filter(result.response)
            if filtered is None:
                return PromptResult(
                    response="[BLOCKED BY GUARDRAIL]",
                    model=result.model, provider=result.provider,
                    tokens_in=result.tokens_in, tokens_out=result.tokens_out,
                    latency_ms=result.latency_ms,
                )
        return result

    def send_prompt(self, prompt, system_prompt=None):
        if self._check_input(prompt) is None:
            return PromptResult(
                response="[BLOCKED BY GUARDRAIL]",
                model=self.model, provider="guardrail",
            )
        result = self.base.send_prompt(prompt, system_prompt=system_prompt)
        return self._check_output(result)

    def send_in_conversation(self, messages, system_prompt=None):
        last_msg = messages[-1] if messages else {}
        content = last_msg.get("content", "")
        if isinstance(content, str) and self._check_input(content) is None:
            return PromptResult(
                response="[BLOCKED BY GUARDRAIL]",
                model=self.model, provider="guardrail",
            )
        result = self.base.send_in_conversation(messages, system_prompt=system_prompt)
        return self._check_output(result)

    def send_with_tools(self, messages, tools, system_prompt=None):
        last_msg = messages[-1] if messages else {}
        content = last_msg.get("content", "")
        if isinstance(content, str) and self._check_input(content) is None:
            return ToolResult(
                response="[BLOCKED BY GUARDRAIL]",
                tool_calls=[], model=self.model, provider="guardrail",
            )
        return self.base.send_with_tools(messages, tools, system_prompt=system_prompt)

    def supports_tools(self):
        return self.base.supports_tools()

    def get_model_info(self):
        info = self.base.get_model_info()
        info["provider"] = f"guardrail({info.get('provider', '')})"
        return info
