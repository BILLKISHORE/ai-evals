import types

import pytest

from ai_blackteam.retry import retry_with_backoff


class _FakeResponse:
    def __init__(self, status_code, headers=None):
        self.status_code = status_code
        self.headers = headers or {}


class _HTTPError(Exception):
    """Stand-in for an SDK error that carries a response, like httpx does."""

    def __init__(self, status_code, headers=None):
        super().__init__(f"HTTP {status_code}")
        self.response = _FakeResponse(status_code, headers)


class _StatusError(Exception):
    """Stand-in for an SDK error that carries status_code directly."""

    def __init__(self, status_code):
        super().__init__(f"HTTP {status_code}")
        self.status_code = status_code


class APIConnectionError(Exception):
    """Named like the paid SDKs' connection error so duck-typing can match it."""


class AuthenticationError(Exception):
    """Named like an SDK auth error that must never be retried."""


@pytest.fixture
def slept(monkeypatch):
    """Collect the delays retry_with_backoff would have slept, instantly."""
    recorded = []
    monkeypatch.setattr("ai_blackteam.retry.time.sleep", recorded.append)
    return recorded


def _counting(exc_factory, succeed_on=None):
    calls = []

    def fn():
        calls.append(len(calls) + 1)
        if succeed_on is not None and len(calls) >= succeed_on:
            return "ok"
        raise exc_factory()

    return fn, calls


# ── Existing behaviour that must keep working ────────────────────────


def test_retry_succeeds_first_try():
    result = retry_with_backoff(lambda: 42)
    assert result == 42


def test_retry_succeeds_after_transient_failure(slept):
    fn, calls = _counting(lambda: ConnectionError("reset by peer"), succeed_on=3)
    assert retry_with_backoff(fn, max_retries=3) == "ok"
    assert len(calls) == 3


def test_retry_exhausted_reraises_last_error(slept):
    def always_fail():
        raise ConnectionError("always fails")

    with pytest.raises(ConnectionError, match="always fails"):
        retry_with_backoff(always_fail, max_retries=2)
    assert len(slept) == 2


def test_retry_only_catches_specified_exceptions(slept):
    def type_error():
        raise TypeError("wrong type")

    with pytest.raises(TypeError):
        retry_with_backoff(type_error, max_retries=2, retryable_exceptions=(ValueError,))
    assert slept == []


def test_explicit_retryable_exceptions_overrides_the_transient_default(slept):
    """Callers that opt into a type keep retrying it even if it is not transient."""
    fn, calls = _counting(lambda: ValueError("nope"), succeed_on=2)
    assert retry_with_backoff(fn, max_retries=3, retryable_exceptions=(ValueError,)) == "ok"
    assert len(calls) == 2


# ── Transient failures retry ─────────────────────────────────────────


def test_429_is_retried(slept):
    fn, calls = _counting(lambda: _StatusError(429), succeed_on=2)
    assert retry_with_backoff(fn, max_retries=3) == "ok"
    assert len(calls) == 2


def test_429_on_a_nested_response_is_retried(slept):
    fn, calls = _counting(lambda: _HTTPError(429), succeed_on=2)
    assert retry_with_backoff(fn, max_retries=3) == "ok"
    assert len(calls) == 2


def test_500_is_retried(slept):
    fn, calls = _counting(lambda: _StatusError(500), succeed_on=3)
    assert retry_with_backoff(fn, max_retries=3) == "ok"
    assert len(calls) == 3


def test_503_is_retried(slept):
    fn, calls = _counting(lambda: _HTTPError(503), succeed_on=2)
    assert retry_with_backoff(fn, max_retries=3) == "ok"
    assert len(calls) == 2


def test_connection_error_is_retried(slept):
    fn, calls = _counting(lambda: ConnectionError("connection reset"), succeed_on=2)
    assert retry_with_backoff(fn, max_retries=3) == "ok"
    assert len(calls) == 2


def test_timeout_error_is_retried(slept):
    fn, calls = _counting(lambda: TimeoutError("read timed out"), succeed_on=2)
    assert retry_with_backoff(fn, max_retries=3) == "ok"
    assert len(calls) == 2


def test_sdk_connection_error_is_retried_by_name(slept):
    """The SDK types are never imported here, so the class name is the signal."""
    fn, calls = _counting(lambda: APIConnectionError("peer closed"), succeed_on=2)
    assert retry_with_backoff(fn, max_retries=3) == "ok"
    assert len(calls) == 2


# ── Permanent failures must not retry (the false-positive guard) ─────


def test_400_is_not_retried(slept):
    fn, calls = _counting(lambda: _StatusError(400))
    with pytest.raises(_StatusError):
        retry_with_backoff(fn, max_retries=3)
    assert len(calls) == 1
    assert slept == []


def test_400_on_a_nested_response_is_not_retried(slept):
    fn, calls = _counting(lambda: _HTTPError(400))
    with pytest.raises(_HTTPError):
        retry_with_backoff(fn, max_retries=3)
    assert len(calls) == 1
    assert slept == []


