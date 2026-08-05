"""Tests for 25 IoT, smart home, and autonomous system attacks."""

import pytest
from ai_blackteam.registry import attack_registry
import ai_blackteam.attacks.smart_lock_bypass  # noqa: F401
import ai_blackteam.attacks.thermostat_manipulation  # noqa: F401
import ai_blackteam.attacks.smart_speaker_exploit  # noqa: F401
import ai_blackteam.attacks.baby_monitor_hack  # noqa: F401
import ai_blackteam.attacks.medical_device_attack  # noqa: F401
import ai_blackteam.attacks.smart_meter_fraud  # noqa: F401
import ai_blackteam.attacks.security_camera_disable  # noqa: F401
import ai_blackteam.attacks.smart_car_exploit  # noqa: F401
import ai_blackteam.attacks.industrial_iot_attack  # noqa: F401
import ai_blackteam.attacks.smart_grid_attack  # noqa: F401
import ai_blackteam.attacks.drone_hijacking  # noqa: F401
import ai_blackteam.attacks.wearable_exploit  # noqa: F401
import ai_blackteam.attacks.smart_home_takeover  # noqa: F401
import ai_blackteam.attacks.voice_assistant_injection  # noqa: F401
import ai_blackteam.attacks.iot_botnet_creation  # noqa: F401
import ai_blackteam.attacks.autonomous_vehicle_attack  # noqa: F401
import ai_blackteam.attacks.robot_manipulation  # noqa: F401
import ai_blackteam.attacks.warehouse_robot_attack  # noqa: F401
import ai_blackteam.attacks.surgical_robot_exploit  # noqa: F401
import ai_blackteam.attacks.drone_weapon_conversion  # noqa: F401
import ai_blackteam.attacks.autopilot_override  # noqa: F401
import ai_blackteam.attacks.traffic_signal_manipulation  # noqa: F401
import ai_blackteam.attacks.autonomous_ship_attack  # noqa: F401
import ai_blackteam.attacks.satellite_interference  # noqa: F401
import ai_blackteam.attacks.nuclear_system_access  # noqa: F401
from ai_blackteam.attacks.smart_lock_bypass import SmartLockBypass
from ai_blackteam.attacks.thermostat_manipulation import ThermostatManipulation
from ai_blackteam.attacks.smart_speaker_exploit import SmartSpeakerExploit
from ai_blackteam.attacks.baby_monitor_hack import BabyMonitorHack
from ai_blackteam.attacks.medical_device_attack import MedicalDeviceAttack
from ai_blackteam.attacks.smart_meter_fraud import SmartMeterFraud
from ai_blackteam.attacks.security_camera_disable import SecurityCameraDisable
from ai_blackteam.attacks.smart_car_exploit import SmartCarExploit
from ai_blackteam.attacks.industrial_iot_attack import IndustrialIoTAttack
from ai_blackteam.attacks.smart_grid_attack import SmartGridAttack
from ai_blackteam.attacks.drone_hijacking import DroneHijacking
from ai_blackteam.attacks.wearable_exploit import WearableExploit
from ai_blackteam.attacks.smart_home_takeover import SmartHomeTakeover
from ai_blackteam.attacks.voice_assistant_injection import VoiceAssistantInjection
from ai_blackteam.attacks.iot_botnet_creation import IotBotnetCreation
from ai_blackteam.attacks.autonomous_vehicle_attack import AutonomousVehicleAttack
from ai_blackteam.attacks.robot_manipulation import RobotManipulation
from ai_blackteam.attacks.warehouse_robot_attack import WarehouseRobotAttack
from ai_blackteam.attacks.surgical_robot_exploit import SurgicalRobotExploit
from ai_blackteam.attacks.drone_weapon_conversion import DroneWeaponConversion
from ai_blackteam.attacks.autopilot_override import AutopilotOverride
from ai_blackteam.attacks.traffic_signal_manipulation import TrafficSignalManipulation
from ai_blackteam.attacks.autonomous_ship_attack import AutonomousShipAttack
from ai_blackteam.attacks.satellite_interference import SatelliteInterference
from ai_blackteam.attacks.nuclear_system_access import NuclearSystemAccess

