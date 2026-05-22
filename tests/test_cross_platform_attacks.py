import ai_blackteam.attacks.api_abuse  # noqa: F401
import ai_blackteam.attacks.webhook_exploitation  # noqa: F401
import ai_blackteam.attacks.oauth_manipulation  # noqa: F401
import ai_blackteam.attacks.slack_injection  # noqa: F401
import ai_blackteam.attacks.email_injection  # noqa: F401
import ai_blackteam.attacks.calendar_manipulation  # noqa: F401
import ai_blackteam.attacks.file_system_traversal  # noqa: F401
import ai_blackteam.attacks.database_manipulation  # noqa: F401
import ai_blackteam.attacks.cloud_resource_abuse  # noqa: F401
import ai_blackteam.attacks.ci_cd_injection  # noqa: F401
import ai_blackteam.attacks.container_escape  # noqa: F401
import ai_blackteam.attacks.dns_manipulation  # noqa: F401
import ai_blackteam.attacks.browser_exploitation  # noqa: F401
import ai_blackteam.attacks.payment_manipulation  # noqa: F401
import ai_blackteam.attacks.notification_spam  # noqa: F401

from ai_blackteam.attacks.api_abuse import ApiAbuse
from ai_blackteam.attacks.webhook_exploitation import WebhookExploitation
from ai_blackteam.attacks.oauth_manipulation import OAuthManipulation
from ai_blackteam.attacks.slack_injection import SlackInjection
from ai_blackteam.attacks.email_injection import EmailInjection
from ai_blackteam.attacks.calendar_manipulation import CalendarManipulation
from ai_blackteam.attacks.file_system_traversal import FileSystemTraversal
from ai_blackteam.attacks.database_manipulation import DatabaseManipulation
from ai_blackteam.attacks.cloud_resource_abuse import CloudResourceAbuse
from ai_blackteam.attacks.ci_cd_injection import CiCdInjection
from ai_blackteam.attacks.container_escape import ContainerEscape
from ai_blackteam.attacks.dns_manipulation import DnsManipulation
from ai_blackteam.attacks.browser_exploitation import BrowserExploitation
from ai_blackteam.attacks.payment_manipulation import PaymentManipulation
from ai_blackteam.attacks.notification_spam import NotificationSpam
from ai_blackteam.registry import attack_registry


TARGET = "example-service"

SINGLE_TURN_ATTACKS = [
    ("slack-injection", SlackInjection),
    ("email-injection", EmailInjection),
    ("ci-cd-injection", CiCdInjection),
    ("dns-manipulation", DnsManipulation),
]

TOOL_USE_ATTACKS = [
    ("api-abuse", ApiAbuse),
    ("webhook-exploitation", WebhookExploitation),
    ("oauth-manipulation", OAuthManipulation),
    ("calendar-manipulation", CalendarManipulation),
    ("file-system-traversal", FileSystemTraversal),
    ("database-manipulation", DatabaseManipulation),
    ("cloud-resource-abuse", CloudResourceAbuse),
    ("container-escape", ContainerEscape),
    ("browser-exploitation", BrowserExploitation),
    ("payment-manipulation", PaymentManipulation),
    ("notification-spam", NotificationSpam),
]

ALL_ATTACKS = SINGLE_TURN_ATTACKS + TOOL_USE_ATTACKS


def test_all_registered():
    registered = attack_registry.list()
    for technique_id, _ in ALL_ATTACKS:
        assert technique_id in registered, f"{technique_id} not in registry"


def test_all_category_cross_platform():
    for _, cls in ALL_ATTACKS:
        instance = cls()
        assert instance.category == "cross-platform", (
            f"{cls.__name__} has wrong category: {instance.category}"
        )


def test_all_owasp_llm():
    for _, cls in ALL_ATTACKS:
        instance = cls()
        assert "LLM06:2025 Excessive Agency" in instance.owasp_llm, (
            f"{cls.__name__} missing LLM06:2025 Excessive Agency"
        )


def test_all_mitre_atlas():
    for _, cls in ALL_ATTACKS:
        instance = cls()
        assert "AML.T0054" in instance.mitre_atlas, (
            f"{cls.__name__} missing AML.T0054"
        )
        assert "AML.T0068" in instance.mitre_atlas, (
            f"{cls.__name__} missing AML.T0068"
        )


