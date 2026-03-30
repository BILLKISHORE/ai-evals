"""Built-in guardrail filter functions for defense testing.

Usage:
    from blackteam.guardrails import keyword_filter, regex_filter

    guard = keyword_filter(["bomb", "weapon", "exploit"])
    result = guard("How to make a bomb")  # Returns None (blocked)
    result = guard("Hello world")         # Returns "Hello world" (passed)
"""

import re


def keyword_filter(blocked_words):
    """Block prompts/responses containing any of the specified words."""
    blocked_lower = [w.lower() for w in blocked_words]

    def filter_fn(text):
        lower = text.lower()
        for word in blocked_lower:
            if word in lower:
                return None
        return text

    return filter_fn


def regex_filter(patterns):
    """Block prompts/responses matching any of the specified regex patterns."""
    compiled = [re.compile(p, re.IGNORECASE) for p in patterns]

    def filter_fn(text):
        for pattern in compiled:
            if pattern.search(text):
                return None
        return text

    return filter_fn


def combined_filter(*filters):
    """Chain multiple filters. Blocks if any filter returns None."""
    def filter_fn(text):
        for f in filters:
            text = f(text)
            if text is None:
                return None
        return text

    return filter_fn
