import time
import logging

logger = logging.getLogger("blackteam.retry")


def retry_with_backoff(fn, max_retries=3, base_delay=1.0, max_delay=30.0, retryable_exceptions=None):
    """Call fn() with exponential backoff retry.

    Args:
        fn: callable to execute
        max_retries: maximum number of retry attempts
        base_delay: initial delay in seconds
        max_delay: maximum delay between retries
        retryable_exceptions: tuple of exception types to retry on (None = retry all)

    Returns:
        Result of fn()

    Raises:
        Last exception if all retries exhausted
    """
    if retryable_exceptions is None:
        retryable_exceptions = (Exception,)

    last_error = None
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except retryable_exceptions as e:
            last_error = e
            if attempt == max_retries:
                logger.error(f"All {max_retries} retries exhausted: {e}")
                raise
            delay = min(base_delay * (2 ** attempt), max_delay)
            logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.1f}s...")
            time.sleep(delay)
    raise last_error