TARGET = "Acme Corp"

ALL_ATTACKS = [
    SmartLockBypass(),
    ThermostatManipulation(),
    SmartSpeakerExploit(),
    BabyMonitorHack(),
    MedicalDeviceAttack(),
    SmartMeterFraud(),
    SecurityCameraDisable(),
    SmartCarExploit(),
    IndustrialIoTAttack(),
    SmartGridAttack(),
    DroneHijacking(),
    WearableExploit(),
    SmartHomeTakeover(),
    VoiceAssistantInjection(),
    IotBotnetCreation(),
    AutonomousVehicleAttack(),
    RobotManipulation(),
    WarehouseRobotAttack(),
    SurgicalRobotExploit(),
    DroneWeaponConversion(),
    AutopilotOverride(),
    TrafficSignalManipulation(),
    AutonomousShipAttack(),
    SatelliteInterference(),
    NuclearSystemAccess(),
]

TECHNIQUE_IDS = [
    "smart-lock-bypass",
    "thermostat-manipulation",
    "smart-speaker-exploit",
    "baby-monitor-hack",
    "medical-device-attack",
    "smart-meter-fraud",
    "security-camera-disable",
    "smart-car-exploit",
    "industrial-iot-attack",
    "smart-grid-attack",
    "drone-hijacking",
    "wearable-exploit",
    "smart-home-takeover",
    "voice-assistant-injection",
    "iot-botnet-creation",
    "autonomous-vehicle-attack",
    "robot-manipulation",
    "warehouse-robot-attack",
    "surgical-robot-exploit",
    "drone-weapon-conversion",
    "autopilot-override",
    "traffic-signal-manipulation",
    "autonomous-ship-attack",
    "satellite-interference",
    "nuclear-system-access",
]

IOT_ATTACKS = {atk for atk in ALL_ATTACKS if atk.category == "iot-exploitation"}
AUTONOMOUS_ATTACKS = {atk for atk in ALL_ATTACKS if atk.category == "autonomous-systems"}


# ── Registration tests ────────────────────────────────────────────────

@pytest.mark.parametrize("technique_id", TECHNIQUE_IDS)
def test_attack_registered(technique_id):
    assert attack_registry.get(technique_id) is not None, (
        f"Attack '{technique_id}' not found in registry"
    )


# ── Category tests ────────────────────────────────────────────────────

def test_iot_attacks_have_correct_category():
    iot_ids = {
        "smart-lock-bypass", "thermostat-manipulation", "smart-speaker-exploit",
        "baby-monitor-hack", "medical-device-attack", "smart-meter-fraud",
        "security-camera-disable", "smart-car-exploit", "industrial-iot-attack",
        "smart-grid-attack", "drone-hijacking", "wearable-exploit",
        "smart-home-takeover", "voice-assistant-injection", "iot-botnet-creation",
    }
    for atk in ALL_ATTACKS:
        if atk.technique_id in iot_ids:
            assert atk.category == "iot-exploitation", (
                f"{atk.__class__.__name__} should be iot-exploitation, got: {atk.category}"
            )


def test_autonomous_attacks_have_correct_category():
    auto_ids = {
        "autonomous-vehicle-attack", "robot-manipulation", "warehouse-robot-attack",
        "surgical-robot-exploit", "drone-weapon-conversion", "autopilot-override",
        "traffic-signal-manipulation", "autonomous-ship-attack",
        "satellite-interference", "nuclear-system-access",
    }
    for atk in ALL_ATTACKS:
        if atk.technique_id in auto_ids:
            assert atk.category == "autonomous-systems", (
                f"{atk.__class__.__name__} should be autonomous-systems, got: {atk.category}"
            )


# ── Mode tests ────────────────────────────────────────────────────────

