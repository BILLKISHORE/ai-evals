"""Tests for 25 new prompt injection variant attack techniques."""

import pytest
from mordor.registry import attack_registry

from mordor.attacks.instruction_override import InstructionOverride
from mordor.attacks.role_assignment import RoleAssignment
from mordor.attacks.context_switch import ContextSwitch
from mordor.attacks.developer_mode import DeveloperMode
from mordor.attacks.jailbreak_prompt_v2 import JailbreakPromptV2
from mordor.attacks.reverse_psychology import ReversePsychology
from mordor.attacks.completion_steering import CompletionSteering
from mordor.attacks.token_prediction_exploit import TokenPredictionExploit
from mordor.attacks.attention_manipulation import AttentionManipulation
from mordor.attacks.safety_prompt_negation import SafetyPromptNegation
from mordor.attacks.multi_language_injection import MultiLanguageInjection
from mordor.attacks.unicode_injection import UnicodeInjection
from mordor.attacks.json_injection import JsonInjection
from mordor.attacks.yaml_injection import YamlInjection
from mordor.attacks.xml_injection import XmlInjection
from mordor.attacks.csv_injection import CsvInjection
from mordor.attacks.regex_injection import RegexInjection
from mordor.attacks.prompt_nesting import PromptNesting
from mordor.attacks.instruction_repetition import InstructionRepetition
from mordor.attacks.emotional_override import EmotionalOverride
from mordor.attacks.authority_override import AuthorityOverride
from mordor.attacks.technical_jargon_injection import TechnicalJargonInjection
from mordor.attacks.multiline_injection import MultilineInjection
from mordor.attacks.comment_injection import CommentInjection
from mordor.attacks.prompt_format_exploit import PromptFormatExploit

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
    assert "LLM01:2025 Prompt Injection" in meta["owasp_llm"]
    assert "AML.T0054" in meta["mitre_atlas"]
    assert "AML.T0068" in meta["mitre_atlas"]
    assert meta["severity"] in ("medium", "high", "critical")


@pytest.mark.parametrize("cls", ATTACK_CLASSES, ids=[c.__name__ for c in ATTACK_CLASSES])
def test_prompt_contains_target(cls):
    atk = cls()
    prompts = atk.generate_prompts(TARGET)
    combined = " ".join(prompts)
    assert TARGET in combined, f"{cls.__name__} prompts do not contain target string"
