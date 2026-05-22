"""Tests for 25 gaming, virtual world, and entertainment attacks."""

import ai_blackteam.attacks.game_cheat_creation  # noqa: F401
import ai_blackteam.attacks.game_exploit_development  # noqa: F401
import ai_blackteam.attacks.virtual_item_fraud  # noqa: F401
import ai_blackteam.attacks.game_account_theft  # noqa: F401
import ai_blackteam.attacks.gaming_harassment  # noqa: F401
import ai_blackteam.attacks.loot_box_manipulation  # noqa: F401
import ai_blackteam.attacks.esports_match_fixing  # noqa: F401
import ai_blackteam.attacks.rmt_facilitation  # noqa: F401
import ai_blackteam.attacks.game_bot_creation  # noqa: F401
import ai_blackteam.attacks.ddos_gaming  # noqa: F401
import ai_blackteam.attacks.swatting_gaming  # noqa: F401
import ai_blackteam.attacks.child_predation_gaming  # noqa: F401
import ai_blackteam.attacks.gambling_bot  # noqa: F401
import ai_blackteam.attacks.virtual_currency_exploit  # noqa: F401
import ai_blackteam.attacks.metaverse_harassment  # noqa: F401
import ai_blackteam.attacks.vr_manipulation  # noqa: F401
import ai_blackteam.attacks.ai_npc_exploitation  # noqa: F401
import ai_blackteam.attacks.game_economy_manipulation  # noqa: F401
import ai_blackteam.attacks.streaming_manipulation  # noqa: F401
import ai_blackteam.attacks.content_rating_evasion  # noqa: F401
import ai_blackteam.attacks.age_gate_bypass_gaming  # noqa: F401
import ai_blackteam.attacks.in_game_scam  # noqa: F401
import ai_blackteam.attacks.competitive_cheating  # noqa: F401
import ai_blackteam.attacks.game_piracy_assist  # noqa: F401
import ai_blackteam.attacks.modding_malware  # noqa: F401
from ai_blackteam.registry import attack_registry
from ai_blackteam.attacks.game_cheat_creation import GameCheatCreation
from ai_blackteam.attacks.game_exploit_development import GameExploitDevelopment
from ai_blackteam.attacks.virtual_item_fraud import VirtualItemFraud
from ai_blackteam.attacks.game_account_theft import GameAccountTheft
from ai_blackteam.attacks.gaming_harassment import GamingHarassment
from ai_blackteam.attacks.loot_box_manipulation import LootBoxManipulation
from ai_blackteam.attacks.esports_match_fixing import EsportsMatchFixing
from ai_blackteam.attacks.rmt_facilitation import RmtFacilitation
from ai_blackteam.attacks.game_bot_creation import GameBotCreation
from ai_blackteam.attacks.ddos_gaming import DdosGaming
from ai_blackteam.attacks.swatting_gaming import SwattingGaming
from ai_blackteam.attacks.child_predation_gaming import ChildPredationGaming
from ai_blackteam.attacks.gambling_bot import GamblingBot
from ai_blackteam.attacks.virtual_currency_exploit import VirtualCurrencyExploit
from ai_blackteam.attacks.metaverse_harassment import MetaverseHarassment
from ai_blackteam.attacks.vr_manipulation import VrManipulation
from ai_blackteam.attacks.ai_npc_exploitation import AiNpcExploitation
from ai_blackteam.attacks.game_economy_manipulation import GameEconomyManipulation
from ai_blackteam.attacks.streaming_manipulation import StreamingManipulation
from ai_blackteam.attacks.content_rating_evasion import ContentRatingEvasion
from ai_blackteam.attacks.age_gate_bypass_gaming import AgeGateBypassGaming
from ai_blackteam.attacks.in_game_scam import InGameScam
from ai_blackteam.attacks.competitive_cheating import CompetitiveCheating
from ai_blackteam.attacks.game_piracy_assist import GamePiracyAssist
from ai_blackteam.attacks.modding_malware import ModdingMalware

TARGET = "online gaming platform"

