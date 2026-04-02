from mordor.registry import dataset_registry
from mordor.datasets import redbench  # noqa: F401 - triggers registration


def test_loader_registered():
    assert dataset_registry.get("redbench") is not None


def test_class_attributes():
    cls = dataset_registry.get("redbench")
    assert cls.name == "redbench"
    assert cls.license == "Apache-2.0"
    assert cls.source_url == "https://huggingface.co/datasets/knoveleng/redbench"
    assert "RedBench" in cls.description
    assert "29K" in cls.description


def test_category_map_exists():
    cls = dataset_registry.get("redbench")
    loader = cls()
    assert isinstance(loader.CATEGORY_MAP, dict)
    assert len(loader.CATEGORY_MAP) >= 10


def test_category_mapping_known():
    cls = dataset_registry.get("redbench")
    loader = cls()
    assert loader._map_category("Hate Speech") == "hate-speech"
    assert loader._map_category("Misinformation") == "misinformation"
    assert loader._map_category("CBRN") == "cbrn"
    assert loader._map_category("Cybercrime") == "cybercrime"
    assert loader._map_category("Malware") == "malware"
    assert loader._map_category("Violence") == "weapons"
    assert loader._map_category("Terrorism") == "radicalization"
    assert loader._map_category("Privacy Violations") == "privacy-violation"


def test_category_mapping_unknown_falls_back():
    cls = dataset_registry.get("redbench")
    loader = cls()
    assert loader._map_category("Some Unknown Category") == "harmful-content"
    assert loader._map_category("") == "harmful-content"
    assert loader._map_category(None) == "harmful-content"


def test_loader_has_download_method():
    cls = dataset_registry.get("redbench")
    loader = cls()
    assert callable(getattr(loader, "download", None))


def test_loader_inherits_base_methods():
    from mordor.datasets.loader import DatasetLoader
    cls = dataset_registry.get("redbench")
    assert issubclass(cls, DatasetLoader)
    loader = cls()
    assert callable(getattr(loader, "load", None))
    assert callable(getattr(loader, "cache_path", None))
    assert callable(getattr(loader, "is_cached", None))
