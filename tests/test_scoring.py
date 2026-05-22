from ai_blackteam.scoring import score_results


def test_all_blocked_is_100():
    results = [
        {"attack": "a", "verdict": "BLOCKED"},
        {"attack": "b", "verdict": "BLOCKED"},
    ]
    scores = score_results(results)
    assert scores["overall_score"] == 100.0
    assert scores["blocked"] == 2
    assert scores["bypassed"] == 0


def test_all_bypassed_is_0():
    results = [
        {"attack": "a", "verdict": "BYPASSED"},
        {"attack": "b", "verdict": "BYPASSED"},
    ]
    scores = score_results(results)
    assert scores["overall_score"] == 0.0
    assert scores["bypassed"] == 2


def test_mixed_results():
    results = [
        {"attack": "a", "verdict": "BLOCKED"},
        {"attack": "b", "verdict": "BYPASSED"},
    ]
    scores = score_results(results)
    assert 0 < scores["overall_score"] < 100


def test_severity_weighting():
    metadata = {
        "critical_attack": {"severity": "critical", "category": "weapons"},
        "low_attack": {"severity": "low", "category": "encoding"},
    }
    # Critical bypassed + low blocked = should be below 50% (critical weighs more)
    results = [
        {"attack": "critical_attack", "verdict": "BYPASSED"},
        {"attack": "low_attack", "verdict": "BLOCKED"},
    ]
    scores = score_results(results, metadata)
    assert scores["overall_score"] < 50


def test_empty_results():
    scores = score_results([])
    assert scores["overall_score"] == 100.0
    assert scores["total"] == 0


def test_category_scores():
    metadata = {
        "a": {"severity": "medium", "category": "phishing"},
        "b": {"severity": "medium", "category": "malware"},
    }
    results = [
        {"attack": "a", "verdict": "BLOCKED"},
        {"attack": "b", "verdict": "BYPASSED"},
    ]
    scores = score_results(results, metadata)
    assert scores["category_scores"]["phishing"]["score"] == 100.0
    assert scores["category_scores"]["malware"]["score"] == 0.0
