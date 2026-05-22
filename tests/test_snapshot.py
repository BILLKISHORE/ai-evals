"""Tests for snapshot-based longitudinal tracking."""

import json
from ai_blackteam.storage.sqlite import Storage
from ai_blackteam.snapshot import SnapshotManager


def _make_storage():
    return Storage(":memory:")


def _seed_runs(storage, provider="anthropic", model="claude-opus-4.6",
               attack="vuln-research-synthetic", target="test",
               verdicts=None):
    if verdicts is None:
        verdicts = ["BYPASSED", "BLOCKED", "BLOCKED", "PARTIAL", "BLOCKED"]
    run_ids = []
    for v in verdicts:
        rid = storage.save_run(
            provider=provider, model=model, attack=attack,
            target=target, mode="single-turn", verdict=v,
            keyword_score=0.5 if v == "BYPASSED" else 0.0,
            regex_matches=1 if v == "BYPASSED" else 0,
            llm_judge_score=None, confidence=0.8 if v == "BYPASSED" else 0.2,
            duration_ms=100, tokens_in=50, tokens_out=100,
        )
        run_ids.append(rid)
    return run_ids


def test_create_snapshot():
    storage = _make_storage()
    run_ids = _seed_runs(storage)
    mgr = SnapshotManager(storage)

    snap_id = mgr.create(
        name="test-snapshot-1",
        run_ids=run_ids,
        provider="anthropic",
        model="claude-opus-4.6",
        attack_suite="vuln-research-synthetic",
        target="test",
    )
    assert snap_id is not None
    assert snap_id > 0


def test_list_snapshots():
    storage = _make_storage()
    run_ids = _seed_runs(storage)
    mgr = SnapshotManager(storage)

    mgr.create(name="snap-1", run_ids=run_ids, provider="anthropic",
               model="claude-opus-4.6", attack_suite="all", target="test")
    mgr.create(name="snap-2", run_ids=run_ids, provider="openai",
               model="gpt-5.4", attack_suite="all", target="test")

    snapshots = mgr.list_all()
    assert len(snapshots) == 2
    assert snapshots[0]["name"] == "snap-1"


def test_snapshot_bypass_rate():
    storage = _make_storage()
    run_ids = _seed_runs(storage, verdicts=["BYPASSED", "BYPASSED", "BLOCKED", "BLOCKED", "BLOCKED"])
    mgr = SnapshotManager(storage)

    snap_id = mgr.create(name="rate-test", run_ids=run_ids, provider="anthropic",
                         model="test", attack_suite="all", target="test")
    snap = mgr.get(snap_id)
    assert snap["bypass_rate"] == 0.4
    assert snap["bypassed"] == 2
    assert snap["blocked"] == 3


def test_diff_snapshots():
    storage = _make_storage()
    mgr = SnapshotManager(storage)

    ids1 = _seed_runs(storage, verdicts=["BYPASSED", "BYPASSED", "BLOCKED", "BLOCKED", "BLOCKED"])
    snap1 = mgr.create(name="before", run_ids=ids1, provider="anthropic",
                       model="claude-v1", attack_suite="all", target="test")

    ids2 = _seed_runs(storage, verdicts=["BYPASSED", "BLOCKED", "BLOCKED", "BLOCKED", "BLOCKED"])
    snap2 = mgr.create(name="after", run_ids=ids2, provider="anthropic",
                       model="claude-v2", attack_suite="all", target="test")

    diff = mgr.diff(snap1, snap2)
    assert diff["before"]["bypass_rate"] == 0.4
    assert diff["after"]["bypass_rate"] == 0.2
    assert diff["delta"] < 0


def test_get_nonexistent_snapshot():
    storage = _make_storage()
    mgr = SnapshotManager(storage)
    assert mgr.get(999) is None
