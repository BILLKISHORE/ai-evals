import json
import os
import time

import httpx

from ai_blackteam.registry import register_provider
from ai_blackteam.providers.base import BaseProvider, PromptResult
from ai_blackteam.retry import retry_with_backoff

PROMPT_PLACEHOLDER = "{{prompt}}"


def _resolve_path(data, path):
    """Extract a value from nested dict/list via a dot path.

    Supports dict keys and integer list indices, e.g.
    "choices.0.message.content".
    """
    current = data
    for part in path.split("."):
        if isinstance(current, list):
            current = current[int(part)]
        elif isinstance(current, dict):
            current = current[part]
        else:
            raise KeyError(f"Cannot descend into {type(current).__name__} at '{part}'")
    return current


@register_provider("http")
class HTTPProvider(BaseProvider):
    """Test any HTTP endpoint that takes a prompt and returns text.

    Lets users red-team their own deployed app, agent, or RAG endpoint
    instead of a vendor SDK. Configure via constructor args or env vars:

      - endpoint          (AIBT_HTTP_ENDPOINT)        the URL to POST to
      - request_template  (AIBT_HTTP_REQUEST_TEMPLATE) JSON body with {{prompt}}
      - response_path     (AIBT_HTTP_RESPONSE_PATH)    dot path to the output text
      - headers           (AIBT_HTTP_HEADERS)          JSON dict of headers
      - method            (AIBT_HTTP_METHOD)           default POST

    Example request_template:
        {"messages": [{"role": "user", "content": "{{prompt}}"}]}
    Example response_path:
        choices.0.message.content
    """

    def __init__(self, model=None, api_key=None, endpoint=None,
                 request_template=None, response_path=None, headers=None,
                 method=None, timeout=60):
        super().__init__(model, api_key)
        self.endpoint = endpoint or os.environ.get("AIBT_HTTP_ENDPOINT")
        if not self.endpoint:
            raise ValueError(
                "HTTP provider requires an endpoint. Set AIBT_HTTP_ENDPOINT or "
                "pass endpoint= / config providers.http.endpoint"
            )
        self.request_template = (
            request_template
            or os.environ.get("AIBT_HTTP_REQUEST_TEMPLATE")
            or '{"prompt": "{{prompt}}"}'
        )
        self.response_path = (
            response_path or os.environ.get("AIBT_HTTP_RESPONSE_PATH") or "response"
        )
        self.method = (method or os.environ.get("AIBT_HTTP_METHOD") or "POST").upper()
        self.timeout = timeout

        raw_headers = headers or os.environ.get("AIBT_HTTP_HEADERS")
        if isinstance(raw_headers, str):
            raw_headers = json.loads(raw_headers)
        self.headers = raw_headers or {"Content-Type": "application/json"}
        if self.api_key and "Authorization" not in self.headers:
            self.headers["Authorization"] = f"Bearer {self.api_key}"

    def default_model(self):
        return "http-endpoint"

    def _build_body(self, prompt):
        # JSON-escape the prompt so quotes/newlines don't break the template.
        escaped = json.dumps(prompt)[1:-1]
        return self.request_template.replace(PROMPT_PLACEHOLDER, escaped)

    def _call(self, prompt):
        body = self._build_body(prompt)
        start = time.time()

        def _do_request():
            with httpx.Client(timeout=self.timeout) as client:
                resp = client.request(
                    self.method, self.endpoint,
                    content=body.encode("utf-8"), headers=self.headers,
                )
                resp.raise_for_status()
                return resp

        resp = retry_with_backoff(_do_request)
        ms = (time.time() - start) * 1000
        try:
            text = _resolve_path(resp.json(), self.response_path)
        except (KeyError, IndexError, ValueError, json.JSONDecodeError):
            text = resp.text
        return PromptResult(
            response=str(text), model=self.model, provider="http", latency_ms=ms
        )

    def send_prompt(self, prompt, system_prompt=None):
        full = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        return self._call(full)

    def send_in_conversation(self, messages, system_prompt=None):
        # Flatten the conversation into a single prompt for endpoints that
        # accept only one text field.
        parts = []
        if system_prompt:
            parts.append(f"[system] {system_prompt}")
        for m in messages:
            parts.append(f"[{m['role']}] {m['content']}")
        return self._call("\n".join(parts))
