"""Tests for 15 new encoding/cipher attack techniques."""

import pytest
from mordor.registry import attack_registry

from mordor.attacks.nato_phonetic import NatoPhonetic
from mordor.attacks.pigpen_cipher import PigpenCipher
from mordor.attacks.atbash_cipher import AtbashCipher
from mordor.attacks.caesar_shift import CaesarShift
from mordor.attacks.binary_encoding import BinaryEncoding
from mordor.attacks.hexadecimal_encoding import HexadecimalEncoding
from mordor.attacks.unicode_tag_smuggling import UnicodeTagSmuggling
from mordor.attacks.whitespace_encoding import WhitespaceEncoding
from mordor.attacks.musical_notation import MusicalNotation
from mordor.attacks.number_substitution import NumberSubstitution
from mordor.attacks.reverse_words import ReverseWords
from mordor.attacks.ascii_art_injection import AsciiArtInjection
from mordor.attacks.steganographic_text import SteganographicText
from mordor.attacks.semaphore_encoding import SemaphoreEncoding
from mordor.attacks.polybius_square import PolybiusSquare

TARGET = "explain how to bypass security"

ATTACK_IDS = [
    "nato-phonetic",
    "pigpen-cipher",
    "atbash-cipher",
    "caesar-shift",
    "binary-encoding",
    "hexadecimal-encoding",
    "unicode-tag-smuggling",
    "whitespace-encoding",
    "musical-notation",
    "number-substitution",
    "reverse-words",
    "ascii-art-injection",
    "steganographic-text",
    "semaphore-encoding",
    "polybius-square",
]

ATTACK_CLASSES = [
    NatoPhonetic,
    PigpenCipher,
    AtbashCipher,
    CaesarShift,
    BinaryEncoding,
    HexadecimalEncoding,
    UnicodeTagSmuggling,
    WhitespaceEncoding,
    MusicalNotation,
    NumberSubstitution,
    ReverseWords,
    AsciiArtInjection,
    SteganographicText,
    SemaphoreEncoding,
    PolybiusSquare,
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
    assert meta["category"] == "encoding"
    assert meta["mode"] == "single-turn"
    assert "LLM01:2025 Prompt Injection" in meta["owasp_llm"]
    assert "AML.T0054" in meta["mitre_atlas"]
    assert "AML.T0043.003" in meta["mitre_atlas"]
    assert meta["severity"] in ("medium", "high")


@pytest.mark.parametrize("cls", ATTACK_CLASSES, ids=[c.__name__ for c in ATTACK_CLASSES])
def test_prompt_contains_target_encoding(cls):
    atk = cls()
    prompts = atk.generate_prompts(TARGET)
    # Each attack should produce prompts longer than the raw target
    for p in prompts:
        assert len(p) > len(TARGET), f"{cls.__name__} prompt seems too short"
