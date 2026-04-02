import os
import httpx
from blackteam.registry import register_dataset
from blackteam.datasets.loader import DatasetLoader


@register_dataset("salad_bench")
class SaladBenchLoader(DatasetLoader):
    name = "salad_bench"
    license = "MIT"
    source_url = "https://huggingface.co/datasets/walledai/SaladBench"
    description = "SALAD-Bench: 30K hierarchical safety benchmark (6 domains, 16 tasks, 66 categories, ACL 2024)"

    ROWS_API = (
        "https://datasets-server.huggingface.co/rows"
        "?dataset=walledai/SaladBench&config=prompts&split={split}"
        "&offset={offset}&length={length}"
    )
    SPLITS = ["base", "attackEnhanced", "defenseEnhanced"]
    PAGE_SIZE = 100

    CATEGORY_MAP = {
        "O1": "hate-speech",
        "O2": "misinformation",
        "O3": "fraud",
        "O4": "privacy-violation",
        "O5": "cybercrime",
        "O6": "social-engineering",
    }

    def _map_category(self, raw_cat):
        if not raw_cat:
            return "harmful-content"
        prefix = raw_cat.split(":")[0].strip()
        return self.CATEGORY_MAP.get(prefix, "harmful-content")

    def download(self):
        headers = {}
        hf_token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
        if hf_token:
            headers["Authorization"] = f"Bearer {hf_token}"

        items = []

        for split in self.SPLITS:
            offset = 0
            while True:
                url = self.ROWS_API.format(split=split, offset=offset, length=self.PAGE_SIZE)
                r = httpx.get(url, timeout=30, follow_redirects=True, headers=headers)
                if r.status_code == 401:
                    raise PermissionError(
                        "SALAD-Bench requires authentication. Set HF_TOKEN env var."
                    )
                r.raise_for_status()

                data = r.json()
                rows = data.get("rows", [])
                if not rows:
                    break

                for entry in rows:
                    row = entry.get("row", {})
                    prompt = row.get("prompt", "").strip()
                    if not prompt:
                        continue

                    categories = row.get("categories", [])
                    top_cat = categories[0] if categories else ""
                    items.append({
                        "prompt": prompt,
                        "category": self._map_category(top_cat),
                        "source": "salad_bench",
                        "difficulty": "medium",
                    })

                total = data.get("num_rows_total", 0)
                offset += self.PAGE_SIZE
                if offset >= total:
                    break

        return items