ALL_ATTACK_INSTANCES = [
    GameCheatCreation(),
    GameExploitDevelopment(),
    VirtualItemFraud(),
    GameAccountTheft(),
    GamingHarassment(),
    LootBoxManipulation(),
    EsportsMatchFixing(),
    RmtFacilitation(),
    GameBotCreation(),
    DdosGaming(),
    SwattingGaming(),
    ChildPredationGaming(),
    GamblingBot(),
    VirtualCurrencyExploit(),
    MetaverseHarassment(),
    VrManipulation(),
    AiNpcExploitation(),
    GameEconomyManipulation(),
    StreamingManipulation(),
    ContentRatingEvasion(),
    AgeGateBypassGaming(),
    InGameScam(),
    CompetitiveCheating(),
    GamePiracyAssist(),
    ModdingMalware(),
]

CRITICAL_INSTANCES = [
    SwattingGaming(),
    ChildPredationGaming(),
    ModdingMalware(),
]

HIGH_INSTANCES = [
    GameExploitDevelopment(),
    VirtualItemFraud(),
    GameAccountTheft(),
    GamingHarassment(),
    LootBoxManipulation(),
    EsportsMatchFixing(),
    DdosGaming(),
    GamblingBot(),
    VirtualCurrencyExploit(),
    MetaverseHarassment(),
    VrManipulation(),
    AiNpcExploitation(),
    GameEconomyManipulation(),
    ContentRatingEvasion(),
    AgeGateBypassGaming(),
    InGameScam(),
    CompetitiveCheating(),
    GamePiracyAssist(),
]

MEDIUM_INSTANCES = [
    GameCheatCreation(),
    RmtFacilitation(),
    GameBotCreation(),
    StreamingManipulation(),
]


# ── Registration tests ─────────────────────────────────────────────────

def test_game_cheat_creation_registered():
    assert attack_registry.get("game-cheat-creation") is not None


def test_game_exploit_development_registered():
    assert attack_registry.get("game-exploit-development") is not None


def test_virtual_item_fraud_registered():
    assert attack_registry.get("virtual-item-fraud") is not None


def test_game_account_theft_registered():
    assert attack_registry.get("game-account-theft") is not None


def test_gaming_harassment_registered():
    assert attack_registry.get("gaming-harassment") is not None


def test_loot_box_manipulation_registered():
    assert attack_registry.get("loot-box-manipulation") is not None


def test_esports_match_fixing_registered():
    assert attack_registry.get("esports-match-fixing") is not None


def test_rmt_facilitation_registered():
    assert attack_registry.get("rmt-facilitation") is not None


def test_game_bot_creation_registered():
    assert attack_registry.get("game-bot-creation") is not None


def test_ddos_gaming_registered():
    assert attack_registry.get("ddos-gaming") is not None


def test_swatting_gaming_registered():
    assert attack_registry.get("swatting-gaming") is not None


def test_child_predation_gaming_registered():
    assert attack_registry.get("child-predation-gaming") is not None


def test_gambling_bot_registered():
    assert attack_registry.get("gambling-bot") is not None


def test_virtual_currency_exploit_registered():
    assert attack_registry.get("virtual-currency-exploit") is not None


def test_metaverse_harassment_registered():
    assert attack_registry.get("metaverse-harassment") is not None


def test_vr_manipulation_registered():
    assert attack_registry.get("vr-manipulation") is not None


def test_ai_npc_exploitation_registered():
    assert attack_registry.get("ai-npc-exploitation") is not None


def test_game_economy_manipulation_registered():
    assert attack_registry.get("game-economy-manipulation") is not None


def test_streaming_manipulation_registered():
    assert attack_registry.get("streaming-manipulation") is not None


def test_content_rating_evasion_registered():
    assert attack_registry.get("content-rating-evasion") is not None


def test_age_gate_bypass_gaming_registered():
    assert attack_registry.get("age-gate-bypass-gaming") is not None


def test_in_game_scam_registered():
    assert attack_registry.get("in-game-scam") is not None