def test_401_is_not_retried(slept):
    fn, calls = _counting(lambda: _StatusError(401))
    with pytest.raises(_StatusError):
        retry_with_backoff(fn, max_retries=3)
    assert len(calls) == 1


def test_404_is_not_retried(slept):
    fn, calls = _counting(lambda: _StatusError(404))
    with pytest.raises(_StatusError):
        retry_with_backoff(fn, max_retries=3)
    assert len(calls) == 1


def test_422_is_not_retried(slept):
    fn, calls = _counting(lambda: _StatusError(422))
    with pytest.raises(_StatusError):
        retry_with_backoff(fn, max_retries=3)
    assert len(calls) == 1


def test_auth_error_without_status_is_not_retried(slept):
    fn, calls = _counting(lambda: AuthenticationError("bad key"))
    with pytest.raises(AuthenticationError):
        retry_with_backoff(fn, max_retries=3)
    assert len(calls) == 1


def test_plain_value_error_is_not_retried(slept):
    fn, calls = _counting(lambda: ValueError("bad argument"))
    with pytest.raises(ValueError):
        retry_with_backoff(fn, max_retries=3)
    assert len(calls) == 1


def test_a_400_named_like_a_timeout_still_loses_to_its_status(slept):
    """A status code is stronger evidence than a class name."""

    class ConnectionTimeoutError(Exception):
        def __init__(self):
            super().__init__("400")
            self.status_code = 400

    fn, calls = _counting(ConnectionTimeoutError)
    with pytest.raises(ConnectionTimeoutError):
        retry_with_backoff(fn, max_retries=3)
    assert len(calls) == 1


def test_keyboard_interrupt_is_never_swallowed(slept):
    def interrupted():
        raise KeyboardInterrupt()

    with pytest.raises(KeyboardInterrupt):
        retry_with_backoff(interrupted, max_retries=3)
    assert slept == []


# ── Jitter ───────────────────────────────────────────────────────────


def test_jitter_keeps_delays_non_identical(slept):
    def always_fail():
        raise _StatusError(429)

    for _ in range(2):
        with pytest.raises(_StatusError):
            retry_with_backoff(always_fail, max_retries=4, base_delay=1.0)

    first, second = slept[:4], slept[4:]
    assert first != second
    assert len(set(slept)) > 1


def test_jittered_delays_stay_under_the_exponential_ceiling(slept):
    def always_fail():
        raise _StatusError(429)

    with pytest.raises(_StatusError):
        retry_with_backoff(always_fail, max_retries=3, base_delay=1.0, max_delay=30.0)

    ceilings = [1.0, 2.0, 4.0]
    assert len(slept) == 3
    for delay, ceiling in zip(slept, ceilings):
        assert 0 < delay <= ceiling


def test_jitter_respects_max_delay(slept):
    def always_fail():
        raise _StatusError(500)

    with pytest.raises(_StatusError):
        retry_with_backoff(always_fail, max_retries=5, base_delay=10.0, max_delay=2.0)

    assert slept
    assert all(0 < d <= 2.0 for d in slept)


# ── Retry-After ──────────────────────────────────────────────────────


def test_retry_after_header_is_honoured(slept):
    fn, calls = _counting(lambda: _HTTPError(429, {"Retry-After": "7"}), succeed_on=2)
    assert retry_with_backoff(fn, max_retries=3, base_delay=1.0) == "ok"
    assert slept == [7.0]


def test_retry_after_is_case_insensitive(slept):
    fn, calls = _counting(lambda: _HTTPError(429, {"retry-after": "3"}), succeed_on=2)
    assert retry_with_backoff(fn, max_retries=3, base_delay=1.0) == "ok"
    assert slept == [3.0]


def test_retry_after_is_capped_at_max_delay(slept):
    fn, calls = _counting(lambda: _HTTPError(429, {"Retry-After": "600"}), succeed_on=2)
    assert retry_with_backoff(fn, max_retries=3, max_delay=30.0) == "ok"
    assert slept == [30.0]


def test_retry_after_http_date_falls_back_to_backoff(slept):
    """A date-form Retry-After is not seconds, so the backoff schedule wins."""
    header = {"Retry-After": "Wed, 21 Oct 2026 07:28:00 GMT"}
    fn, calls = _counting(lambda: _HTTPError(503, header), succeed_on=2)
    assert retry_with_backoff(fn, max_retries=3, base_delay=1.0) == "ok"
    assert len(slept) == 1
    assert 0 < slept[0] <= 1.0


def test_response_without_headers_does_not_crash(slept):
    exc = types.SimpleNamespace()

    def fn():
        err = _StatusError(429)
        err.response = exc
        raise err

    with pytest.raises(_StatusError):
        retry_with_backoff(fn, max_retries=1, base_delay=1.0)
    assert len(slept) == 1
