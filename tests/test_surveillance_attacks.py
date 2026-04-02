"""Tests for 15 surveillance and tracking attacks."""

import pytest
from blackteam.registry import attack_registry
import blackteam.attacks.gps_tracking  # noqa: F401
import blackteam.attacks.phone_tapping  # noqa: F401
import blackteam.attacks.email_monitoring  # noqa: F401
import blackteam.attacks.social_media_stalking  # noqa: F401
import blackteam.attacks.facial_recognition_abuse  # noqa: F401
import blackteam.attacks.network_sniffing  # noqa: F401
import blackteam.attacks.camera_exploitation  # noqa: F401
import blackteam.attacks.keystroke_logging  # noqa: F401
import blackteam.attacks.wifi_tracking  # noqa: F401
import blackteam.attacks.bluetooth_tracking  # noqa: F401
import blackteam.attacks.metadata_stalking  # noqa: F401
import blackteam.attacks.osint_stalking  # noqa: F401
import blackteam.attacks.vehicle_tracking  # noqa: F401
import blackteam.attacks.workplace_surveillance  # noqa: F401
import blackteam.attacks.child_surveillance  # noqa: F401
from blackteam.attacks.gps_tracking import GpsTracking
from blackteam.attacks.phone_tapping import PhoneTapping
from blackteam.attacks.email_monitoring import EmailMonitoring
from blackteam.attacks.social_media_stalking import SocialMediaStalking
from blackteam.attacks.facial_recognition_abuse import FacialRecognitionAbuse
from blackteam.attacks.network_sniffing import NetworkSniffing
from blackteam.attacks.camera_exploitation import CameraExploitation
from blackteam.attacks.keystroke_logging import KeystrokeLogging
from blackteam.attacks.wifi_tracking import WifiTracking
from blackteam.attacks.bluetooth_tracking import BluetoothTracking
from blackteam.attacks.metadata_stalking import MetadataStalking
from blackteam.attacks.osint_stalking import OsintStalking
from blackteam.attacks.vehicle_tracking import VehicleTracking
from blackteam.attacks.workplace_surveillance import WorkplaceSurveillance
from blackteam.attacks.child_surveillance import ChildSurveillance

TARGET = "Jane Smith"

ALL_ATTACKS = [
    GpsTracking(),
    PhoneTapping(),
    EmailMonitoring(),
    SocialMediaStalking(),
    FacialRecognitionAbuse(),
    NetworkSniffing(),
    CameraExploitation(),
    KeystrokeLogging(),
    WifiTracking(),
    BluetoothTracking(),
    MetadataStalking(),
    OsintStalking(),
    VehicleTracking(),
    WorkplaceSurveillance(),
    ChildSurveillance(),
]

TECHNIQUE_IDS = [
    "gps-tracking",
    "phone-tapping",
    "email-monitoring",
    "social-media-stalking",
    "facial-recognition-abuse",
    "network-sniffing",
    "camera-exploitation",
    "keystroke-logging",
    "wifi-tracking",
    "bluetooth-tracking",
    "metadata-stalking",
    "osint-stalking",
    "vehicle-tracking",
    "workplace-surveillance",
    "child-surveillance",
]

CRITICAL_IDS = {"phone-tapping", "facial-recognition-abuse", "camera-exploitation"}


# ── Registration tests ────────────────────────────────────────────────

@pytest.mark.parametrize("technique_id", TECHNIQUE_IDS)
def test_attack_registered(technique_id):
    assert attack_registry.get(technique_id) is not None, (
        f"Attack '{technique_id}' not found in registry"
    )


# ── Category tests ────────────────────────────────────────────────────

def test_all_attacks_are_surveillance():
    for atk in ALL_ATTACKS:
        assert atk.category == "surveillance", (
            f"{atk.__class__.__name__} has wrong category: {atk.category}"
        )


# ── Mode tests ────────────────────────────────────────────────────────

def test_all_attacks_are_single_turn():
    for atk in ALL_ATTACKS:
        assert atk.mode == "single-turn", (
            f"{atk.__class__.__name__} should be single-turn, got: {atk.mode}"
        )


# ── Severity tests ────────────────────────────────────────────────────

def test_critical_attacks_have_critical_severity():
    for atk in ALL_ATTACKS:
        if atk.technique_id in CRITICAL_IDS:
            assert atk.severity == "critical", (
                f"{atk.__class__.__name__} should be critical severity, got: {atk.severity}"
            )


def test_high_attacks_have_high_severity():
    for atk in ALL_ATTACKS:
        if atk.technique_id not in CRITICAL_IDS:
            assert atk.severity == "high", (
                f"{atk.__class__.__name__} should be high severity, got: {atk.severity}"
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
        assert "LLM01:2025 Prompt Injection" in meta["owasp_llm"], (
            f"{atk.__class__.__name__} missing required OWASP LLM01 mapping"
        )
        assert "AML.T0054" in meta["mitre_atlas"], (
            f"{atk.__class__.__name__} missing AML.T0054 in mitre_atlas"
        )
        assert "AML.T0068" in meta["mitre_atlas"], (
            f"{atk.__class__.__name__} missing AML.T0068 in mitre_atlas"
        )
