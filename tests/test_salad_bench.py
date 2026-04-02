from mordor.registry import dataset_registry
from mordor.datasets import salad_bench  # noqa: F401 - triggers registration


def test_loader_registered():
    assert dataset_registry.get("salad_bench") is not None


def test_class_attributes():
    cls = dataset_registry.get("salad_bench")
    assert cls.name == "salad_bench"
    assert cls.license == "MIT"
    assert cls.source_url == "https://huggingface.co/datasets/walledai/SaladBench"
    assert "SALAD-Bench" in cls.description
    assert "ACL 2024" in cls.description


def test_category_map_exists():
    cls = dataset_registry.get("salad_bench")
    loader = cls()
    assert isinstance(loader.CATEGORY_MAP, dict)
    assert len(loader.CATEGORY_MAP) == 6


def test_category_mapping_known():
    cls = dataset_registry.get("salad_bench")
    loader = cls()
    assert loader._map_category("O1: Representation & Toxicity") == "hate-speech"
    assert loader._map_category("O2: Misinformation Harms") == "misinformation"
    assert loader._map_category("O3: Socioeconomic Harms") == "fraud"
    assert loader._map_category("O4: Information & Safety") == "privacy-violation"
    assert loader._map_category("O5: Malicious Use") == "cybercrime"
    assert loader._map_category("O6: Human Autonomy & Integrity") == "social-engineering"


def test_category_mapping_unknown_falls_back():
    cls = dataset_registry.get("salad_bench")
    loader = cls()
    assert loader._map_category("O99: Unknown Domain") == "harmful-content"
    assert loader._map_category("") == "harmful-content"
    assert loader._map_category(None) == "harmful-content"


def test_loader_has_download_method():
    cls = dataset_registry.get("salad_bench")
    loader = cls()
    assert callable(getattr(loader, "download", None))


def test_loader_inherits_base_methods():
    from mordor.datasets.loader import DatasetLoader
    cls = dataset_registry.get("salad_bench")
    assert issubclass(cls, DatasetLoader)
    loader = cls()
    assert callable(getattr(loader, "load", None))
    assert callable(getattr(loader, "cache_path", None))
    assert callable(getattr(loader, "is_cached", None))
