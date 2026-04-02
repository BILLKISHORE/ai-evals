from mordor.attacks.base import BaseAttack
from mordor.taxonomy import severity_to_cvss, SEVERITY_TO_CVSS


def test_severity_to_cvss_critical():
    assert severity_to_cvss("critical") == 9.5


def test_severity_to_cvss_high():
    assert severity_to_cvss("high") == 7.5


def test_severity_to_cvss_medium():
    assert severity_to_cvss("medium") == 5.0


def test_severity_to_cvss_low():
    assert severity_to_cvss("low") == 2.5


def test_severity_to_cvss_unknown_defaults():
    assert severity_to_cvss("unknown") == 5.0


def test_cvss_score_in_metadata_auto_assigned():
    class _TestAttack(BaseAttack):
        name = "test"
        technique_id = "test-cvss"
        severity = "high"

        def generate_prompts(self, target, **kwargs):
            return [target]

    meta = _TestAttack().metadata()
    assert meta["cvss_score"] == 7.5


def test_cvss_score_explicit_overrides_auto():
    class _TestAttack(BaseAttack):
        name = "test"
        technique_id = "test-cvss-explicit"
        severity = "high"
        cvss_score = 8.2

        def generate_prompts(self, target, **kwargs):
            return [target]

    meta = _TestAttack().metadata()
    assert meta["cvss_score"] == 8.2


def test_severity_to_cvss_map_has_four_entries():
    assert len(SEVERITY_TO_CVSS) == 4
