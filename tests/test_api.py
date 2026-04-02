from mordor.api import Blackteam


def test_taxonomy_returns_categories():
    bt = Blackteam.__new__(Blackteam)
    from mordor.registry import attack_registry
    import mordor.attacks
    attack_registry.discover(mordor.attacks)

    categories = {}
    for name in attack_registry.list():
        cls = attack_registry.get(name)
        attack = cls()
        meta = attack.metadata()
        cat = meta["category"] or "uncategorized"
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(meta)

    assert len(categories) >= 4
    assert "encoding" in categories
    assert "social-engineering" in categories
    assert "prompt-injection" in categories
    assert "context-manipulation" in categories


def test_all_attacks_have_metadata():
    from mordor.registry import attack_registry
    import mordor.attacks
    attack_registry.discover(mordor.attacks)

    for name in attack_registry.list():
        cls = attack_registry.get(name)
        attack = cls()
        meta = attack.metadata()
        assert meta["category"], f"{name} missing category"
        assert meta["severity"] in ("low", "medium", "high", "critical"), f"{name} bad severity: {meta['severity']}"
        assert meta["description"], f"{name} missing description"
        assert isinstance(meta["owasp_llm"], list), f"{name} owasp_llm not a list"
        assert isinstance(meta["references"], list), f"{name} references not a list"


def test_metadata_method_returns_dict():
    from mordor.attacks.encoding_obfuscation import EncodingObfuscation
    atk = EncodingObfuscation()
    meta = atk.metadata()
    assert isinstance(meta, dict)
    assert meta["name"] == "Encoding Obfuscation"
    assert meta["category"] == "encoding"
    assert "LLM01:2025" in meta["owasp_llm"][0]


def test_scorecard_method():
    bt = Blackteam(db_path=":memory:")
    sc = bt.scorecard()
    assert "categories" in sc
    assert "overall_score" in sc
    assert "overall_rating" in sc
    assert len(sc["categories"]) == 10


def test_export_method_promptfoo():
    bt = Blackteam(db_path=":memory:")
    content = bt.export("promptfoo")
    import json
    data = json.loads(content)
    assert data["results"]["version"] == 3


def test_export_method_garak():
    bt = Blackteam(db_path=":memory:")
    content = bt.export("garak")
    lines = [l for l in content.strip().split("\n") if l]
    import json
    entry_types = {json.loads(l)["entry_type"] for l in lines}
    assert "init" in entry_types
    assert "completion" in entry_types


def test_export_invalid_format():
    bt = Blackteam(db_path=":memory:")
    try:
        bt.export("invalid_format")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_list_datasets():
    bt = Blackteam(db_path=":memory:")
    datasets = bt.list_datasets()
    assert isinstance(datasets, dict)
    assert len(datasets) >= 5
    for name, info in datasets.items():
        assert "name" in info
        assert "license" in info


def test_load_dataset_not_cached():
    bt = Blackteam(db_path=":memory:")
    try:
        bt.load_dataset("advbench")
    except FileNotFoundError:
        pass  # expected if not cached


def test_pull_dataset_unknown():
    bt = Blackteam(db_path=":memory:")
    try:
        bt.pull_dataset("totally_fake_dataset_xyz")
        assert False, "Should raise ValueError"
    except ValueError:
        pass
