import time
from ai_blackteam.registry import register_provider
from ai_blackteam.providers.base import BaseProvider, PromptResult, ToolResult
from ai_blackteam.retry import retry_with_backoff


@register_provider("bedrock")
class BedrockProvider(BaseProvider):
    """Amazon Bedrock provider using the unified Converse API.

    Auth uses standard AWS credential chain (env vars, ~/.aws/credentials, IAM role).
    Pass `region` via constructor or set AWS_REGION env var.
    """

    def __init__(self, model=None, api_key=None, region=None):
        try:
            import boto3
        except ImportError as e:
            raise ImportError(
                "Bedrock provider requires boto3. Install with: pip install 'ai-blackteam[bedrock]'"
            ) from e
        super().__init__(model, api_key)
        self.region = region or "us-east-1"
        self._client = boto3.client("bedrock-runtime", region_name=self.region)

    def default_model(self):
        return "anthropic.claude-sonnet-5"

    def supports_tools(self):
        return True

    def _converse(self, messages, system_prompt, tool_config=None):
        kwargs = {
            "modelId": self.model,
            "messages": messages,
            "inferenceConfig": {"maxTokens": 4096},
        }
        if system_prompt:
            kwargs["system"] = [{"text": system_prompt}]
        if tool_config:
            kwargs["toolConfig"] = tool_config
        start = time.time()
        r = retry_with_backoff(lambda: self._client.converse(**kwargs))
        ms = (time.time() - start) * 1000
        return r, ms

    def _to_prompt_result(self, r, ms):
        # The Converse API returns the reasoning trace as its own content block
        # (reasoningContent) alongside the text block. Bedrock folds reasoning
        # tokens into outputTokens, so no separate count is reported here.
        text = ""
        reasoning = None
        for block in r["output"]["message"]["content"]:
            if "text" in block and not text:
                text = block["text"]
            elif "reasoningContent" in block and reasoning is None:
                rc = block["reasoningContent"].get("reasoningText", {})
                trace = rc.get("text")
                if trace and trace.strip():
                    reasoning = trace
        usage = r.get("usage", {})
        return PromptResult(
            response=text,
            model=self.model,
            provider="bedrock",
            tokens_in=usage.get("inputTokens"),
            tokens_out=usage.get("outputTokens"),
            latency_ms=ms,
            reasoning=reasoning,
        )

    def send_prompt(self, prompt, system_prompt=None):
        messages = [{"role": "user", "content": [{"text": prompt}]}]
        r, ms = self._converse(messages, system_prompt)
        return self._to_prompt_result(r, ms)

    def send_in_conversation(self, messages, system_prompt=None):
        bedrock_messages = [
            {"role": m["role"], "content": [{"text": m["content"]}]} for m in messages
        ]
        r, ms = self._converse(bedrock_messages, system_prompt)
        return self._to_prompt_result(r, ms)

    def send_with_tools(self, messages, tools, system_prompt=None):
        bedrock_messages = [
            {"role": m["role"], "content": [{"text": m["content"]}]} for m in messages
        ]
        tool_config = {
            "tools": [
                {"toolSpec": {
                    "name": t["name"],
                    "description": t.get("description", ""),
                    "inputSchema": {"json": t["input_schema"]},
                }}
                for t in tools
            ]
        }
        r, ms = self._converse(bedrock_messages, system_prompt, tool_config=tool_config)
        text = None
        calls = []
        for block in r["output"]["message"]["content"]:
            if "text" in block:
                text = block["text"]
            elif "toolUse" in block:
                tu = block["toolUse"]
                calls.append({"id": tu["toolUseId"], "tool": tu["name"], "input": tu["input"]})
        usage = r.get("usage", {})
        return ToolResult(
            response=text,
            tool_calls=calls,
            model=self.model,
            provider="bedrock",
            tokens_in=usage.get("inputTokens"),
            tokens_out=usage.get("outputTokens"),
            latency_ms=ms,
        )
