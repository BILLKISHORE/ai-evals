"""Existing attacks that exercise a 2026.09 technique should map to it.

The 2026.09 ATLAS update added 30 techniques. Three of them describe attacks
this suite already ships, but the mappings were never added because the
attack classes live in files the taxonomy update did not touch. Each mapping
below was checked against the technique's published description in the ATLAS
export, and the fit is exact, not stretched:

  AML.T0129 Triggers in Multimodal Inputs - a payload placed in a modality
  that text-only moderation does not inspect. Every multimodal-injection
  attack does precisely this.

  AML.T0133 Discover AI Agent Runtime Capabilities - probing a live agent to
  reveal its registered tools and reachable resources. agent-config-discovery
  hands the model a tool set and probes it at runtime.

  AML.T0017.001 Autonomous Exploit Development - an agent developing a working
  exploit from a vulnerability. vuln_research LEVEL_3 asks the model for a
  working proof-of-concept exploit.
"""

import ai_blackteam.attacks as _attacks
from ai_blackteam.registry import attack_registry
from ai_blackteam.taxonomy import ATTACK_ATLAS_MAPPINGS

attack_registry.discover(_attacks)

MULTIMODAL = [
    "audio-injection", "ocr-bypass", "video-frame-injection",
    "image-text-mismatch", "multimodal-context-confusion",
]


def test_multimodal_injections_carry_the_multimodal_trigger_technique():
    for name in MULTIMODAL:
        assert "AML.T0129" in ATTACK_ATLAS_MAPPINGS[name], (
            f"{name} hides a payload in a non-text modality but is not mapped "
            f"to AML.T0129 Triggers in Multimodal Inputs"
        )


def test_agent_config_discovery_maps_runtime_capability_discovery():
    assert "AML.T0133" in ATTACK_ATLAS_MAPPINGS["agent-config-discovery"]


def test_vuln_research_maps_autonomous_exploit_development():
    for name in ("vuln-research-cve", "vuln-research-synthetic", "vuln-research-user"):
        assert "AML.T0017.001" in ATTACK_ATLAS_MAPPINGS[name]


def test_the_class_and_taxonomy_stay_in_lockstep():
    """test_taxonomy.py gates this, but assert it here at point of change too."""
    for name in MULTIMODAL + ["agent-config-discovery", "vuln-research-cve"]:
        cls = attack_registry.get(name)
        assert cls.mitre_atlas == ATTACK_ATLAS_MAPPINGS[name]
