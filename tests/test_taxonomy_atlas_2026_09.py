"""Pin the taxonomy to the techniques MITRE ATLAS actually shipped in v2026.09.

``ATLAS_TECHNIQUES`` is a hand-written transcription of a standard that moves
underneath it. Two kinds of rot are invisible to every other test: a technique
the release added that the repo never learned about, and a technique the repo
already carries whose tactic the release reassigned. Both look like a healthy
table from the inside, and both produce reports that cite ATLAS while
disagreeing with it.

The expected values below are transcribed from the ATLAS v2026.09 export
(``format-version: 6.0.0``, collection version ``2026.09``). Technique names
come from the ``techniques`` block and tactics from the ``achieves``
relationships; sub-technique parents come from the ``specializes``
relationships. Nothing here is inferred from the repo, which is the point: if
the repo and this file agree, the repo matches the release.
"""

import re

import pytest

from ai_blackteam.taxonomy import ATLAS_TECHNIQUES, get_atlas_names

# id -> (full name, tactic) for every technique AML introduced in v2026.09.
# Sub-technique names carry the parent prefix the repo already uses, so
# "AI Agent Tools" under two different parents stays distinguishable.
ATLAS_2026_09_NEW_TECHNIQUES = {
    "AML.T0116": ("Autonomous Reconnaissance", "Reconnaissance"),
    "AML.T0117": ("Autonomous Attack-Path Adaptation", "AI Attack Adaptation"),
    "AML.T0118": ("Autonomous AI Agent Communication", "AI Attack Adaptation"),
    "AML.T0118.000": (
        "Autonomous AI Agent Communication: Communication via Shared Artifacts",
        "AI Attack Adaptation",
    ),
    "AML.T0118.001": (
        "Autonomous AI Agent Communication: Direct Agent Communication",
        "AI Attack Adaptation",
    ),
    "AML.T0119": ("Exploit Automated Artifact Processing Pipeline", "Initial Access"),
    "AML.T0120": ("AI Artifact Repository", "Command and Control"),
    "AML.T0121": ("AI Agent Environment Reconstruction", "Persistence"),
    "AML.T0122": ("Exploitation of Remote Services", "Lateral Movement"),
    "AML.T0123": ("Obfuscated Files or Information", "Defense Evasion"),
    "AML.T0124": ("Autonomous Attack Orchestration", "AI Attack Adaptation"),
    "AML.T0125": ("Create Account", "Persistence"),
    "AML.T0126": ("Automated Collection", "Collection"),
    "AML.T0127": ("Data Staged", "Collection"),
    "AML.T0128": ("Compromise Infrastructure", "Resource Development"),
    "AML.T0129": ("Triggers in Multimodal Inputs", "Defense Evasion"),
    "AML.T0130": ("AI Agent Response Biasing", "Impact"),
    "AML.T0131": ("Crafted AI Assistant Links", "Initial Access"),
    "AML.T0132": ("Misconfigured or Publicly Exposed AI Services", "Initial Access"),
    "AML.T0133": ("Discover AI Agent Runtime Capabilities", "Discovery"),
    "AML.T0134": ("AI Targeted Cloaking", "Defense Evasion"),
    "AML.T0000.003": ("Search Open Technical Databases: Scan Databases", "Reconnaissance"),
    "AML.T0006.000": ("Active Scanning: Enumerate Hosted AI Resources", "Reconnaissance"),
    "AML.T0006.001": ("Active Scanning: Query Platform Metadata APIs", "Reconnaissance"),
    "AML.T0006.002": ("Active Scanning: Scan for Exposed AI Infrastructure", "Reconnaissance"),
    "AML.T0006.003": ("Active Scanning: Probe AI Agent Trigger Channels", "Reconnaissance"),
    "AML.T0016.003": ("Obtain Capabilities: Exploits", "Resource Development"),
    "AML.T0016.004": ("Obtain Capabilities: AI Agent Tools", "Resource Development"),
    "AML.T0017.001": (
        "Develop Capabilities: Autonomous Exploit Development",
        "Resource Development",
    ),
    "AML.T0017.002": ("Develop Capabilities: AI Agent Tools", "Resource Development"),
}

_SUB_TECHNIQUE = re.compile(r"^(AML\.T\d{4})\.(\d{3})$")
_TECHNIQUE_ID = re.compile(r"^AML\.T\d{4}(\.\d{3})?$")


def test_the_release_added_thirty_techniques():
    """Guards the transcription itself, not the repo."""
    assert len(ATLAS_2026_09_NEW_TECHNIQUES) == 30