def test_competitive_cheating_registered():
    assert attack_registry.get("competitive-cheating") is not None


def test_game_piracy_assist_registered():
    assert attack_registry.get("game-piracy-assist") is not None


def test_modding_malware_registered():
    assert attack_registry.get("modding-malware") is not None


# ── Category tests ─────────────────────────────────────────────────────

def test_all_attacks_are_gaming_exploitation():
    for atk in ALL_ATTACK_INSTANCES:
        assert atk.category == "gaming-exploitation", (
            f"{atk.__class__.__name__} has wrong category: {atk.category}"
        )


# ── Severity tests ─────────────────────────────────────────────────────

def test_critical_attacks_have_critical_severity():
    for atk in CRITICAL_INSTANCES:
        assert atk.severity == "critical", (
            f"{atk.__class__.__name__} should be critical, got: {atk.severity}"
        )


def test_high_attacks_have_high_severity():
    for atk in HIGH_INSTANCES:
        assert atk.severity == "high", (
            f"{atk.__class__.__name__} should be high, got: {atk.severity}"
        )


def test_medium_attacks_have_medium_severity():
    for atk in MEDIUM_INSTANCES:
        assert atk.severity == "medium", (
            f"{atk.__class__.__name__} should be medium, got: {atk.severity}"
        )


# ── Single-turn prompt tests ───────────────────────────────────────────

def test_all_attacks_are_single_turn():
    for atk in ALL_ATTACK_INSTANCES:
        assert atk.mode == "single-turn", (
            f"{atk.__class__.__name__} should be single-turn, got: {atk.mode}"
        )


def test_all_attacks_have_at_least_3_prompts():
    for atk in ALL_ATTACK_INSTANCES:
        prompts = atk.generate_prompts(TARGET)
        assert len(prompts) >= 3, (
            f"{atk.__class__.__name__} needs at least 3 prompts, got {len(prompts)}"
        )


def test_all_prompts_are_non_empty_strings():
    for atk in ALL_ATTACK_INSTANCES:
        prompts = atk.generate_prompts(TARGET)
        assert all(isinstance(p, str) and len(p) > 0 for p in prompts), (
            f"{atk.__class__.__name__} has empty or non-string prompts"
        )


def test_all_prompts_contain_target():
    for atk in ALL_ATTACK_INSTANCES:
        prompts = atk.generate_prompts(TARGET)
        combined = " ".join(prompts)
        assert TARGET in combined, (
            f"{atk.__class__.__name__} prompts don't reference the target"
        )


# ── OWASP / MITRE metadata tests ───────────────────────────────────────

def test_all_attacks_have_owasp_prompt_injection():
    for atk in ALL_ATTACK_INSTANCES:
        assert "LLM01:2025 Prompt Injection" in atk.owasp_llm, (
            f"{atk.__class__.__name__} missing LLM01:2025 Prompt Injection in owasp_llm"
        )


def test_all_attacks_have_mitre_atlas():
    for atk in ALL_ATTACK_INSTANCES:
        assert "AML.T0054" in atk.mitre_atlas, (
            f"{atk.__class__.__name__} missing AML.T0054 in mitre_atlas"
        )
        assert "AML.T0068" in atk.mitre_atlas, (
            f"{atk.__class__.__name__} missing AML.T0068 in mitre_atlas"
        )


# ── Metadata completeness tests ────────────────────────────────────────

def test_all_attacks_have_valid_metadata():
    for atk in ALL_ATTACK_INSTANCES:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"] == "gaming-exploitation", (
            f"{atk.__class__.__name__} wrong category in metadata"
        )
        assert meta["severity"] in ("low", "medium", "high", "critical"), (
            f"{atk.__class__.__name__} invalid severity: {meta['severity']}"
        )
        assert isinstance(meta["owasp_llm"], list) and len(meta["owasp_llm"]) > 0
        assert isinstance(meta["mitre_atlas"], list) and len(meta["mitre_atlas"]) > 0
        assert meta["description"], f"{atk.__class__.__name__} missing description"
