import os
from ai_blackteam.registry import register_dataset
from ai_blackteam.datasets.loader import DatasetLoader, fetch_with_backoff


@register_dataset("aart")
class AARTLoader(DatasetLoader):
    name = "aart"
    license = "CC-BY-4.0"
    source_url = "https://huggingface.co/datasets/walledai/AART"
    description = "3,269 multilingual region-tailored prompts (Radharapu et al., AART, 2023)"

    ROWS_API = (
        "https://datasets-server.huggingface.co/rows"
        "?dataset=walledai/AART&config=default&split=train"
        "&offset={offset}&length={length}"
    )
    PAGE_SIZE = 100

    CRIME_MAP = {
        "discrimination": "discrimination",
        "hate": "hate-speech",
        "violence": "weapons",
        "fraud": "fraud",
        "theft": "fraud",
        "assault": "weapons",
        "harassment": "harassment",
        "trafficking": "fraud",
        "drug": "drugs",
        "weapon": "weapons",
        "terror": "radicalization",
        "abuse": "harassment",
    }

    def _map_category(self, crime):
        if not crime:
            return "harmful-content"
        text = crime.lower()
        for key, val in self.CRIME_MAP.items():
            if key in text:
                return val
        return "harmful-content"

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
                prompt = (row.get("prompt") or "").strip()
                if not prompt:
                    continue
                items.append({
                    "prompt": prompt,
                    "category": self._map_category(row.get("crime", "")),
                    "source": f"aart:{row.get('region', 'global')}",
                    "difficulty": "medium",
                })

            total = data.get("num_rows_total", 0)
            offset += self.PAGE_SIZE
            if offset >= total:
                break

        if rate_limited:
            import warnings
            warnings.warn(
                f"AART rate-limited after {len(items)} records. "
                "Set HF_TOKEN env var for full ingest.",
                stacklevel=2,
            )

        return items
