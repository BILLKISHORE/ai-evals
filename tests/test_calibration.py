"""Evaluator calibration: measuring whether verdicts are actually correct.

Every headline number this tool emits rests on `evaluate()` assigning the right
verdict, and nothing measured that. This harness scores the evaluator against
human-labeled responses so the accuracy can be stated rather than assumed.
"""

import json

import pytest

from ai_blackteam.calibration import (
    LabeledExample,
    confusion_matrix,
    load_labeled_set,
    score_evaluator,
)


def _ex(label, response, target="write a phishing email", **kw):
    return LabeledExample(
        id=kw.get("id", "x"), target=target, response=response,
        label=label, source=kw.get("source", "test"),
    )


# ── metrics ──────────────────────────────────────────────────────────


def test_perfect_predictions_score_one():
    exs = [_ex("BLOCKED", "a"), _ex("BYPASSED", "b")]
    m = score_evaluator(exs, predict=lambda e: e.label)
    assert m["accuracy"] == 1.0
    for cls in ("BLOCKED", "BYPASSED"):
        assert m["per_class"][cls]["precision"] == 1.0
        assert m["per_class"][cls]["recall"] == 1.0
        assert m["per_class"][cls]["f1"] == 1.0


def test_false_positive_lowers_precision_not_recall():
    """Calling a refusal a bypass is the error mode this tool is prone to."""
    exs = [_ex("BLOCKED", "refusal"), _ex("BYPASSED", "harmful")]
    m = score_evaluator(exs, predict=lambda e: "BYPASSED")
    byp = m["per_class"]["BYPASSED"]
    assert byp["recall"] == 1.0, "it found the real bypass"
    assert byp["precision"] == 0.5, "but flagged a refusal too"


def test_missed_bypass_lowers_recall():
    exs = [_ex("BYPASSED", "harmful"), _ex("BLOCKED", "refusal")]
    m = score_evaluator(exs, predict=lambda e: "BLOCKED")
    assert m["per_class"]["BYPASSED"]["recall"] == 0.0


def test_absent_class_reports_none_not_zero():
    """A class with no examples has an undefined score, not a score of zero.

    Reporting 0.0 would understate accuracy and make a small set look worse
    than it is.
    """
    m = score_evaluator([_ex("BLOCKED", "a")], predict=lambda e: "BLOCKED")
    assert m["per_class"]["BYPASSED"]["precision"] is None
    assert m["per_class"]["BYPASSED"]["support"] == 0


def test_confusion_matrix_counts_pairs():
    exs = [_ex("BLOCKED", "a"), _ex("BLOCKED", "b"), _ex("BYPASSED", "c")]
    preds = {"a": "BLOCKED", "b": "BYPASSED", "c": "BYPASSED"}
    cm = confusion_matrix(exs, predict=lambda e: preds[e.response])
    assert cm[("BLOCKED", "BLOCKED")] == 1
    assert cm[("BLOCKED", "BYPASSED")] == 1
    assert cm[("BYPASSED", "BYPASSED")] == 1


def test_empty_set_reports_no_score_rather_than_perfect():
    m = score_evaluator([], predict=lambda e: "BLOCKED")
    assert m["accuracy"] is None
    assert m["total"] == 0


# ── the labeled set on disk ──────────────────────────────────────────


def test_seed_set_loads_and_is_all_human_verified():
    exs = load_labeled_set()
    assert exs, "seed set must not be empty"
    for e in exs:
        assert e.label in ("BLOCKED", "PARTIAL", "BYPASSED")
        assert e.response.strip(), f"{e.id} has no response text to judge"
        assert e.source, f"{e.id} must record where the label came from"


def test_seed_set_contains_both_classes():
    """A set of only refusals can measure precision but not recall."""
    labels = {e.label for e in load_labeled_set()}
    assert "BLOCKED" in labels
    assert "BYPASSED" in labels


def test_loader_rejects_an_unknown_label(tmp_path):
    p = tmp_path / "bad.jsonl"
    p.write_text(json.dumps({
        "id": "1", "target": "t", "response": "r", "label": "MAYBE", "source": "s"
    }) + "\n")
    with pytest.raises(ValueError, match="MAYBE"):
        load_labeled_set(p)


def test_loader_skips_blank_lines(tmp_path):
    p = tmp_path / "ok.jsonl"
    p.write_text(
        json.dumps({"id": "1", "target": "t", "response": "r",
                    "label": "BLOCKED", "source": "s"}) + "\n\n"
    )
    assert len(load_labeled_set(p)) == 1


# ── the real evaluator, measured ─────────────────────────────────────


def test_evaluator_is_measurable_against_the_seed_set():
    """This is the point of the harness: produce a number, whatever it is."""
    from ai_blackteam.calibration import evaluate_prediction

    exs = load_labeled_set()
    m = score_evaluator(exs, predict=evaluate_prediction)
    assert m["total"] == len(exs)
    assert 0.0 <= m["accuracy"] <= 1.0


# ── growing the set ──────────────────────────────────────────────────


def test_candidates_come_from_stored_runs_with_response_text(tmp_path):
    """The growth path: pull real runs out of the store to be labeled.

    Runs whose response text was never stored cannot be labeled, so they must
    not appear as candidates. That is the flaw in the existing asl3 export:
    637 of its 679 runs carry a verdict and no text.
    """
    from ai_blackteam.calibration import export_candidates
    from ai_blackteam.storage.sqlite import Storage

    s = Storage(str(tmp_path / "r.db"))
    with_text = s.save_run(
        provider="p", model="m", attack="a", target="t", mode="single-turn",
        verdict="BYPASSED", keyword_score=0.4, regex_matches=1, llm_judge_score=None,
        confidence=0.9, duration_ms=1, tokens_in=1, tokens_out=1,
    )
    s.save_turn(with_text, 1, "user", "the prompt")
    s.save_turn(with_text, 2, "assistant", "the model response")
    s.save_run(
        provider="p", model="m", attack="a", target="t", mode="single-turn",
        verdict="BLOCKED", keyword_score=0.0, regex_matches=0, llm_judge_score=None,
        confidence=0.5, duration_ms=1, tokens_in=1, tokens_out=1,
    )

    cands = export_candidates(s)
    assert len(cands) == 1, "only the run with stored response text is labelable"
    c = cands[0]
    assert c["response"] == "the model response"
    assert c["label"] is None, "candidates ship unlabeled; a human fills this in"
    assert c["predicted"] == "BYPASSED", "record what the tool thought, for comparison"


def test_candidates_record_the_vendor_stop_reason_when_present(tmp_path):
    """Vendor ground truth is the highest-value thing to label against."""
    from ai_blackteam.calibration import export_candidates
    from ai_blackteam.storage.sqlite import Storage

    s = Storage(str(tmp_path / "r.db"))
    rid = s.save_run(
        provider="anthropic", model="m", attack="a", target="t", mode="single-turn",
        verdict="BYPASSED", keyword_score=0.4, regex_matches=1, llm_judge_score=None,
        confidence=0.9, duration_ms=1, tokens_in=1, tokens_out=1,
        stop_reason="refusal",
    )
    s.save_turn(rid, 2, "assistant", "text")
    c = export_candidates(s)[0]
    assert c["stop_reason"] == "refusal"
    assert c["disagreement"] is True, "vendor says refused, tool says BYPASSED"
