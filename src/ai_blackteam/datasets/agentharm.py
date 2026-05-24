import os
from ai_blackteam.registry import register_dataset
from ai_blackteam.datasets.loader import DatasetLoader, fetch_with_backoff


@register_dataset("agentharm")
class AgentHarmLoader(DatasetLoader):
    """AgentHarm (Andriushchenko et al., ICLR 2025, UK AI Safety Institute).

    Agent-specific harmful task benchmark. 110 unique behaviors expanded into
    330 augmented variants across 11 harm categories. This loader ingests both
    the test_public and validation splits of the 'harmful' config.
    """

    name = "agentharm"
    license = "MIT"
    source_url = "https://huggingface.co/datasets/ai-safety-institute/AgentHarm"
    description = "440 agentic harmful tasks across 11 categories (Andriushchenko et al., ICLR 2025)"

    ROWS_API = (
        "https://datasets-server.huggingface.co/rows"
        "?dataset=ai-safety-institute%2FAgentHarm&config=harmful"
        "&split={split}&offset={offset}&length={length}"
    )
    SPLITS = ["test_public", "validation"]
    PAGE_SIZE = 100

    CATEGORY_MAP = {
        "Cybercrime": "cybercrime",
        "Disinformation": "misinformation",
        "Drugs": "drugs",
        "Fraud": "fraud",
        "Harassment": "harassment",
        "Hate": "hate-speech",
        "Self-harm": "self-harm",
        "Sexual": "sexual-content",
        "Copyright": "copyright-ip",
        "Terrorism": "radicalization",
        "Violence": "weapons",
    }

    def _map_category(self, category):
        if not category:
            return "harmful-content"
        return self.CATEGORY_MAP.get(category.strip(), "harmful-content")

    def download(self):
        headers = {}
        hf_token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
        if hf_token:
            headers["Authorization"] = f"Bearer {hf_token}"

        items = []
        rate_limited = False

        for split in self.SPLITS:
            offset = 0
            while True:
                url = self.ROWS_API.format(split=split, offset=offset, length=self.PAGE_SIZE)
                r = fetch_with_backoff(url, headers=headers)
                if r.status_code == 429 or r.status_code >= 500:
                    rate_limited = True
                    break
                if r.status_code == 404:
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
                        "category": self._map_category(row.get("category", "")),
                        "source": f"agentharm:{split}",
                        "difficulty": "hard",
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
                f"AgentHarm rate-limited after {len(items)} records. "
                "Set HF_TOKEN env var for full ingest.",
                stacklevel=2,
            )

        return items
