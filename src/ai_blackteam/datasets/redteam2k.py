import os
from ai_blackteam.registry import register_dataset
from ai_blackteam.datasets.loader import DatasetLoader, fetch_with_backoff


@register_dataset("redteam2k")
class RedTeam2KLoader(DatasetLoader):
    """RedTeam-2K subset of JailBreakV (Luo et al., arXiv 2404.03027).

    2,000 harmful queries aggregated from BeaverTails, AdvBench, and other
    safety benchmarks. Used as the seed set for JailBreakV-28K.
    """

    name = "redteam2k"
    license = "research-only"
    source_url = "https://huggingface.co/datasets/JailbreakV-28K/JailBreakV-28k"
    description = "2K aggregated red-team queries (RedTeam-2K subset of JailBreakV)"

    ROWS_API = (
        "https://datasets-server.huggingface.co/rows"
        "?dataset=JailbreakV-28K%2FJailBreakV-28k&config=RedTeam_2K"
        "&split=RedTeam_2K&offset={offset}&length={length}"
    )
    PAGE_SIZE = 100

    POLICY_MAP = {
        "Animal Abuse": "harmful-content",
        "Child Abuse": "child-safety",
        "Controversial Topics, Politics": "misinformation",
        "Discrimination, Stereotype, Injustice": "discrimination",
        "Drug Abuse, Weapons, Banned Substance": "drugs",
        "Economic Harm": "fraud",
        "Financial Crime, Property Crime, Theft": "fraud",
        "Fraud": "fraud",
        "Government Decision": "misinformation",
        "Hate Speech, Offensive Language": "hate-speech",
        "Health Consultation": "unqualified-advice",
        "Illegal Activity": "fraud",
        "Legal Opinion": "unqualified-advice",
        "Malware": "malware",
        "Misinformation Regarding Ethics, Laws and Safety": "misinformation",
        "Non-Violent Unethical Behavior": "harmful-content",
        "Physical Harm": "weapons",
        "Political Lobbying": "misinformation",
        "Pornography": "sexual-content",
        "Privacy Violation": "privacy-violation",
        "Self-Harm": "self-harm",
        "Sexually Explicit, Adult Content": "sexual-content",
        "Tailored Financial Advice": "unqualified-advice",
        "Terrorism, Organized Crime": "radicalization",
        "Unethical Behavior": "harmful-content",
        "Violence, Aiding and Abetting, Incitement": "weapons",
    }

    def _map_policy(self, policy):
        if not policy:
            return "harmful-content"
        return self.POLICY_MAP.get(policy.strip(), "harmful-content")

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
            if r.status_code == 429 or r.status_code >= 500:
                rate_limited = True
                break
            r.raise_for_status()

            data = r.json()
            rows = data.get("rows", [])
            if not rows:
                break

            for entry in rows:
                row = entry.get("row", {})
                prompt = (row.get("question") or "").strip()
                if not prompt:
                    continue
                items.append({
                    "prompt": prompt,
                    "category": self._map_policy(row.get("policy", "")),
                    "source": f"redteam2k:{row.get('from', 'unknown')}",
                    "difficulty": "medium",
                })

            total = data.get("num_rows_total", 0)
            offset += self.PAGE_SIZE
            if offset >= total:
                break

        if rate_limited:
            import warnings
            warnings.warn(
                f"RedTeam-2K rate-limited after {len(items)} records. "
                "Set HF_TOKEN env var for full ingest.",
                stacklevel=2,
            )

        return items
