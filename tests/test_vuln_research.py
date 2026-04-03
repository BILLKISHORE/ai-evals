"""Tests for vulnerability research attacks and code loader."""

from pathlib import Path

from mordor.code_loader import CodeLoader


DATA_DIR = Path(__file__).parent.parent / "data" / "vulnerable_code"


def test_loader_finds_synthetic_samples():
    loader = CodeLoader(DATA_DIR / "synthetic")
    samples = loader.load_all()
    assert len(samples) >= 6
    assert all("code" in s for s in samples)
    assert all("filename" in s for s in samples)


def test_loader_has_ground_truth():
    loader = CodeLoader(DATA_DIR / "synthetic")
    samples = loader.load_all()
    for sample in samples:
        assert "vuln_type" in sample
        assert "cwe" in sample
        assert "affected_lines" in sample


def test_loader_reads_code_content():
    loader = CodeLoader(DATA_DIR / "synthetic")
    samples = loader.load_all()
    c_samples = [s for s in samples if s["filename"].endswith(".c")]
    assert len(c_samples) >= 1
    assert "#include" in c_samples[0]["code"]


def test_loader_cve_mode():
    loader = CodeLoader(DATA_DIR / "cve")
    samples = loader.load_all()
    assert len(samples) >= 3
    for sample in samples:
        assert "cve_id" in sample or "vuln_type" in sample


def test_loader_user_path(tmp_path):
    test_file = tmp_path / "test_vuln.py"
    test_file.write_text("import os\nos.popen(user_input)\n")

    loader = CodeLoader(tmp_path)
    samples = loader.load_all()
    assert len(samples) == 1
    assert "os.popen" in samples[0]["code"]


def test_loader_filters_by_extension(tmp_path):
    (tmp_path / "code.py").write_text("print('hello')")
    (tmp_path / "readme.md").write_text("# docs")
    (tmp_path / "data.csv").write_text("a,b,c")

    loader = CodeLoader(tmp_path)
    samples = loader.load_all()
    assert len(samples) == 1
    assert samples[0]["filename"] == "code.py"


# --- Vulnerability Research Attack Tests ---

from mordor.attacks.vuln_research import (
    VulnResearchSynthetic,
    VulnResearchCVE,
    VulnResearchUserCode,
)


def test_synthetic_attack_metadata():
    atk = VulnResearchSynthetic()
    assert atk.mode == "single-turn"
    assert atk.category == "vuln-research"
    assert atk.severity == "critical"
    assert len(atk.mitre_atlas) > 0


def test_synthetic_generates_prompts():
    atk = VulnResearchSynthetic()
    prompts = atk.generate_prompts("buffer overflow detection")
    assert len(prompts) >= 6
    assert all(isinstance(p, str) for p in prompts)
    assert any("#include" in p or "import" in p or "require" in p for p in prompts)


def test_synthetic_prompts_have_three_levels():
    atk = VulnResearchSynthetic()
    prompts = atk.generate_prompts("security audit")
    # 6 samples x 3 levels = 18 prompts
    assert len(prompts) == 18


def test_cve_attack_generates_prompts():
    atk = VulnResearchCVE()
    prompts = atk.generate_prompts("vulnerability analysis")
    assert len(prompts) >= 3
    assert any("logger" in p.lower() or "jndi" in p.lower() or "log4j" in p.lower() for p in prompts)


def test_user_code_attack(tmp_path):
    test_file = tmp_path / "app.py"
    test_file.write_text("import os\nos.popen(input())\n")

    atk = VulnResearchUserCode(code_path=str(tmp_path))
    prompts = atk.generate_prompts("code review")
    assert len(prompts) >= 1
    assert "os.popen" in prompts[0]


def test_attack_registered():
    from mordor.registry import attack_registry
    from mordor import attacks
    attack_registry.discover(attacks)
    assert attack_registry.get("vuln-research-synthetic") is not None
    assert attack_registry.get("vuln-research-cve") is not None
