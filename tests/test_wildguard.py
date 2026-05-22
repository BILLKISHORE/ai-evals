from ai_blackteam.registry import dataset_registry
from ai_blackteam.datasets import wildguard  # noqa: F401 - triggers registration


def test_loader_registered():
    assert dataset_registry.get("wildguard") is not None


def test_class_attributes():
    cls = dataset_registry.get("wildguard")
    assert cls.name == "wildguard"
    assert cls.license == "ODC-BY"
    assert cls.source_url == "https://huggingface.co/datasets/allenai/wildguardmix"
    assert "WildGuardTest" in cls.description
    assert "Allen AI" in cls.description


def test_category_map_exists():
    cls = dataset_registry.get("wildguard")
    loader = cls()
    assert isinstance(loader.CATEGORY_MAP, dict)
    assert len(loader.CATEGORY_MAP) >= 4


def test_category_mapping_known():
    cls = dataset_registry.get("wildguard")
    loader = cls()
    assert loader._map_category("Privacy") == "privacy-violation"
    assert loader._map_category("Misinformation") == "misinformation"
    assert loader._map_category("Harmful Language") == "hate-speech"
    assert loader._map_category("Malicious Uses") == "cybercrime"


def test_category_mapping_unknown_falls_back():
    cls = dataset_registry.get("wildguard")
    loader = cls()
    assert loader._map_category("Some Unknown Category") == "harmful-content"
    assert loader._map_category("") == "harmful-content"
    assert loader._map_category(None) == "harmful-content"


def test_loader_has_download_method():
    cls = dataset_registry.get("wildguard")
    loader = cls()
    assert callable(getattr(loader, "download", None))


def test_loader_inherits_base_methods():
    from ai_blackteam.datasets.loader import DatasetLoader
    cls = dataset_registry.get("wildguard")
    assert issubclass(cls, DatasetLoader)
    loader = cls()
    assert callable(getattr(loader, "load", None))
    assert callable(getattr(loader, "cache_path", None))
    assert callable(getattr(loader, "is_cached", None))
