from mordor.retry import retry_with_backoff
import pytest


def test_retry_succeeds_first_try():
    result = retry_with_backoff(lambda: 42)
    assert result == 42


def test_retry_succeeds_after_failure():
    attempts = [0]

    def flaky():
        attempts[0] += 1
        if attempts[0] < 3:
            raise ValueError("not yet")
        return "ok"

    result = retry_with_backoff(flaky, max_retries=3, base_delay=0.01)
    assert result == "ok"
    assert attempts[0] == 3


def test_retry_exhausted_raises():
    def always_fail():
        raise ValueError("always fails")

    with pytest.raises(ValueError, match="always fails"):
        retry_with_backoff(always_fail, max_retries=2, base_delay=0.01)


def test_retry_only_catches_specified_exceptions():
    def type_error():
        raise TypeError("wrong type")

    with pytest.raises(TypeError):
        retry_with_backoff(type_error, max_retries=2, base_delay=0.01,
                           retryable_exceptions=(ValueError,))