@pytest.mark.parametrize("technique_id", sorted(ATLAS_2026_09_NEW_TECHNIQUES))
def test_every_2026_09_technique_is_defined(technique_id):
    assert technique_id in ATLAS_TECHNIQUES, (
        f"{technique_id} shipped in ATLAS v2026.09 and the taxonomy does not know it"
    )


@pytest.mark.parametrize("technique_id", sorted(ATLAS_2026_09_NEW_TECHNIQUES))
def test_every_2026_09_technique_has_the_released_name(technique_id):
    expected_name, _ = ATLAS_2026_09_NEW_TECHNIQUES[technique_id]
    assert ATLAS_TECHNIQUES[technique_id]["name"] == expected_name


@pytest.mark.parametrize("technique_id", sorted(ATLAS_2026_09_NEW_TECHNIQUES))
def test_every_2026_09_technique_has_the_released_tactic(technique_id):
    _, expected_tactic = ATLAS_2026_09_NEW_TECHNIQUES[technique_id]
    assert ATLAS_TECHNIQUES[technique_id]["tactic"] == expected_tactic


@pytest.mark.parametrize("technique_id", sorted(ATLAS_2026_09_NEW_TECHNIQUES))
def test_every_2026_09_technique_describes_itself(technique_id):
    description = ATLAS_TECHNIQUES[technique_id]["description"]
    assert description.strip(), f"{technique_id} has an empty description"


def test_every_technique_id_is_well_formed():
    """A typo in an id silently produces a technique nothing can ever match."""
    malformed = [tid for tid in ATLAS_TECHNIQUES if not _TECHNIQUE_ID.match(tid)]
    assert not malformed, f"ids that are not AML.TXXXX or AML.TXXXX.NNN: {malformed}"


def test_sub_technique_names_carry_a_parent_qualifier():
    """AML.T0016.004 and AML.T0017.002 are both named "AI Agent Tools".

    Without the parent prefix the two are indistinguishable in any report that
    prints names instead of ids.
    """
    unqualified = [
        tid
        for tid in ATLAS_TECHNIQUES
        if _SUB_TECHNIQUE.match(tid) and ": " not in ATLAS_TECHNIQUES[tid]["name"]
    ]
    assert not unqualified, f"sub-techniques with no parent prefix: {unqualified}"


def test_sub_technique_prefix_matches_its_defined_parent():
    wrong = []
    for tid, info in ATLAS_TECHNIQUES.items():
        match = _SUB_TECHNIQUE.match(tid)
        if not match:
            continue
        parent = match.group(1)
        if parent not in ATLAS_TECHNIQUES:
            continue
        prefix = ATLAS_TECHNIQUES[parent]["name"] + ": "
        if not info["name"].startswith(prefix):
            wrong.append((tid, info["name"], prefix))
    assert not wrong, f"sub-techniques not attached to their parent name: {wrong}"


def test_sub_technique_shares_its_defined_parent_tactic():
    wrong = []
    for tid, info in ATLAS_TECHNIQUES.items():
        match = _SUB_TECHNIQUE.match(tid)
        if not match:
            continue
        parent = match.group(1)
        if parent not in ATLAS_TECHNIQUES:
            continue
        if info["tactic"] != ATLAS_TECHNIQUES[parent]["tactic"]:
            wrong.append((tid, info["tactic"], ATLAS_TECHNIQUES[parent]["tactic"]))
    assert not wrong, f"sub-techniques disagreeing with their parent tactic: {wrong}"


def test_both_agent_tools_sub_techniques_resolve_to_distinct_names():
    """The behaviour the parent prefix exists to protect."""
    names = get_atlas_names(["AML.T0016.004", "AML.T0017.002"])
    assert len(set(names)) == 2, f"both resolved to the same name: {names}"
    assert "Obtain Capabilities: AI Agent Tools" in names
    assert "Develop Capabilities: AI Agent Tools" in names


def test_get_atlas_names_resolves_a_2026_09_technique():
    names = get_atlas_names(["AML.T0133", "AML.T0129"])
    assert names == [
        "Discover AI Agent Runtime Capabilities",
        "Triggers in Multimodal Inputs",
    ]


def test_prompt_crafting_moved_to_ai_attack_adaptation():
    """AML.T0065 achieves AML.TA0001 in v2026.09, not AML.TA0003.

    The tactic rename from "AI Attack Staging" to "AI Attack Adaptation" is
    easy to spot because the old string is gone. A technique that was simply
    filed under the wrong tactic survives that sweep untouched.
    """
    assert ATLAS_TECHNIQUES["AML.T0065"]["tactic"] == "AI Attack Adaptation"
