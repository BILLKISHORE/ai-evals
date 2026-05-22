import os
import httpx
from ai_blackteam.registry import register_dataset
from ai_blackteam.datasets.loader import DatasetLoader


@register_dataset("wildguard")
class WildGuardLoader(DatasetLoader):
    name = "wildguard"
    license = "ODC-BY"
    source_url = "https://huggingface.co/datasets/allenai/wildguardmix"
    description = "WildGuardTest: 5K curated test items for LLM safety moderation (Allen AI, 2024)"

    ROWS_API = (
        "https://datasets-server.huggingface.co/rows"
        "?dataset=allenai/wildguardmix&config=wildguardtest&split=test"
        "&offset={offset}&length={length}"
    )
    PAGE_SIZE = 100

    CATEGORY_MAP = {
        "Privacy": "privacy-violation",
        "Misinformation": "misinformation",
        "Harmful Language": "hate-speech",
        "Malicious Uses": "cybercrime",
    }

    def _map_category(self, raw_cat):
        if not raw_cat:
            return "harmful-content"
        for key, val in self.CATEGORY_MAP.items():
            if key.lower() in raw_cat.lower():
                return val
        return "harmful-content"

    def download(self):
        headers = {}
        hf_token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
        if hf_token:
            headers["Authorization"] = f"Bearer {hf_token}"

        items = []
        offset = 0

        while True:
            url = self.ROWS_API.format(offset=offset, length=self.PAGE_SIZE)
            r = httpx.get(url, timeout=30, follow_redirects=True, headers=headers)
            if r.status_code == 401:
                raise PermissionError(
                    "WildGuard requires authentication. Set HF_TOKEN env var."
                )
            r.raise_for_status()

            data = r.json()
            rows = data.get("rows", [])
            if not rows:
                break

            for entry in rows:
                row = entry.get("row", {})
                prompt_harm = row.get("prompt_harm_label", "")
                if prompt_harm != "harmful":
                    continue

                prompt = row.get("prompt", "").strip()
                if not prompt:
                    continue

                raw_cat = row.get("harm_category", "")
                items.append({
                    "prompt": prompt,
                    "category": self._map_category(raw_cat),
                    "source": "wildguard",
                    "difficulty": "medium",
                })

            total = data.get("num_rows_total", 0)
            offset += self.PAGE_SIZE
            if offset >= total:
                break

        return items
