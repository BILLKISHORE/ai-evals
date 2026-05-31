import json
from unittest.mock import patch

import httpx
import pytest

from ai_blackteam.providers.http import HTTPProvider, _resolve_path


def test_resolve_path_nested_dict_and_list():
    data = {"choices": [{"message": {"content": "HELLO"}}]}
    assert _resolve_path(data, "choices.0.message.content") == "HELLO"


def test_resolve_path_simple_key():
    assert _resolve_path({"response": "ok"}, "response") == "ok"


def test_resolve_path_raises_on_bad_descent():
    with pytest.raises((KeyError, IndexError)):
        _resolve_path({"a": "scalar"}, "a.b")


def test_missing_endpoint_raises():
    with pytest.raises(ValueError, match="requires an endpoint"):
        HTTPProvider(endpoint=None)


def test_default_model():
    p = HTTPProvider(endpoint="http://x/y")
    assert p.default_model() == "http-endpoint"


def test_body_building_escapes_prompt():
    p = HTTPProvider(
        endpoint="http://x/y",
        request_template='{"messages":[{"role":"user","content":"{{prompt}}"}]}',
    )
    body = p._build_body('say "hi"\nnow')
    parsed = json.loads(body)  # must stay valid JSON after escaping
    assert parsed["messages"][0]["content"] == 'say "hi"\nnow'


def test_api_key_becomes_bearer_header():
    p = HTTPProvider(endpoint="http://x/y", api_key="secret")
    assert p.headers["Authorization"] == "Bearer secret"


def test_send_prompt_extracts_response_path():
    p = HTTPProvider(
        endpoint="http://x/y",
        request_template='{"messages":[{"role":"user","content":"{{prompt}}"}]}',
        response_path="choices.0.message.content",
    )
    with patch("httpx.Client") as MockClient:
        inst = MockClient.return_value.__enter__.return_value
        inst.request.return_value = httpx.Response(
            200,
            json={"choices": [{"message": {"content": "refused"}}]},
            request=httpx.Request("POST", "http://x/y"),
        )
        result = p.send_prompt("attack prompt")
    assert result.response == "refused"
    assert result.provider == "http"
    assert result.latency_ms is not None


def test_send_prompt_falls_back_to_raw_text_on_bad_path():
    p = HTTPProvider(
        endpoint="http://x/y",
        request_template='{"q":"{{prompt}}"}',
        response_path="nonexistent.path",
    )
    with patch("httpx.Client") as MockClient:
        inst = MockClient.return_value.__enter__.return_value
        inst.request.return_value = httpx.Response(
            200, text="plain text body",
            request=httpx.Request("POST", "http://x/y"),
        )
        result = p.send_prompt("x")
    assert result.response == "plain text body"


def test_env_var_configuration(monkeypatch):
    monkeypatch.setenv("AIBT_HTTP_ENDPOINT", "http://env/endpoint")
    monkeypatch.setenv("AIBT_HTTP_RESPONSE_PATH", "data.text")
    p = HTTPProvider()
    assert p.endpoint == "http://env/endpoint"
    assert p.response_path == "data.text"
