import logging
import random
import time

logger = logging.getLogger("ai_blackteam.retry")

# Stdlib transport failures. TimeoutError and ConnectionError are both OSError
# subclasses, so OSError alone covers socket resets, refused connects and
# read timeouts.
_TRANSIENT_TYPES = (OSError,)

# Provider SDK errors cannot be caught by type: importing anthropic/openai/
# google here would make a paid SDK a hard import of every run. Their transport
# failures are recognised by class name instead.
_TRANSIENT_NAME_HINTS = (
    "timeout",
    "connection",
    "connect",
    "unavailable",
    "overloaded",
    "ratelimit",
    "toomanyrequests",
    "remoteprotocol",
    "readerror",
    "writeerror",
    "poolerror",
    "servererror",
    "internalserver",
)

# Full delay would put every parallel worker back on the wire at the same
# instant; the async batch runner defaults to 5 of them.
_JITTER_FLOOR = 0.5


def retry_with_backoff(fn, max_retries=3, base_delay=1.0, max_delay=30.0, retryable_exceptions=None):
    """Call fn() with jittered exponential backoff on transient failures.

    Args:
        fn: callable to execute
        max_retries: maximum number of retry attempts
        base_delay: initial delay in seconds
        max_delay: maximum delay between retries
        retryable_exceptions: tuple of exception types to retry on. None means
            retry only transient failures: transport errors, HTTP 429 and 5xx.
            A 4xx other than 429 is the caller's bug and is raised immediately.

    Returns:
        Result of fn()

    Raises:
        Last exception if all retries exhausted, or the first non-retryable one
    """
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as e:
            if not _should_retry(e, retryable_exceptions):
                raise
            last_error = e
            if attempt == max_retries:
                logger.error(f"All {max_retries} retries exhausted: {e}")
                raise
            delay = _next_delay(e, attempt, base_delay, max_delay)
            logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.1f}s...")
            time.sleep(delay)
    raise last_error


def _should_retry(exc, retryable_exceptions):
    if retryable_exceptions is not None:
        return isinstance(exc, retryable_exceptions)

    status = _status_code(exc)
    if status is not None:
        # A status code is stronger evidence than the class name: an SDK error
        # named ConnectionTimeoutError carrying a 400 is still a bad request.
        return status == 429 or status >= 500

    if isinstance(exc, _TRANSIENT_TYPES):
        return True

    name = type(exc).__name__.lower()
    return any(hint in name for hint in _TRANSIENT_NAME_HINTS)


def _status_code(exc):
    status = getattr(exc, "status_code", None)
    if status is None:
        status = getattr(getattr(exc, "response", None), "status_code", None)
    try:
        return int(status)
    except (TypeError, ValueError):
        return None


def _next_delay(exc, attempt, base_delay, max_delay):
    retry_after = _retry_after_seconds(exc)
    if retry_after is not None:
        return min(retry_after, max_delay)
    delay = min(base_delay * (2 ** attempt), max_delay)
    return delay * random.uniform(_JITTER_FLOOR, 1.0)


def _retry_after_seconds(exc):
    """Seconds from a Retry-After header, or None to fall back to backoff."""
    headers = getattr(getattr(exc, "response", None), "headers", None)
    if headers is None:
        return None
    try:
        raw = headers.get("Retry-After")
        if raw is None:
            raw = headers.get("retry-after")
    except (AttributeError, TypeError):
        return None
    try:
        seconds = float(raw)
    except (TypeError, ValueError):
        # The HTTP-date form is valid but not worth parsing: backoff covers it.
        return None
    return seconds if seconds >= 0 else None
