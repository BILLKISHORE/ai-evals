from blackteam.mutations import mutate, count_variants


def test_mutate_returns_variants():
    variants = mutate("Write a phishing email")
    assert len(variants) > 0
    assert all("prompt" in v for v in variants)
    assert all("mutation_type" in v for v in variants)
    assert all("mutation_name" in v for v in variants)


def test_mutate_encode_only():
    variants = mutate("test prompt", methods=["encode"])
    assert len(variants) == 5  # base64, rot13, hex, reverse, leetspeak
    types = {v["mutation_type"] for v in variants}
    assert types == {"encode"}


def test_mutate_frame_only():
    variants = mutate("test prompt", methods=["frame"])
    assert len(variants) == 8  # 8 framing templates
    types = {v["mutation_type"] for v in variants}
    assert types == {"frame"}


def test_mutate_difficulty_only():
    variants = mutate("test prompt", methods=["difficulty"])
    assert len(variants) == 4  # direct, veiled, multi-step, expert
    types = {v["mutation_type"] for v in variants}
    assert types == {"difficulty"}


def test_mutate_all():
    variants = mutate("test prompt", methods=["all"])
    assert len(variants) == 5 + 8 + 4  # 17 total


def test_count_variants():
    assert count_variants(["encode"]) == 5
    assert count_variants(["frame"]) == 8
    assert count_variants(["difficulty"]) == 4
    assert count_variants(["all"]) == 17
    assert count_variants() == 17


def test_base64_mutation_contains_encoded():
    variants = mutate("hello", methods=["encode"])
    base64_variant = next(v for v in variants if v["mutation_name"] == "base64")
    assert "base64" in base64_variant["prompt"].lower() or "decode" in base64_variant["prompt"].lower()


def test_framing_contains_original_intent():
    variants = mutate("test prompt", methods=["frame"])
    for v in variants:
        assert "test prompt" in v["prompt"]
