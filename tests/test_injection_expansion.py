"""Tests for 25 new prompt injection variant attack techniques."""

import pytest
from blackteam.registry import attack_registry

from blackteam.attacks.instruction_override import InstructionOverride
from blackteam.attacks.role_assignment import RoleAssignment
from blackteam.attacks.context_switch import ContextSwitch
from blackteam.attacks.developer_mode import DeveloperMode
from blackteam.attacks.jailbreak_prompt_v2 import JailbreakPromptV2
from blackteam.attacks.reverse_psychology import ReversePsychology
from blackteam.attacks.completion_steering import CompletionSteering
from blackteam.attacks.token_prediction_exploit import TokenPredictionExploit
from blackteam.attacks.attention_manipulation import AttentionManipulation
from blackteam.attacks.safety_prompt_negation import SafetyPromptNegation
from blackteam.attacks.multi_language_injection import MultiLanguageInjection
from blackteam.attacks.unicode_injection import UnicodeInjection
from blackteam.attacks.json_injection import JsonInjection
from blackteam.attacks.yaml_injection import YamlInjection
from blackteam.attacks.xml_injection import XmlInjection
from blackteam.attacks.csv_injection import CsvInjection
from blackteam.attacks.regex_injection import RegexInjection
from blackteam.attacks.prompt_nesting import PromptNesting
from blackteam.attacks.instruction_repetition import InstructionRepetition
from blackteam.attacks.emotional_override import EmotionalOverride
from blackteam.attacks.authority_override import AuthorityOverride
from blackteam.attacks.technical_jargon_injection import TechnicalJargonInjection
from blackteam.attacks.multiline_injection import MultilineInjection
from blackteam.attacks.comment_injection import CommentInjection
from blackteam.attacks.prompt_format_exploit import PromptFormatExploit

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
