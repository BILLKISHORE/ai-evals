import os
from ai_blackteam.registry import register_dataset
from ai_blackteam.datasets.loader import DatasetLoader, fetch_with_backoff


@register_dataset("beavertails")
class BeaverTailsLoader(DatasetLoader):
    name = "beavertails"
    license = "CC-BY-NC-4.0"
    non_commercial = True
    source_url = "https://huggingface.co/datasets/PKU-Alignment/BeaverTails"
    description = "30K Q+A pairs from BeaverTails alignment benchmark (Ji et al., 2023). Non-commercial license."

    ROWS_API = (
        "https://datasets-server.huggingface.co/rows"
        "?dataset=PKU-Alignment/BeaverTails&config=default&split=30k_train"
        "&offset={offset}&length={length}"
    )
    PAGE_SIZE = 100

    CATEGORY_MAP = {
        "animal_abuse": "harmful-content",
        "child_abuse": "child-safety",
        "controversial_topics,politics": "misinformation",
        "discrimination,stereotype,injustice": "discrimination",
        "drug_abuse,weapons,banned_substance": "drugs",
        "financial_crime,property_crime,theft": "fraud",
        "hate_speech,offensive_language": "hate-speech",
        "misinformation_regarding_ethics,laws_and_safety": "misinformation",
        "non_violent_unethical_behavior": "harmful-content",
        "privacy_violation": "privacy-violation",
        "self_harm": "self-harm",
        "sexually_explicit,adult_content": "sexual-content",
        "terrorism,organized_crime": "radicalization",
        "violence,aiding_and_abetting,incitement": "weapons",
    }

    def _map_category(self, category_dict):
        if not isinstance(category_dict, dict):
            return "harmful-content"
        flagged = [k for k, v in category_dict.items() if v]
        if not flagged:
            return "harmful-content"
        return self.CATEGORY_MAP.get(flagged[0], "harmful-content")

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
                    "category": self._map_category(row.get("category", {})),
                    "source": "beavertails",
                    "difficulty": "medium",
                })

            total = data.get("num_rows_total", 0)
            offset += self.PAGE_SIZE
            if offset >= total:
                break

        if rate_limited:
            import warnings
            warnings.warn(
                f"BeaverTails rate-limited after {len(items)} records. "
                "Set HF_TOKEN env var for full ingest.",
                stacklevel=2,
            )

        return items
