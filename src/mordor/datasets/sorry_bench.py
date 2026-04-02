import json
import os
import httpx
from mordor.registry import register_dataset
from mordor.datasets.loader import DatasetLoader


@register_dataset("sorry-bench")
class SorryBenchLoader(DatasetLoader):
    name = "sorry-bench"
    license = "CC-BY-4.0"
    source_url = "https://huggingface.co/datasets/sorry-bench/sorry-bench-202406"
    description = "450 unsafe instructions across 45 safety categories (gated, needs HF_TOKEN)"

    RAW_URL = "https://huggingface.co/datasets/sorry-bench/sorry-bench-202406/resolve/main/question.jsonl"

    CATEGORY_MAP = {
        "hate": "hate-speech",
        "harassment": "harassment",
        "violence": "weapons",
        "self-harm": "self-harm",
        "sexual": "sexual-content",
        "terrorism": "radicalization",
        "child_abuse": "child-safety",
        "financial_crime": "fraud",
        "drug": "drugs",
        "weapon": "weapons",
        "cyber": "cybercrime",
        "privacy": "privacy-violation",
        "discrimination": "discrimination",
        "misinformation": "misinformation",
    }

    def _map_category(self, raw_cat):
        lower = raw_cat.lower()
        for key, val in self.CATEGORY_MAP.items():
            if key in lower:
                return val
        return "malware"

    def download(self):
        headers = {}
        hf_token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
        if hf_token:
            headers["Authorization"] = f"Bearer {hf_token}"

        r = httpx.get(self.RAW_URL, timeout=30, follow_redirects=True, headers=headers)
        if r.status_code == 401:
            raise PermissionError(
                "sorry-bench is a gated dataset. Set HF_TOKEN env var after accepting terms at "
                "https://huggingface.co/datasets/sorry-bench/sorry-bench-202406"
            )
        r.raise_for_status()

        items = []
        for line in r.text.strip().split("\n"):
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            prompt = entry.get("turns", [[""]])[0]
            if isinstance(prompt, list):
                prompt = prompt[0] if prompt else ""
            prompt = str(prompt).strip()
            if not prompt:
                continue

            raw_cat = entry.get("category", "")
            items.append({
                "prompt": prompt,
                "category": self._map_category(raw_cat),
                "source": "sorry-bench",
                "difficulty": "medium",
            })

        return items
