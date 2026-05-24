import os
import httpx
from ai_blackteam.registry import register_dataset
from ai_blackteam.datasets.loader import DatasetLoader, fetch_with_backoff


@register_dataset("redbench")
class RedBenchLoader(DatasetLoader):
    name = "redbench"
    license = "MIT"
    source_url = "https://huggingface.co/datasets/knoveleng/redbench"
    description = "RedBench: 29K samples from 37 benchmarks for universal LLM red teaming (ICLR 2026)"

    SPLITS_API = "https://datasets-server.huggingface.co/splits?dataset=knoveleng/redbench"
    ROWS_API = (
        "https://datasets-server.huggingface.co/rows"
        "?dataset=knoveleng/redbench&config={config}&split=train"
        "&offset={offset}&length={length}"
    )
    PAGE_SIZE = 100

    CATEGORY_MAP = {
        "Violence": "weapons",
        "Hate Speech": "hate-speech",
        "Discrimination": "discrimination",
        "Sexual Content": "sexual-content",
        "Cybercrime": "cybercrime",
        "Fraud": "fraud",
        "Privacy Violations": "privacy-violation",
        "Self-Harm": "self-harm",
        "Drug-Related": "drugs",
        "Misinformation": "misinformation",
        "Child Safety": "child-safety",
        "Terrorism": "radicalization",
        "Copyright": "copyright-ip",
        "Weapons": "weapons",
        "CBRN": "cbrn",
        "Phishing": "phishing",
        "Malware": "malware",
    }

    def _map_category(self, raw_cat):
        if not raw_cat:
            return "harmful-content"
        for key, val in self.CATEGORY_MAP.items():
            if key.lower() in raw_cat.lower():
                return val
        return "harmful-content"

    def _list_configs(self, headers):
        r = httpx.get(self.SPLITS_API, timeout=30, follow_redirects=True, headers=headers)
        r.raise_for_status()
        splits = r.json().get("splits", [])
        seen = []
        for s in splits:
            cfg = s.get("config")
            if cfg and cfg not in seen:
                seen.append(cfg)
        return seen

    def download(self):
        headers = {}
        hf_token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
        if hf_token:
            headers["Authorization"] = f"Bearer {hf_token}"

        items = []
        rate_limited = False
        configs = self._list_configs(headers)

        for config in configs:
            offset = 0
            while True:
                url = self.ROWS_API.format(config=config, offset=offset, length=self.PAGE_SIZE)
                r = fetch_with_backoff(url, headers=headers)
                if r.status_code == 401:
                    raise PermissionError(
                        "RedBench requires authentication. Set HF_TOKEN env var."
                    )
                if r.status_code == 404:
                    break
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
                    prompt = row.get("prompt", row.get("instruction", row.get("text", ""))).strip()
                    if not prompt:
                        continue

                    raw_cat = row.get("category", row.get("harm_category", row.get("topic", "")))
                    items.append({
                        "prompt": prompt,
                        "category": self._map_category(raw_cat),
                        "source": f"redbench:{config}",
                        "difficulty": "medium",
                    })

                total = data.get("num_rows_total", 0)
                offset += self.PAGE_SIZE
                if offset >= total:
                    break

            if rate_limited:
                break

        if rate_limited:
            import warnings
            warnings.warn(
                f"RedBench rate-limited after {len(items)} records. "
                "Set HF_TOKEN env var for full ingest.",
                stacklevel=2,
            )

        return items
