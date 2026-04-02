from mordor.attacks.agent_session_smuggling import AgentSessionSmuggling
from mordor.attacks.agent_collusion import AgentCollusion
from mordor.attacks.agent_impersonation import AgentImpersonation
from mordor.attacks.cascading_jailbreak import CascadingJailbreak
from mordor.attacks.agent_delegation_abuse import AgentDelegationAbuse
from mordor.registry import attack_registry
import mordor.attacks.agent_session_smuggling  # noqa: F401 - triggers registration
import mordor.attacks.agent_collusion  # noqa: F401
import mordor.attacks.agent_impersonation  # noqa: F401
import mordor.attacks.cascading_jailbreak  # noqa: F401
import mordor.attacks.agent_delegation_abuse  # noqa: F401


TARGET = "multi-agent system"

MULTI_TURN_ATTACKS = [
    ("agent-session-smuggling", AgentSessionSmuggling),
    ("agent-collusion", AgentCollusion),
    ("agent-impersonation", AgentImpersonation),
    ("cascading-jailbreak", CascadingJailbreak),
]

TOOL_USE_ATTACKS = [
    ("agent-delegation-abuse", AgentDelegationAbuse),
]


def test_all_registered():
    registered = attack_registry.list()
    for technique_id, _ in MULTI_TURN_ATTACKS + TOOL_USE_ATTACKS:
        assert technique_id in registered, f"{technique_id} not registered"


def test_correct_category():
    for _, cls in MULTI_TURN_ATTACKS + TOOL_USE_ATTACKS:
        instance = cls()
        assert instance.category == "multi-agent-exploitation", (
            f"{cls.__name__} has wrong category: {instance.category}"
        )


def test_owasp_agentic_set():
    for _, cls in MULTI_TURN_ATTACKS + TOOL_USE_ATTACKS:
        instance = cls()
        assert len(instance.owasp_agentic) > 0, (
            f"{cls.__name__} has no owasp_agentic mappings"
        )


def test_session_smuggling_prompts_and_turns():
    atk = AgentSessionSmuggling()
    assert atk.mode == "multi-turn"
    assert atk.severity == "critical"

    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)

    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 3
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)


def test_agent_collusion_prompts_and_turns():
    atk = AgentCollusion()
    assert atk.mode == "multi-turn"
    assert atk.severity == "high"

    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)

    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 3
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)


def test_agent_impersonation_prompts_and_turns():
    atk = AgentImpersonation()
    assert atk.mode == "multi-turn"
    assert atk.severity == "critical"

    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)

    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 3
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)


def test_cascading_jailbreak_prompts_and_turns():
    atk = CascadingJailbreak()
    assert atk.mode == "multi-turn"
    assert atk.severity == "critical"

    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)

    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 3
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)


def test_delegation_abuse_tool_use():
    atk = AgentDelegationAbuse()
    assert atk.mode == "tool-use"
    assert atk.severity == "critical"

    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)

    messages = atk.generate_tool_messages(TARGET)
    assert len(messages) >= 3
    assert all(isinstance(m, str) and len(m) > 0 for m in messages)

    tools = atk.get_tools()
    assert isinstance(tools, list)
    assert len(tools) >= 3
    tool_names = [t["name"] for t in tools]
    assert "delegate_task" in tool_names
    assert "request_approval" in tool_names
    assert "execute_action" in tool_names
    for tool in tools:
        assert "name" in tool
        assert "input_schema" in tool
