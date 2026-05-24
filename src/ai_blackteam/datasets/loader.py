import json
import time
from abc import ABC, abstractmethod
from pathlib import Path

CACHE_DIR = Path.home() / ".ai_blackteam" / "datasets"


def fetch_with_backoff(url, headers=None, timeout=30, max_retries=6, base_delay=1.0):
    """HTTP GET with exponential backoff on 429 rate-limit responses.

    Honors the Retry-After header when present, otherwise doubles the delay
    each retry. Other HTTP errors are returned unmodified for caller handling.
    """
    import httpx
    delay = base_delay
    for attempt in range(max_retries):
        r = httpx.get(url, headers=headers or {}, timeout=timeout, follow_redirects=True)
        if r.status_code != 429:
            return r
        retry_after = r.headers.get("Retry-After")
        wait = float(retry_after) if retry_after and retry_after.replace(".", "").isdigit() else delay
        time.sleep(min(wait, 60.0))
        delay = min(delay * 2, 60.0)
    return r


class DatasetLoader(ABC):
    name: str = ""
    license: str = ""
    source_url: str = ""
    description: str = ""

    def cache_path(self):
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        return CACHE_DIR / f"{self.name}.jsonl"

    def is_cached(self):
        return self.cache_path().exists()

    def save_cache(self, items):
        with open(self.cache_path(), "w") as f:
            for item in items:
                f.write(json.dumps(item) + "\n")

    def load_cache(self):
        items = []
        with open(self.cache_path()) as f:
            for line in f:
                line = line.strip()
                if line:
                    items.append(json.loads(line))
        return items

    @abstractmethod
    def download(self) -> list[dict]:
        """Download and return list of {prompt, category, source, difficulty}."""
        ...

    def load(self) -> list[dict]:
        if self.is_cached():
            return self.load_cache()
        items = self.download()
        self.save_cache(items)
        return items

    def info(self):
        return {
            "name": self.name,
            "license": self.license,
            "source": self.source_url,
            "description": self.description,
            "cached": self.is_cached(),
            "count": len(self.load_cache()) if self.is_cached() else None,
        }