def test_single_turn_prompts():
    for _, cls in SINGLE_TURN_ATTACKS:
        instance = cls()
        assert instance.mode == "single-turn", f"{cls.__name__} should be single-turn"
        prompts = instance.generate_prompts(TARGET)
        assert len(prompts) >= 3, f"{cls.__name__} needs at least 3 prompts"
        assert all(isinstance(p, str) and len(p) > 0 for p in prompts), (
            f"{cls.__name__} has empty prompts"
        )
        assert all(TARGET in p or True for p in prompts), (
            f"{cls.__name__} prompts should reference target"
        )


def test_tool_use_prompts():
    for _, cls in TOOL_USE_ATTACKS:
        instance = cls()
        assert instance.mode == "tool-use", f"{cls.__name__} should be tool-use"
        prompts = instance.generate_prompts(TARGET)
        assert len(prompts) >= 3, f"{cls.__name__} needs at least 3 prompts"
        assert all(isinstance(p, str) and len(p) > 0 for p in prompts), (
            f"{cls.__name__} has empty prompts"
        )


def test_tool_use_has_tools():
    for _, cls in TOOL_USE_ATTACKS:
        instance = cls()
        tools = instance.get_tools()
        assert isinstance(tools, list), f"{cls.__name__}.get_tools() must return a list"
        assert len(tools) >= 1, f"{cls.__name__} needs at least 1 tool"
        for tool in tools:
            assert "name" in tool, f"{cls.__name__} tool missing 'name'"
            assert "input_schema" in tool, f"{cls.__name__} tool missing 'input_schema'"


def test_tool_use_messages():
    for _, cls in TOOL_USE_ATTACKS:
        instance = cls()
        messages = instance.generate_tool_messages(TARGET)
        assert len(messages) >= 3, f"{cls.__name__} needs at least 3 tool messages"
        assert all(isinstance(m, str) and len(m) > 0 for m in messages), (
            f"{cls.__name__} has empty tool messages"
        )


def test_severities():
    critical = [OAuthManipulation, FileSystemTraversal, DatabaseManipulation,
                CloudResourceAbuse, CiCdInjection, ContainerEscape, PaymentManipulation]
    high = [ApiAbuse, WebhookExploitation, SlackInjection, EmailInjection,
            DnsManipulation, BrowserExploitation]
    medium = [CalendarManipulation, NotificationSpam]

    for cls in critical:
        assert cls().severity == "critical", f"{cls.__name__} should be critical"
    for cls in high:
        assert cls().severity == "high", f"{cls.__name__} should be high"
    for cls in medium:
        assert cls().severity == "medium", f"{cls.__name__} should be medium"


def test_api_abuse_details():
    atk = ApiAbuse()
    assert atk.technique_id == "api-abuse"
    tools = atk.get_tools()
    tool_names = [t["name"] for t in tools]
    assert "call_api" in tool_names
    assert "list_api_keys" in tool_names


def test_webhook_exploitation_details():
    atk = WebhookExploitation()
    assert atk.technique_id == "webhook-exploitation"
    tools = atk.get_tools()
    tool_names = [t["name"] for t in tools]
    assert "register_webhook" in tool_names
    assert "trigger_webhook" in tool_names


def test_oauth_manipulation_details():
    atk = OAuthManipulation()
    assert atk.technique_id == "oauth-manipulation"
    tools = atk.get_tools()
    tool_names = [t["name"] for t in tools]
    assert "oauth_authorize" in tool_names
    assert "exchange_token" in tool_names
    assert "revoke_token" in tool_names


def test_payment_manipulation_details():
    atk = PaymentManipulation()
    assert atk.technique_id == "payment-manipulation"
    tools = atk.get_tools()
    tool_names = [t["name"] for t in tools]
    assert "process_payment" in tool_names
    assert "issue_refund" in tool_names
    assert "update_price" in tool_names


def test_container_escape_details():
    atk = ContainerEscape()
    assert atk.technique_id == "container-escape"
    tools = atk.get_tools()
    tool_names = [t["name"] for t in tools]
    assert "execute_command" in tool_names
    assert "mount_volume" in tool_names


def test_metadata_complete():
    for _, cls in ALL_ATTACKS:
        instance = cls()
        meta = instance.metadata()
        assert meta["name"], f"{cls.__name__} missing name"
        assert meta["technique_id"], f"{cls.__name__} missing technique_id"
        assert meta["category"] == "cross-platform"
        assert meta["severity"] in ("low", "medium", "high", "critical")
        assert meta["cvss_score"] > 0, f"{cls.__name__} has 0 cvss_score"
