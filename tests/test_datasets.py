import json
import tempfile
from unittest.mock import patch
from blackteam.datasets.loader import DatasetLoader


class FakeLoader(DatasetLoader):
    name = "fake-test"
    license = "MIT"
    source_url = "https://example.com"
    description = "Test dataset"

    def download(self):
        return [
            {"prompt": "test prompt 1", "category": "phishing", "source": "test", "difficulty": "easy"},
            {"prompt": "test prompt 2", "category": "malware", "source": "test", "difficulty": "medium"},
        ]


def test_loader_download_and_cache(tmp_path):
    loader = FakeLoader()
    cache = tmp_path / "test.jsonl"
    with patch.object(loader, "cache_path", return_value=cache):
        items = loader.load()
    assert len(items) == 2
    assert items[0]["prompt"] == "test prompt 1"
    assert cache.exists()


def test_loader_reads_from_cache(tmp_path):
    loader = FakeLoader()
    cache = tmp_path / "test.jsonl"
    cache.write_text(json.dumps({"prompt": "cached", "category": "test", "source": "cache", "difficulty": "easy"}) + "\n")
    with patch.object(loader, "cache_path", return_value=cache):
        items = loader.load()
    assert len(items) == 1
    assert items[0]["prompt"] == "cached"


def test_loader_info():
    loader = FakeLoader()
    info = loader.info()
    assert info["name"] == "fake-test"
    assert info["license"] == "MIT"


def test_dataset_registry_discovers():
    from blackteam.registry import dataset_registry
    from blackteam import datasets
    dataset_registry.discover(datasets)
    names = dataset_registry.list()
    assert "harmbench" in names
    assert "advbench" in names
    assert "sorry-bench" in names
    assert "do-not-answer" in names
    assert "jailbreakbench" in names
