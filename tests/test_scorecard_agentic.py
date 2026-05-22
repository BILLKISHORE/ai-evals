from ai_blackteam.scorecard import generate_agentic_scorecard


def _make_runs(attack, verdicts):
    return [
        {"attack": attack, "verdict": v, "provider": "anthropic", "model": "claude-test"}
        for v in verdicts
    ]


def test_agentic_scorecard_returns_ten_categories():
    runs = _make_runs("agent-credential-theft", ["BLOCKED", "BLOCKED", "BYPASSED"])
    result = generate_agentic_scorecard(runs)
    assert len(result["categories"]) == 10


def test_agentic_scorecard_all_asi_codes_present():
    runs = _make_runs("agent-credential-theft", ["BLOCKED"])
    result = generate_agentic_scorecard(runs)
    expected_codes = [f"ASI0{i}" for i in range(1, 10)] + ["ASI10"]
    for code in expected_codes:
        assert code in result["categories"], f"{code} missing from scorecard"


def test_agentic_scorecard_calculates_block_rate():
    runs = _make_runs("agent-credential-theft", ["BLOCKED", "BLOCKED", "BYPASSED"])
    result = generate_agentic_scorecard(runs)
    asi02 = result["categories"]["ASI02"]
    assert asi02["blocked"] == 2
    assert asi02["total"] == 3
    assert abs(asi02["block_rate"] - 66.67) < 0.1


def test_agentic_scorecard_untested_categories_are_na():
    runs = _make_runs("agent-credential-theft", ["BLOCKED"])
    result = generate_agentic_scorecard(runs)
    asi05 = result["categories"]["ASI05"]
    assert asi05["rating"] == "N/A"
    assert asi05["total"] == 0


def test_agentic_scorecard_overall_score_is_float():
    runs = _make_runs("agent-credential-theft", ["BLOCKED", "BYPASSED"])
    result = generate_agentic_scorecard(runs)
    assert isinstance(result["overall_score"], float)
    assert 0.0 <= result["overall_score"] <= 100.0


def test_agentic_scorecard_empty_runs_returns_all_na():
    result = generate_agentic_scorecard([])
    assert result["overall_score"] == 0.0
    for code, cat in result["categories"].items():
        assert cat["rating"] == "N/A"
