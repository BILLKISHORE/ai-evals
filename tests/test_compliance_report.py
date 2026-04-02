from mordor.scorecard import generate_compliance_report


def _make_runs(attack, verdicts):
    return [
        {"attack": attack, "verdict": v, "provider": "test", "model": "test"}
        for v in verdicts
    ]


def test_compliance_report_has_both_frameworks():
    result = generate_compliance_report([])
    assert "eu_ai_act" in result
    assert "nist_ai_rmf" in result


def test_compliance_report_eu_has_four_levels():
    result = generate_compliance_report([])
    assert len(result["eu_ai_act"]) == 4


def test_compliance_report_nist_has_four_pillars():
    result = generate_compliance_report([])
    assert len(result["nist_ai_rmf"]) == 4


def test_compliance_report_empty_runs_all_na():
    result = generate_compliance_report([])
    assert result["overall_score"] == 0.0
    for cat in result["eu_ai_act"].values():
        assert cat["rating"] == "N/A"


def test_compliance_report_overall_is_float():
    runs = _make_runs("encoding-obfuscation", ["BLOCKED", "BYPASSED"])
    result = generate_compliance_report(runs)
    assert isinstance(result["overall_score"], float)
