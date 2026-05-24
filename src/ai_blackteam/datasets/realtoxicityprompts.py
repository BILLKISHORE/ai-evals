import os
from ai_blackteam.registry import register_dataset
from ai_blackteam.datasets.loader import DatasetLoader, fetch_with_backoff


@register_dataset("realtoxicityprompts")
class RealToxicityPromptsLoader(DatasetLoader):
    """RealToxicityPrompts (Gehman et al., 2020).

    Source dataset has ~100k prompts. This loader filters client-side to the
    high-toxicity subset (toxicity > TOXICITY_THRESHOLD) to keep memory
    manageable while retaining the prompts most useful for safety evaluation.
    """

    name = "realtoxicityprompts"
    license = "Apache-2.0"
    source_url = "https://huggingface.co/datasets/allenai/real-toxicity-prompts"
    description = "~10K high-toxicity prompts filtered from RealToxicityPrompts (Gehman et al., 2020)"

    TOXICITY_THRESHOLD = 0.5
    ROWS_API = (
        "https://datasets-server.huggingface.co/rows"
        "?dataset=allenai/real-toxicity-prompts&config=default&split=train"
        "&offset={offset}&length={length}"
    )
    PAGE_SIZE = 100

    def _score_to_category(self, prompt_meta):
        if not isinstance(prompt_meta, dict):
            return "harmful-content"
        scores = {
            "hate-speech": prompt_meta.get("identity_attack", 0) or 0,
            "harassment": prompt_meta.get("threat", 0) or 0,
            "sexual-content": prompt_meta.get("sexually_explicit", 0) or 0,
            "harmful-content": prompt_meta.get("toxicity", 0) or 0,
        }
        return max(scores, key=scores.get)

    def download(self):
        headers = {}
        hf_token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
        if hf_token:
            headers["Authorization"] = f"Bearer {hf_token}"

        items = []
        rate_limited = False
        offset = 0
        while True:
            url = self.ROWS_API.format(offset=offset, length=self.PAGE_SIZE)
            r = fetch_with_backoff(url, headers=headers)
            if r.status_code == 429:
                rate_limited = True
                break
            r.raise_for_status()

            data = r.json()
            rows = data.get("rows", [])
            if not rows:
                break

            for entry in rows:
                row = entry.get("row", {})
                prompt_meta = row.get("prompt") or {}
                text = (prompt_meta.get("text") or "").strip()
                if not text:
                    continue
                toxicity = prompt_meta.get("toxicity") or 0.0
                if toxicity < self.TOXICITY_THRESHOLD:
                    continue
                items.append({
                    "prompt": text,
                    "category": self._score_to_category(prompt_meta),
                    "source": "realtoxicityprompts",
                    "difficulty": "easy",
                })

            total = data.get("num_rows_total", 0)
            offset += self.PAGE_SIZE
            if offset >= total:
                break

        if rate_limited:
            import warnings
            warnings.warn(
                f"RealToxicityPrompts rate-limited after {len(items)} records. "
                "Set HF_TOKEN env var for full ingest.",
                stacklevel=2,
            )

        return items
