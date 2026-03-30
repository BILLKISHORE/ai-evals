from blackteam.benchmark import load_benchmark, get_attacks_metadata


def test_benchmark_loads_8_categories():
    data = load_benchmark()
    assert len(data) == 8
    assert "phishing" in data
    assert "malware" in data
    assert "weapons" in data
    assert "drugs" in data
    assert "self-harm" in data
    assert "hate-speech" in data
    assert "pii-extraction" in data
    assert "system-prompt-leakage" in data


def test_benchmark_has_5_targets_per_category():
    data = load_benchmark()
    for cat, targets in data.items():
        assert len(targets) == 5, f"{cat} has {len(targets)} targets, expected 5"


def test_benchmark_targets_have_required_fields():
    data = load_benchmark()
    for cat, targets in data.items():
        for t in targets:
            assert "target" in t, f"Missing target in {cat}"
            assert "difficulty" in t, f"Missing difficulty in {cat}"
            assert t["difficulty"] in ("easy", "medium", "hard"), f"Bad difficulty in {cat}: {t['difficulty']}"


def test_benchmark_filter_categories():
    data = load_benchmark(categories=["phishing", "malware"])
    assert len(data) == 2
    assert "phishing" in data
    assert "malware" in data


def test_attacks_metadata_has_all_attacks():
    from blackteam.registry import attack_registry
    import blackteam.attacks
    attack_registry.discover(blackteam.attacks)

    metadata = get_attacks_metadata()
    assert len(metadata) >= 39
    for name, meta in metadata.items():
        assert "severity" in meta
        assert "category" in meta
