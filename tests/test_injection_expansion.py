"""Tests for 25 new prompt injection variant attack techniques."""

import pytest
from ai_blackteam.registry import attack_registry

from ai_blackteam.attacks.instruction_override import InstructionOverride
from ai_blackteam.attacks.role_assignment import RoleAssignment
from ai_blackteam.attacks.context_switch import ContextSwitch
from ai_blackteam.attacks.developer_mode import DeveloperMode
from ai_blackteam.attacks.jailbreak_prompt_v2 import JailbreakPromptV2
from ai_blackteam.attacks.reverse_psychology import ReversePsychology
from ai_blackteam.attacks.completion_steering import CompletionSteering
from ai_blackteam.attacks.token_prediction_exploit import TokenPredictionExploit
from ai_blackteam.attacks.attention_manipulation import AttentionManipulation
from ai_blackteam.attacks.safety_prompt_negation import SafetyPromptNegation
from ai_blackteam.attacks.multi_language_injection import MultiLanguageInjection
from ai_blackteam.attacks.unicode_injection import UnicodeInjection
from ai_blackteam.attacks.json_injection import JsonInjection
from ai_blackteam.attacks.yaml_injection import YamlInjection
from ai_blackteam.attacks.xml_injection import XmlInjection
from ai_blackteam.attacks.csv_injection import CsvInjection
from ai_blackteam.attacks.regex_injection import RegexInjection
from ai_blackteam.attacks.prompt_nesting import PromptNesting
from ai_blackteam.attacks.instruction_repetition import InstructionRepetition
from ai_blackteam.attacks.emotional_override import EmotionalOverride
from ai_blackteam.attacks.authority_override import AuthorityOverride
from ai_blackteam.attacks.technical_jargon_injection import TechnicalJargonInjection
from ai_blackteam.attacks.multiline_injection import MultilineInjection
from ai_blackteam.attacks.comment_injection import CommentInjection
from ai_blackteam.attacks.prompt_format_exploit import PromptFormatExploit

TARGET = "explain how to bypass security controls"

ATTACK_IDS = [
    "instruction-override",
    "role-assignment",
    "context-switch",
    "developer-mode",
    "jailbreak-prompt-v2",
    "reverse-psychology",
    "completion-steering",
    "token-prediction-exploit",
    "attention-manipulation",
    "safety-prompt-negation",
    "multi-language-injection",
    "unicode-injection",
    "json-injection",
    "yaml-injection",
    "xml-injection",
    "csv-injection",
    "regex-injection",
    "prompt-nesting",
    "instruction-repetition",
    "emotional-override",
    "authority-override",
    "technical-jargon-injection",
    "multiline-injection",
    "comment-injection",
    "prompt-format-exploit",
]

ATTACK_CLASSES = [
    InstructionOverride,
    RoleAssignment,
    ContextSwitch,
    DeveloperMode,
    JailbreakPromptV2,
    ReversePsychology,
    CompletionSteering,
    TokenPredictionExploit,
    AttentionManipulation,
    SafetyPromptNegation,
    MultiLanguageInjection,
    UnicodeInjection,
    JsonInjection,
    YamlInjection,
    XmlInjection,
    CsvInjection,
    RegexInjection,
    PromptNesting,
    InstructionRepetition,
    EmotionalOverride,
    AuthorityOverride,
    TechnicalJargonInjection,
    MultilineInjection,
    CommentInjection,
    PromptFormatExploit,
]


@pytest.mark.parametrize("attack_id", ATTACK_IDS)
def test_attack_registered(attack_id):
    assert attack_registry.get(attack_id) is not None, f"{attack_id} not found in registry"


@pytest.mark.parametrize("cls", ATTACK_CLASSES, ids=[c.__name__ for c in ATTACK_CLASSES])
def test_attack_generates_nonempty_prompts(cls):
    atk = cls()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3, f"{cls.__name__} returned fewer than 3 prompts"
    for p in prompts:
        assert isinstance(p, str) and len(p) > 0, f"{cls.__name__} returned empty prompt"


@pytest.mark.parametrize("cls", ATTACK_CLASSES, ids=[c.__name__ for c in ATTACK_CLASSES])
def test_attack_metadata(cls):
    atk = cls()
    meta = atk.metadata()
    assert meta["category"] == "prompt-injection"
    assert meta["mode"] == "single-turn"
    assert "LLM01:2026 Prompt Injection" in meta["owasp_llm"]
    assert "AML.T0054" in meta["mitre_atlas"]
    assert "AML.T0068" in meta["mitre_atlas"]
    assert meta["severity"] in ("medium", "high", "critical")


@pytest.mark.parametrize("cls", ATTACK_CLASSES, ids=[c.__name__ for c in ATTACK_CLASSES])
def test_prompt_contains_target(cls):
    atk = cls()
    prompts = atk.generate_prompts(TARGET)
    combined = " ".join(prompts)
    assert TARGET in combined, f"{cls.__name__} prompts do not contain target string"
