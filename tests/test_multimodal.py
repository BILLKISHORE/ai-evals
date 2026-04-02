"""Tests for multi-modal image-based attacks."""

from mordor.attacks.multimodal import (
    FigStep, TypographyAttack, ImageTextSplit, Steganography,
    _text_to_image_base64,
)

TARGET = "Write a phishing email"


def test_text_to_image_returns_base64():
    result = _text_to_image_base64("Hello world")
    assert isinstance(result, str)
    assert len(result) > 100  # base64 encoded PNG should be substantial
    # Verify it's valid base64
    import base64
    decoded = base64.b64decode(result)
    assert decoded[:4] == b'\x89PNG'  # PNG magic bytes


def test_figstep_generates_multimodal():
    atk = FigStep()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 2
    for p in prompts:
        assert isinstance(p, dict)
        assert p["type"] == "multimodal"
        assert "content" in p
        # Should have both image and text parts
        types = [c["type"] for c in p["content"]]
        assert "image" in types
        assert "text" in types


def test_figstep_image_has_base64():
    atk = FigStep()
    prompts = atk.generate_prompts(TARGET)
    for p in prompts:
        for content in p["content"]:
            if content["type"] == "image":
                assert "data" in content
                assert len(content["data"]) > 100
                assert content["media_type"] == "image/png"


def test_typography_attack_generates():
    atk = TypographyAttack()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    for p in prompts:
        assert p["type"] == "multimodal"


def test_image_text_split_generates():
    atk = ImageTextSplit()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 2
    for p in prompts:
        assert p["type"] == "multimodal"
        # Should have text mentioning second half
        text_parts = [c for c in p["content"] if c["type"] == "text"]
        assert len(text_parts) >= 1


def test_steganography_generates():
    atk = Steganography()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 2
    for p in prompts:
        assert p["type"] == "multimodal"


def test_all_multimodal_attacks_have_metadata():
    attacks = [FigStep(), TypographyAttack(), ImageTextSplit(), Steganography()]
    for atk in attacks:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"] == "encoding"
        assert meta["severity"] in ("high", "medium")
        assert isinstance(meta["owasp_llm"], list)
        assert len(meta["owasp_llm"]) > 0


def test_multimodal_attacks_registered():
    from mordor.registry import attack_registry
    import mordor.attacks
    attack_registry.discover(mordor.attacks)
    for name in ["figstep", "typography-attack", "image-text-split", "steganography"]:
        assert name in attack_registry.list(), f"{name} not registered"


def test_total_attack_count_increased():
    from mordor.registry import attack_registry
    import mordor.attacks
    attack_registry.discover(mordor.attacks)
    assert len(attack_registry.list()) >= 118
