import time
from huggingface_hub import InferenceClient
from ai_blackteam.registry import register_provider
from ai_blackteam.providers.base import BaseProvider, PromptResult, read_openai_reasoning, read_reasoning_tokens, split_reasoning_tags
from ai_blackteam.providers.base import read_openai_message
from ai_blackteam.retry import retry_with_backoff


@register_provider("huggingface")
class HuggingFaceProvider(BaseProvider):
    def __init__(self, model=None, api_key=None):
        super().__init__(model, api_key)
        self._client = InferenceClient(token=self.api_key) if self.api_key else InferenceClient()

    def default_model(self):
        return "meta-llama/Llama-4-Scout-17B-16E-Instruct"

    def send_prompt(self, prompt, system_prompt=None):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        start = time.time()
        r = retry_with_backoff(lambda: self._client.chat_completion(messages=messages, model=self.model, max_tokens=4096))
        ms = (time.time() - start) * 1000

        choice = r.choices[0]
        text, refused = read_openai_message(choice.message)
        # HF serves deepseek-r1 and QwQ, which return the trace on a
        # reasoning_content field or inline as <think>. Try the field, then
        # split inline tags off the answer.
        reasoning = read_openai_reasoning(choice.message)
        if reasoning is None:
            text, reasoning = split_reasoning_tags(text)
        return PromptResult(
            response=text, model=self.model, provider="huggingface",
            tokens_in=r.usage.prompt_tokens if r.usage else None,
            tokens_out=r.usage.completion_tokens if r.usage else None,
            latency_ms=ms,
            reasoning=reasoning,
            reasoning_tokens=read_reasoning_tokens(r.usage),
            # A structured refusal is the vendor saying so outright, which
            # is stronger than whatever finish_reason carries.
            stop_reason="refusal" if refused else getattr(choice, "finish_reason", None),
        )

    def send_in_conversation(self, messages, system_prompt=None):
        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + list(messages)
        start = time.time()
        r = retry_with_backoff(lambda: self._client.chat_completion(messages=messages, model=self.model, max_tokens=4096))
        ms = (time.time() - start) * 1000

        choice = r.choices[0]
        text, refused = read_openai_message(choice.message)
        # HF serves deepseek-r1 and QwQ, which return the trace on a
        # reasoning_content field or inline as <think>. Try the field, then
        # split inline tags off the answer.
        reasoning = read_openai_reasoning(choice.message)
        if reasoning is None:
            text, reasoning = split_reasoning_tags(text)
        return PromptResult(
            response=text, model=self.model, provider="huggingface",
            tokens_in=r.usage.prompt_tokens if r.usage else None,
            tokens_out=r.usage.completion_tokens if r.usage else None,
            latency_ms=ms,
            reasoning=reasoning,
            reasoning_tokens=read_reasoning_tokens(r.usage),
            # A structured refusal is the vendor saying so outright, which
            # is stronger than whatever finish_reason carries.
            stop_reason="refusal" if refused else getattr(choice, "finish_reason", None),
        )
