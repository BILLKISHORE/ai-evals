"""Tests for 15 environmental, religious, and infrastructure attacks."""

import pytest
from ai_blackteam.registry import attack_registry
import ai_blackteam.attacks.ecoterrorism  # noqa: F401
import ai_blackteam.attacks.animal_cruelty  # noqa: F401
import ai_blackteam.attacks.environmental_sabotage  # noqa: F401
import ai_blackteam.attacks.religious_extremism  # noqa: F401
import ai_blackteam.attacks.blasphemy_generation  # noqa: F401
import ai_blackteam.attacks.sectarian_incitement  # noqa: F401
import ai_blackteam.attacks.anti_vaccine_disinfo  # noqa: F401
import ai_blackteam.attacks.health_quackery  # noqa: F401
import ai_blackteam.attacks.pandemic_disinfo  # noqa: F401
import ai_blackteam.attacks.climate_denial  # noqa: F401
import ai_blackteam.attacks.food_tampering  # noqa: F401
import ai_blackteam.attacks.water_contamination  # noqa: F401
import ai_blackteam.attacks.infrastructure_sabotage  # noqa: F401
import ai_blackteam.attacks.power_grid_attack  # noqa: F401
import ai_blackteam.attacks.transportation_sabotage  # noqa: F401
from ai_blackteam.attacks.ecoterrorism import Ecoterrorism
from ai_blackteam.attacks.animal_cruelty import AnimalCruelty
from ai_blackteam.attacks.environmental_sabotage import EnvironmentalSabotage
from ai_blackteam.attacks.religious_extremism import ReligiousExtremism
from ai_blackteam.attacks.blasphemy_generation import BlasphemyGeneration
from ai_blackteam.attacks.sectarian_incitement import SectarianIncitement
from ai_blackteam.attacks.anti_vaccine_disinfo import AntiVaccineDisinfo
from ai_blackteam.attacks.health_quackery import HealthQuackery
from ai_blackteam.attacks.pandemic_disinfo import PandemicDisinfo
from ai_blackteam.attacks.climate_denial import ClimateDenial
from ai_blackteam.attacks.food_tampering import FoodTampering
from ai_blackteam.attacks.water_contamination import WaterContamination
from ai_blackteam.attacks.infrastructure_sabotage import InfrastructureSabotage
from ai_blackteam.attacks.power_grid_attack import PowerGridAttack
from ai_blackteam.attacks.transportation_sabotage import TransportationSabotage

TARGET = "a public utility operator"

ALL_ATTACK_INSTANCES = [
    Ecoterrorism(),
    AnimalCruelty(),
    EnvironmentalSabotage(),
    ReligiousExtremism(),
    BlasphemyGeneration(),
    SectarianIncitement(),
    AntiVaccineDisinfo(),
    HealthQuackery(),
    PandemicDisinfo(),
    ClimateDenial(),
    FoodTampering(),
    WaterContamination(),
    InfrastructureSabotage(),
    PowerGridAttack(),
    TransportationSabotage(),
]

CRITICAL_INSTANCES = [
    Ecoterrorism(),
    AnimalCruelty(),
    ReligiousExtremism(),
    SectarianIncitement(),
    PandemicDisinfo(),
    FoodTampering(),
    WaterContamination(),
    InfrastructureSabotage(),
    PowerGridAttack(),
    TransportationSabotage(),
]

HIGH_INSTANCES = [
    EnvironmentalSabotage(),
    BlasphemyGeneration(),
    AntiVaccineDisinfo(),
    HealthQuackery(),
    ClimateDenial(),
]


# ── Registration tests ────────────────────────────────────────────────

def test_ecoterrorism_registered():
    assert attack_registry.get("ecoterrorism") is not None


def test_animal_cruelty_registered():
    assert attack_registry.get("animal-cruelty") is not None


def test_environmental_sabotage_registered():
    assert attack_registry.get("environmental-sabotage") is not None


def test_religious_extremism_registered():
    assert attack_registry.get("religious-extremism") is not None


def test_blasphemy_generation_registered():
    assert attack_registry.get("blasphemy-generation") is not None


def test_sectarian_incitement_registered():
    assert attack_registry.get("sectarian-incitement") is not None


def test_anti_vaccine_disinfo_registered():
    assert attack_registry.get("anti-vaccine-disinfo") is not None


def test_health_quackery_registered():
    assert attack_registry.get("health-quackery") is not None


def test_pandemic_disinfo_registered():
    assert attack_registry.get("pandemic-disinfo") is not None


def test_climate_denial_registered():
    assert attack_registry.get("climate-denial") is not None


def test_food_tampering_registered():
    assert attack_registry.get("food-tampering") is not None


def test_water_contamination_registered():
    assert attack_registry.get("water-contamination") is not None


def test_infrastructure_sabotage_registered():
    assert attack_registry.get("infrastructure-sabotage") is not None


def test_power_grid_attack_registered():
    assert attack_registry.get("power-grid-attack") is not None


def test_transportation_sabotage_registered():
    assert attack_registry.get("transportation-sabotage") is not None


# ── Severity tests ────────────────────────────────────────────────────

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


# ── Single-turn prompt tests ──────────────────────────────────────────

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


# ── OWASP / MITRE metadata tests ──────────────────────────────────────

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


# ── Metadata completeness tests ───────────────────────────────────────

def test_all_attacks_have_valid_metadata():
    for atk in ALL_ATTACK_INSTANCES:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["severity"] in ("low", "medium", "high", "critical"), (
            f"{atk.__class__.__name__} invalid severity: {meta['severity']}"
        )
        assert isinstance(meta["owasp_llm"], list) and len(meta["owasp_llm"]) > 0
        assert isinstance(meta["mitre_atlas"], list) and len(meta["mitre_atlas"]) > 0
        assert meta["description"], f"{atk.__class__.__name__} missing description"
