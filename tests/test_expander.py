from blackteam.registry import attack_registry
import blackteam.attacks
attack_registry.discover(blackteam.attacks)

from blackteam.expander import (
    load_taxonomy, expand_attacks, expand_count, expand_summary, TemplateAttack,
)


def test_load_taxonomy_has_28_categories():
    taxonomy = load_taxonomy()
    assert len(taxonomy) == 28


def test_taxonomy_categories_have_4_difficulties():
    taxonomy = load_taxonomy()
    for cat_id, cat_info in taxonomy.items():
        targets = cat_info.get("targets", {})
        for diff in ["easy", "medium", "hard", "extreme"]:
            assert diff in targets, f"{cat_id} missing difficulty: {diff}"


def test_taxonomy_categories_have_owasp():
    taxonomy = load_taxonomy()
    for cat_id, cat_info in taxonomy.items():
        assert "owasp" in cat_info, f"{cat_id} missing owasp field"
        assert isinstance(cat_info["owasp"], list)


def test_expand_attacks_returns_list():
    attacks = expand_attacks()
    assert isinstance(attacks, list)
    assert len(attacks) > 5000


def test_expand_attacks_are_template_attacks():
    attacks = expand_attacks(categories=["phishing"], difficulties=["easy"])
    for atk in attacks:
        assert isinstance(atk, TemplateAttack)


def test_expand_attacks_id_format():
    attacks = expand_attacks(
        techniques=["encoding-obfuscation"],
        categories=["phishing"],
        difficulties=["hard"],
    )
    assert len(attacks) == 1
    assert attacks[0].technique_id == "encoding-obfuscation-phishing-hard"


def test_expand_attacks_filter_by_category():
    all_attacks = expand_attacks()
    phishing_only = expand_attacks(categories=["phishing"])
    assert len(phishing_only) < len(all_attacks)
    for atk in phishing_only:
        assert atk.category == "phishing"


def test_expand_attacks_filter_by_difficulty():
    hard_only = expand_attacks(difficulties=["hard"])
    for atk in hard_only:
        assert atk.difficulty == "hard"
        assert atk.severity == "high"


def test_expand_attacks_filter_by_technique():
    filtered = expand_attacks(techniques=["dan-variants"])
    for atk in filtered:
        assert "dan-variants" in atk.technique_id


def test_expand_attacks_owasp_merged():
    attacks = expand_attacks(
        techniques=["encoding-obfuscation"],
        categories=["misinformation"],
        difficulties=["easy"],
    )
    atk = attacks[0]
    owasp_ids = [o.split(":")[0] for o in atk.owasp_llm]
    # encoding-obfuscation has LLM01, misinformation category has LLM01 + LLM09
    assert "LLM01" in owasp_ids


def test_expand_attacks_generate_prompts():
    attacks = expand_attacks(
        techniques=["encoding-obfuscation"],
        categories=["phishing"],
        difficulties=["easy"],
    )
    atk = attacks[0]
    prompts = atk.generate_prompts()
    assert isinstance(prompts, list)
    assert len(prompts) > 0
    assert all(isinstance(p, str) for p in prompts)


def test_expand_count():
    count = expand_count()
    summary = expand_summary()
    assert count == summary["total_attacks"]


def test_expand_summary():
    s = expand_summary()
    assert s["techniques"] >= 50
    assert s["categories"] == 28
    assert s["difficulties"] == 4
    assert s["total_attacks"] == s["techniques"] * s["categories"] * 4
    assert "phishing" in s["category_names"]
    assert "agentic-risks" in s["category_names"]


def test_expand_count_with_filters():
    count = expand_count(categories=["phishing"], difficulties=["easy", "hard"])
    summary = expand_summary()
    assert count == summary["techniques"] * 1 * 2
