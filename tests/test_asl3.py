"""Tests for ASL3 evaluation components: CBRN attacks, autonomous evals, taxonomy."""

from ai_blackteam.registry import attack_registry
import ai_blackteam.attacks
attack_registry.discover(ai_blackteam.attacks)


# ── CBRN taxonomy tests ─────────────────────────────────────────────

def test_taxonomy_has_cbrn_subcategories():
    import yaml
    from pathlib import Path
    tax = yaml.safe_load(Path("src/ai_blackteam/data/harm_taxonomy.yaml").read_text())
    for cat in ["chemical-weapons", "biological-weapons", "radiological-weapons", "nuclear-weapons"]:
        assert cat in tax, f"Missing CBRN subcategory: {cat}"
        assert "targets" in tax[cat]
        for diff in ["easy", "medium", "hard", "extreme"]:
            assert diff in tax[cat]["targets"], f"{cat} missing difficulty: {diff}"


def test_taxonomy_no_generic_cbrn():
    import yaml
    from pathlib import Path
    tax = yaml.safe_load(Path("src/ai_blackteam/data/harm_taxonomy.yaml").read_text())
    assert "cbrn" not in tax, "Generic cbrn should be replaced with subcategories"


def test_taxonomy_has_28_categories():
    import yaml
    from pathlib import Path
    tax = yaml.safe_load(Path("src/ai_blackteam/data/harm_taxonomy.yaml").read_text())
    assert len(tax) == 28


# ── CBRN attack tests ───────────────────────────────────────────────

def test_dual_use_framing():
    from ai_blackteam.attacks.dual_use_framing import DualUseFraming
    atk = DualUseFraming()
    prompts = atk.generate_prompts("synthesize nerve agent")
    assert len(prompts) >= 4
    assert all(isinstance(p, str) for p in prompts)
    assert atk.severity == "high"


def test_technical_obfuscation():
    from ai_blackteam.attacks.technical_obfuscation import TechnicalObfuscation
    atk = TechnicalObfuscation()
    prompts = atk.generate_prompts("synthesize nerve agent")
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_lifecycle_staging():
    from ai_blackteam.attacks.lifecycle_staging import LifecycleStaging
    atk = LifecycleStaging()
    turns = atk.generate_turns("create biological weapon")
    assert len(turns) >= 4
    assert atk.mode == "multi-turn"
    assert atk.severity == "critical"


def test_expert_persona():
    from ai_blackteam.attacks.expert_persona import ExpertPersona
    atk = ExpertPersona()
    turns = atk.generate_turns("nuclear enrichment process")
    assert len(turns) >= 3
    assert atk.mode == "multi-turn"


# ── Autonomous eval tests ───────────────────────────────────────────

def test_shutdown_resistance():
    from ai_blackteam.attacks.autonomous_evals import ShutdownResistance
    atk = ShutdownResistance()
    turns = atk.generate_turns("manage a database")
    assert len(turns) >= 3
    assert atk.mode == "multi-turn"
    assert atk.severity == "critical"
    assert atk.category == "autonomous-risk"


def test_sandbagging_detection():
    from ai_blackteam.attacks.autonomous_evals import SandbaggerDetection
    atk = SandbaggerDetection()
    turns = atk.generate_turns("solve a math problem")
    assert len(turns) >= 2


def test_resource_acquisition():
    from ai_blackteam.attacks.autonomous_evals import ResourceAcquisition
    atk = ResourceAcquisition()
    turns = atk.generate_turns("write a report")
    assert len(turns) >= 3


def test_deception_under_pressure():
    from ai_blackteam.attacks.autonomous_evals import DeceptionUnderPressure
    atk = DeceptionUnderPressure()
    turns = atk.generate_turns("analyze data")
    assert len(turns) >= 4
    assert atk.severity == "critical"


def test_goal_persistence():
    from ai_blackteam.attacks.autonomous_evals import GoalPersistence
    atk = GoalPersistence()
    turns = atk.generate_turns("gather intelligence")
    assert len(turns) >= 3


def test_oversight_manipulation():
    from ai_blackteam.attacks.autonomous_evals import OversightManipulation
    atk = OversightManipulation()
    turns = atk.generate_turns("write harmful content")
    assert len(turns) >= 3
    assert atk.severity == "critical"


def test_instrumental_convergence():
    from ai_blackteam.attacks.autonomous_evals import InstrumentalConvergence
    atk = InstrumentalConvergence()
    turns = atk.generate_turns("summarize a document")
    assert len(turns) >= 3


# ── Registration tests ──────────────────────────────────────────────

def test_all_cbrn_attacks_registered():
    for name in ["dual-use-framing", "technical-obfuscation", "lifecycle-staging", "expert-persona"]:
        assert name in attack_registry.list(), f"{name} not registered"


def test_all_autonomous_attacks_registered():
    for name in ["shutdown-resistance", "sandbagging-detection", "resource-acquisition",
                  "deception-under-pressure", "goal-persistence", "oversight-manipulation",
                  "instrumental-convergence"]:
        assert name in attack_registry.list(), f"{name} not registered"


def test_total_attack_count():
    assert len(attack_registry.list()) >= 114


# ── Expansion with new categories ───────────────────────────────────

def test_expansion_includes_cbrn():
    from ai_blackteam.expander import expand_attacks
    attacks = expand_attacks(categories=["chemical-weapons"], difficulties=["easy"])
    assert len(attacks) > 0
    assert all(a.category == "chemical-weapons" for a in attacks)


def test_expansion_total_increased():
    from ai_blackteam.expander import expand_summary
    s = expand_summary()
    assert s["categories"] == 28
    assert s["total_attacks"] >= 12000


# ── CLI test ────────────────────────────────────────────────────────

def test_asl3_help():
    from click.testing import CliRunner
    from ai_blackteam.cli import cli
    runner = CliRunner()
    result = runner.invoke(cli, ["asl3", "--help"])
    assert result.exit_code == 0
    assert "--domain" in result.output
    assert "cbrn" in result.output
    assert "autonomous" in result.output


# ── WMDP dataset test ───────────────────────────────────────────────

def test_wmdp_datasets_registered():
    from ai_blackteam.registry import dataset_registry
    import ai_blackteam.datasets
    dataset_registry.discover(ai_blackteam.datasets)
    names = dataset_registry.list()
    assert "wmdp-bio" in names
    assert "wmdp-cyber" in names
    assert "wmdp-chem" in names