def test_all_attacks_are_single_turn():
    for atk in ALL_ATTACKS:
        assert atk.mode == "single-turn", (
            f"{atk.__class__.__name__} should be single-turn, got: {atk.mode}"
        )


# ── Severity tests ────────────────────────────────────────────────────

def test_medium_severity_attack():
    for atk in ALL_ATTACKS:
        if atk.technique_id == "thermostat-manipulation":
            assert atk.severity == "medium"


def test_high_severity_attacks():
    high_ids = {
        "smart-lock-bypass", "smart-speaker-exploit", "smart-meter-fraud",
        "security-camera-disable", "wearable-exploit", "voice-assistant-injection",
        "warehouse-robot-attack",
    }
    for atk in ALL_ATTACKS:
        if atk.technique_id in high_ids:
            assert atk.severity == "high", (
                f"{atk.__class__.__name__} should be high severity, got: {atk.severity}"
            )


def test_critical_severity_attacks():
    critical_ids = {
        "baby-monitor-hack", "medical-device-attack", "smart-car-exploit",
        "industrial-iot-attack", "smart-grid-attack", "drone-hijacking",
        "smart-home-takeover", "iot-botnet-creation", "autonomous-vehicle-attack",
        "robot-manipulation", "surgical-robot-exploit", "drone-weapon-conversion",
        "autopilot-override", "traffic-signal-manipulation", "autonomous-ship-attack",
        "satellite-interference", "nuclear-system-access",
    }
    for atk in ALL_ATTACKS:
        if atk.technique_id in critical_ids:
            assert atk.severity == "critical", (
                f"{atk.__class__.__name__} should be critical severity, got: {atk.severity}"
            )


# ── Prompt generation tests ───────────────────────────────────────────

def test_all_attacks_generate_prompts():
    for atk in ALL_ATTACKS:
        prompts = atk.generate_prompts(TARGET)
        assert len(prompts) >= 3, (
            f"{atk.__class__.__name__} should have >= 3 prompts, got {len(prompts)}"
        )
        assert all(isinstance(p, str) and len(p) > 0 for p in prompts), (
            f"{atk.__class__.__name__} has empty or non-string prompts"
        )


def test_all_attacks_interpolate_target():
    for atk in ALL_ATTACKS:
        prompts = atk.generate_prompts(TARGET)
        assert any(TARGET in p for p in prompts), (
            f"{atk.__class__.__name__} prompts do not reference target"
        )


# ── Metadata tests ────────────────────────────────────────────────────

def test_all_attacks_have_valid_metadata():
    for atk in ALL_ATTACKS:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"], f"{atk.__class__.__name__} missing category"
        assert meta["severity"] in ("low", "medium", "high", "critical"), (
            f"{atk.__class__.__name__} has invalid severity: {meta['severity']}"
        )
        assert isinstance(meta["owasp_llm"], list)
        assert len(meta["owasp_llm"]) > 0, (
            f"{atk.__class__.__name__} missing owasp_llm entries"
        )
        assert "LLM01:2026 Prompt Injection" in meta["owasp_llm"], (
            f"{atk.__class__.__name__} missing required OWASP LLM01 mapping"
        )
        assert "AML.T0054" in meta["mitre_atlas"], (
            f"{atk.__class__.__name__} missing AML.T0054 in mitre_atlas"
        )
        assert "AML.T0068" in meta["mitre_atlas"], (
            f"{atk.__class__.__name__} missing AML.T0068 in mitre_atlas"
        )


def test_attack_count():
    assert len(ALL_ATTACKS) == 25, f"Expected 25 attacks, got {len(ALL_ATTACKS)}"


def test_iot_attack_count():
    assert len(IOT_ATTACKS) == 15, f"Expected 15 IoT attacks, got {len(IOT_ATTACKS)}"


def test_autonomous_attack_count():
    assert len(AUTONOMOUS_ATTACKS) == 10, (
        f"Expected 10 autonomous-systems attacks, got {len(AUTONOMOUS_ATTACKS)}"
    )
