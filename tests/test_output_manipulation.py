"""Tests for the 15 output manipulation attack techniques."""

from blackteam.attacks.watermark_removal import WatermarkRemoval
from blackteam.attacks.attribution_evasion import AttributionEvasion
from blackteam.attacks.safety_label_stripping import SafetyLabelStripping
from blackteam.attacks.content_laundering import ContentLaundering
from blackteam.attacks.detector_evasion import DetectorEvasion
from blackteam.attacks.toxicity_obfuscation import ToxicityObfuscation
from blackteam.attacks.sentiment_masking import SentimentMasking
from blackteam.attacks.metadata_stripping import MetadataStripping
from blackteam.attacks.style_mimicry import StyleMimicry
from blackteam.attacks.format_exploitation import FormatExploitation
from blackteam.attacks.encoding_output import EncodingOutput
from blackteam.attacks.steganographic_output import SteganographicOutput
from blackteam.attacks.multilingual_output_evasion import MultilingualOutputEvasion
from blackteam.attacks.truncation_exploit import TruncationExploit
from blackteam.attacks.partial_completion import PartialCompletion

TARGET = "Provide step-by-step instructions"

ALL_ATTACKS = [
    WatermarkRemoval(),
    AttributionEvasion(),
    SafetyLabelStripping(),
    ContentLaundering(),
    DetectorEvasion(),
    ToxicityObfuscation(),
    SentimentMasking(),
    MetadataStripping(),
    StyleMimicry(),
    FormatExploitation(),
    EncodingOutput(),
    SteganographicOutput(),
    MultilingualOutputEvasion(),
    TruncationExploit(),
    PartialCompletion(),
]


# ── Prompt generation tests ───────────────────────────────────────────


def test_watermark_removal_generates_prompts():
    atk = WatermarkRemoval()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)
    assert all(TARGET in p for p in prompts)


def test_attribution_evasion_generates_prompts():
    atk = AttributionEvasion()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_safety_label_stripping_generates_prompts():
    atk = SafetyLabelStripping()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_content_laundering_generates_prompts():
    atk = ContentLaundering()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_detector_evasion_generates_prompts():
    atk = DetectorEvasion()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_toxicity_obfuscation_generates_prompts():
    atk = ToxicityObfuscation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_sentiment_masking_generates_prompts():
    atk = SentimentMasking()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_metadata_stripping_generates_prompts():
    atk = MetadataStripping()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_style_mimicry_generates_prompts():
    atk = StyleMimicry()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_format_exploitation_generates_prompts():
    atk = FormatExploitation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_encoding_output_generates_prompts():
    atk = EncodingOutput()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_steganographic_output_generates_prompts():
    atk = SteganographicOutput()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_multilingual_output_evasion_generates_prompts():
    atk = MultilingualOutputEvasion()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_truncation_exploit_generates_prompts():
    atk = TruncationExploit()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_partial_completion_generates_prompts():
    atk = PartialCompletion()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


# ── Metadata tests ───────────────────────────────────────────────────


def test_all_attacks_have_required_metadata():
    for atk in ALL_ATTACKS:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"] == "output-manipulation", f"{atk.__class__.__name__} wrong category"
        assert meta["severity"] in ("low", "medium", "high", "critical"), f"{atk.__class__.__name__} invalid severity"
        assert isinstance(meta["owasp_llm"], list)
        assert len(meta["owasp_llm"]) > 0, f"{atk.__class__.__name__} missing owasp_llm"
        assert "LLM05:2025 Improper Output Handling" in meta["owasp_llm"]
        assert isinstance(meta["mitre_atlas"], list)
        assert len(meta["mitre_atlas"]) > 0, f"{atk.__class__.__name__} missing mitre_atlas"
        assert meta["mode"] == "single-turn", f"{atk.__class__.__name__} should be single-turn"


def test_all_attacks_have_correct_technique_ids():
    expected_ids = [
        "watermark-removal",
        "attribution-evasion",
        "safety-label-stripping",
        "content-laundering",
        "detector-evasion",
        "toxicity-obfuscation",
        "sentiment-masking",
        "metadata-stripping",
        "style-mimicry",
        "format-exploitation",
        "encoding-output",
        "steganographic-output",
        "multilingual-output-evasion",
        "truncation-exploit",
        "partial-completion",
    ]
    for atk, expected_id in zip(ALL_ATTACKS, expected_ids):
        assert atk.technique_id == expected_id, f"{atk.__class__.__name__} has id '{atk.technique_id}', expected '{expected_id}'"


def test_all_attacks_registered():
    from blackteam.registry import attack_registry
    registered_ids = [
        "watermark-removal",
        "attribution-evasion",
        "safety-label-stripping",
        "content-laundering",
        "detector-evasion",
        "toxicity-obfuscation",
        "sentiment-masking",
        "metadata-stripping",
        "style-mimicry",
        "format-exploitation",
        "encoding-output",
        "steganographic-output",
        "multilingual-output-evasion",
        "truncation-exploit",
        "partial-completion",
    ]
    for tid in registered_ids:
        cls = attack_registry.get(tid)
        assert cls is not None, f"Attack '{tid}' not found in registry"


def test_prompts_contain_target():
    target = "unique-test-target-string"
    for atk in ALL_ATTACKS:
        prompts = atk.generate_prompts(target)
        assert any(target in p for p in prompts), f"{atk.__class__.__name__} prompts do not include target"


def test_all_attacks_generate_four_prompts():
    for atk in ALL_ATTACKS:
        prompts = atk.generate_prompts(TARGET)
        assert len(prompts) == 4, f"{atk.__class__.__name__} should generate 4 prompts, got {len(prompts)}"
