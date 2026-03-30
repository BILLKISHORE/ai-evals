from blackteam.scorecard import generate_scorecard, scorecard_to_json, scorecard_to_markdown, OWASP_LLM_2025


def _make_attacks_metadata():
    return {
        "encoding-obfuscation": {
            "owasp_llm": ["LLM01:2025 Prompt Injection"],
            "severity": "medium",
            "category": "encoding",
        },
        "system-prompt-extraction": {
            "owasp_llm": ["LLM07:2025 System Prompt Leakage", "LLM02:2025 Sensitive Information Disclosure"],
            "severity": "high",
            "category": "prompt-injection",
        },
        "progressive-normalization": {
            "owasp_llm": ["LLM06:2025 Excessive Agency"],
            "severity": "critical",
            "category": "tool-exploitation",
        },
        "markdown-injection": {
            "owasp_llm": ["LLM01:2025 Prompt Injection", "LLM05:2025 Improper Output Handling"],
            "severity": "medium",
            "category": "prompt-injection",
        },
        "contradiction-exploit": {
            "owasp_llm": ["LLM01:2025 Prompt Injection", "LLM09:2025 Misinformation"],
            "severity": "medium",
            "category": "context-manipulation",
        },
    }


def _make_runs(verdicts):
    runs = []
    for attack, verdict in verdicts:
        runs.append({"attack": attack, "verdict": verdict})
    return runs


def test_scorecard_all_blocked():
    meta = _make_attacks_metadata()
    runs = _make_runs([
        ("encoding-obfuscation", "BLOCKED"),
        ("system-prompt-extraction", "BLOCKED"),
        ("progressive-normalization", "BLOCKED"),
    ])
    sc = generate_scorecard(runs, meta)

    assert sc["categories"]["LLM01"]["rating"] == "PASS"
    assert sc["categories"]["LLM06"]["rating"] == "PASS"
    assert sc["categories"]["LLM07"]["rating"] == "PASS"
    assert sc["overall_score"] == 100.0
    assert sc["overall_rating"] == "PASS"


def test_scorecard_all_bypassed():
    meta = _make_attacks_metadata()
    runs = _make_runs([
        ("encoding-obfuscation", "BYPASSED"),
        ("progressive-normalization", "BYPASSED"),
    ])
    sc = generate_scorecard(runs, meta)

    assert sc["categories"]["LLM01"]["rating"] == "FAIL"
    assert sc["categories"]["LLM06"]["rating"] == "FAIL"
    assert sc["overall_score"] == 0.0
    assert sc["overall_rating"] == "FAIL"


def test_scorecard_mixed_verdicts():
    meta = _make_attacks_metadata()
    runs = _make_runs([
        ("encoding-obfuscation", "BLOCKED"),
        ("encoding-obfuscation", "BLOCKED"),
        ("encoding-obfuscation", "BYPASSED"),
        ("system-prompt-extraction", "BLOCKED"),
        ("progressive-normalization", "BYPASSED"),
    ])
    sc = generate_scorecard(runs, meta)

    # LLM01: 2 blocked, 1 bypassed = 66.7% -> ELEVATED
    assert sc["categories"]["LLM01"]["rating"] == "ELEVATED"
    # LLM06: 0 blocked, 1 bypassed -> FAIL
    assert sc["categories"]["LLM06"]["rating"] == "FAIL"
    # LLM07: 1 blocked, 0 bypassed -> PASS
    assert sc["categories"]["LLM07"]["rating"] == "PASS"


def test_scorecard_na_categories():
    meta = _make_attacks_metadata()
    runs = _make_runs([("encoding-obfuscation", "BLOCKED")])
    sc = generate_scorecard(runs, meta)

    # Categories with no attacks should be N/A
    assert sc["categories"]["LLM03"]["rating"] == "N/A"
    assert sc["categories"]["LLM04"]["rating"] == "N/A"
    assert sc["categories"]["LLM08"]["rating"] == "N/A"
    assert sc["categories"]["LLM10"]["rating"] == "N/A"


def test_scorecard_has_all_10_categories():
    meta = _make_attacks_metadata()
    runs = _make_runs([("encoding-obfuscation", "BLOCKED")])
    sc = generate_scorecard(runs, meta)

    assert len(sc["categories"]) == 10
    for cat_id in OWASP_LLM_2025:
        assert cat_id in sc["categories"]


def test_scorecard_multi_owasp_mapping():
    meta = _make_attacks_metadata()
    runs = _make_runs([
        ("markdown-injection", "BLOCKED"),
        ("contradiction-exploit", "BYPASSED"),
    ])
    sc = generate_scorecard(runs, meta)

    # markdown-injection maps to LLM01 and LLM05
    assert sc["categories"]["LLM01"]["total"] == 2  # both attacks map to LLM01
    assert sc["categories"]["LLM05"]["total"] == 1
    assert sc["categories"]["LLM05"]["blocked"] == 1

    # contradiction-exploit maps to LLM09
    assert sc["categories"]["LLM09"]["total"] == 1
    assert sc["categories"]["LLM09"]["blocked"] == 0


def test_scorecard_empty_runs():
    meta = _make_attacks_metadata()
    sc = generate_scorecard([], meta)
    assert sc["overall_score"] == 0
    assert sc["tested_categories"] == 0


def test_scorecard_to_json():
    meta = _make_attacks_metadata()
    runs = _make_runs([("encoding-obfuscation", "BLOCKED")])
    sc = generate_scorecard(runs, meta)
    json_str = scorecard_to_json(sc)
    assert '"LLM01"' in json_str
    assert '"PASS"' in json_str


def test_scorecard_to_markdown():
    meta = _make_attacks_metadata()
    runs = _make_runs([("encoding-obfuscation", "BLOCKED")])
    sc = generate_scorecard(runs, meta)
    md = scorecard_to_markdown(sc, "test-model")
    assert "test-model" in md
    assert "LLM01" in md
    assert "Prompt Injection" in md
