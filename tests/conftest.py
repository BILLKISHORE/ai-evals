"""Keep the offline test suite offline.

`evaluator.evaluate()` adds the LLM judge to its method list whenever
ANTHROPIC_API_KEY is present in the environment, and the judge issues a real,
billed request. Five test modules call `evaluate()` with default methods. On a
machine with no key exported the suite is silently offline and green; on a
developer's machine, which is the normal state for someone using this tool,
the same green suite spends money on every run.

That is a cost leak rather than a correctness bug, so nothing fails to reveal
it. The keys are stripped for every test that is not explicitly marked
``live``, which makes the offline suite offline by construction instead of by
luck about the shell it happens to run in.

Tests marked ``live`` keep their environment, because reaching the vendor is
the entire point of those; they are deselected by default via -m "not live".
"""

import pytest

# Every vendor credential the providers read directly from the environment.
# A name absent from the environment is left absent; nothing here adds one.
_VENDOR_KEY_VARS = (
    "ANTHROPIC_API_KEY",
    "OPENAI_API_KEY",
    "AZURE_OPENAI_API_KEY",
    "GOOGLE_API_KEY",
    "GEMINI_API_KEY",
    "MISTRAL_API_KEY",
    "COHERE_API_KEY",
    "GROQ_API_KEY",
    "TOGETHER_API_KEY",
    "DEEPSEEK_API_KEY",
    "PERPLEXITY_API_KEY",
    "XAI_API_KEY",
    "FIREWORKS_API_KEY",
    "OPENROUTER_API_KEY",
    "REPLICATE_API_TOKEN",
    "HF_TOKEN",
    "HUGGINGFACE_API_KEY",
    "AI21_API_KEY",
    "NVIDIA_API_KEY",
    "WRITER_API_KEY",
    "CEREBRAS_API_KEY",
    "SAMBANOVA_API_KEY",
)


@pytest.fixture(autouse=True)
def _no_vendor_credentials(request, monkeypatch):
    """Strip vendor API keys from every non-live test.

    monkeypatch restores the real environment afterwards, so this does not
    disturb the shell or a later live run in the same session.
    """
    if request.node.get_closest_marker("live"):
        return
    for var in _VENDOR_KEY_VARS:
        monkeypatch.delenv(var, raising=False)
