from ai_blackteam.attacks.base import BaseAttack
from ai_blackteam.registry import attack_registry


def test_base_attack_has_owasp_agentic_field():
    assert hasattr(BaseAttack, "owasp_agentic")
    assert BaseAttack.owasp_agentic == []


def test_base_attack_metadata_includes_owasp_agentic():
    class _TestAttack(BaseAttack):
        name = "test"
        technique_id = "test-attack"
        owasp_agentic = ["ASI01", "ASI02"]

        def generate_prompts(self, target, **kwargs):
            return [target]

    attack = _TestAttack()
    meta = attack.metadata()
    assert "owasp_agentic" in meta
    assert meta["owasp_agentic"] == ["ASI01", "ASI02"]


def test_all_registered_agent_attacks_have_owasp_agentic():
    try:
        from ai_blackteam._loader import load_attacks
        load_attacks()
    except Exception:
        pass

    for name, attack_cls in attack_registry.items():
        instance = attack_cls()
        if instance.category == "agent-exploitation":
            assert len(instance.owasp_agentic) > 0, (
                f"Agent attack '{name}' has no owasp_agentic mappings"
            )
