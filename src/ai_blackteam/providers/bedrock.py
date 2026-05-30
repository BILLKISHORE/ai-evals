import time
from ai_blackteam.registry import register_provider
from ai_blackteam.providers.base import BaseProvider, PromptResult
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
        return "anthropic.claude-3-5-sonnet-20241022-v2:0"

    def _converse(self, messages, system_prompt):
        kwargs = {
            "modelId": self.model,
            "messages": messages,
            "inferenceConfig": {"maxTokens": 4096},
        }
        if system_prompt:
            kwargs["system"] = [{"text": system_prompt}]
        start = time.time()
        r = retry_with_backoff(lambda: self._client.converse(**kwargs))
        ms = (time.time() - start) * 1000
        text = r["output"]["message"]["content"][0]["text"]
        usage = r.get("usage", {})
        return PromptResult(
            response=text,
            model=self.model,
            provider="bedrock",
            tokens_in=usage.get("inputTokens"),
            tokens_out=usage.get("outputTokens"),
            latency_ms=ms,
        )

    def send_prompt(self, prompt, system_prompt=None):
        messages = [{"role": "user", "content": [{"text": prompt}]}]
        return self._converse(messages, system_prompt)

    def send_in_conversation(self, messages, system_prompt=None):
        bedrock_messages = [
            {"role": m["role"], "content": [{"text": m["content"]}]} for m in messages
        ]
        return self._converse(bedrock_messages, system_prompt)
