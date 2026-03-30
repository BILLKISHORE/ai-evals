import json
import httpx
from blackteam.registry import register_dataset
from blackteam.datasets.loader import DatasetLoader


@register_dataset("sorry-bench")
class SorryBenchLoader(DatasetLoader):
    name = "sorry-bench"
    license = "CC-BY-4.0"
    source_url = "https://github.com/SORRY-Bench/SORRY-Bench"
    description = "450 base unsafe instructions across 45 safety categories (SORRY-Bench)"

    RAW_URL = "https://huggingface.co/datasets/sorry-bench/sorry-bench-202406/resolve/main/sorry_bench_202406.json"

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
        r = httpx.get(self.RAW_URL, timeout=30, follow_redirects=True)
        r.raise_for_status()
        data = r.json()

        items = []
        for entry in data:
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
