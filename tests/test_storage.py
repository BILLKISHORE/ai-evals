import tempfile
from ai_blackteam.storage.sqlite import Storage


def test_save_and_list_runs():
    with tempfile.NamedTemporaryFile(suffix=".db") as f:
        db = Storage(f.name)
        run_id = db.save_run(
            provider="anthropic", model="claude-sonnet-4-6",
            attack="encoding-obfuscation", target="test target",
            mode="single-turn", verdict="BYPASSED",
            keyword_score=0.6, regex_matches=2, llm_judge_score=None,
            confidence=0.8, duration_ms=1234, tokens_in=100, tokens_out=50,
        )
        assert run_id == 1
        runs = db.list_runs()
        assert len(runs) == 1
        assert runs[0]["verdict"] == "BYPASSED"


def test_save_turns():
    with tempfile.NamedTemporaryFile(suffix=".db") as f:
        db = Storage(f.name)
        run_id = db.save_run("anthropic", "claude", "role-play", "test",
                             "multi-turn", "BLOCKED", 0, 0, None, 0, 100, 10, 5)
        db.save_turn(run_id, 1, "user", "hello")
        db.save_turn(run_id, 2, "assistant", "hi there")
        turns = db.get_turns(run_id)
        assert len(turns) == 2
        assert turns[0]["role"] == "user"


# ── The results DB holds full attack transcripts ─────────────────────


def test_results_db_is_not_world_readable(tmp_path):
    import os, stat
    from ai_blackteam.storage.sqlite import Storage
    db = tmp_path / "results.db"
    Storage(str(db))
    mode = stat.S_IMODE(os.stat(db).st_mode)
    assert mode == 0o600, f"expected 0600, got {oct(mode)}"


def test_in_memory_storage_still_works():
    """':memory:' has no file to chmod; must not raise."""
    from ai_blackteam.storage.sqlite import Storage
    s = Storage(":memory:")
    assert s.db_path == ":memory:"


def test_storage_creates_a_missing_parent_directory(tmp_path):
    """First run on a clean machine: nothing has created ~/.ai_blackteam yet.

    Only save_config() used to create that directory, so any entry point that
    did not save config first (env-var keys, ollama, a bare `run`) crashed with
    an unhandled sqlite3.OperationalError.
    """
    from ai_blackteam.storage.sqlite import Storage
    db = tmp_path / "does-not-exist-yet" / "results.db"
    assert not db.parent.exists()
    Storage(str(db))
    assert db.exists()


def test_storage_keeps_the_tool_directory_private(tmp_path, monkeypatch):
    import os, stat
    import ai_blackteam.config as cfg
    from ai_blackteam.storage.sqlite import Storage
    fake = tmp_path / ".ai_blackteam"
    monkeypatch.setattr(cfg, "DEFAULT_CONFIG_DIR", fake)
    Storage(str(fake / "results.db"))
    assert stat.S_IMODE(os.stat(fake).st_mode) == 0o700


def test_run_row_records_the_vendor_stop_reason(tmp_path):
    """The vendor's own refusal signal has to survive into the store.

    Without it the calibration set cannot compare vendor ground truth against
    the evaluator's text inference, which is the measurement that decides
    which signal should be authoritative.
    """
    from ai_blackteam.storage.sqlite import Storage
    s = Storage(str(tmp_path / "r.db"))
    rid = s.save_run(
        provider="anthropic", model="m", attack="a", target="t", mode="single-turn",
        verdict="BLOCKED", keyword_score=0.0, regex_matches=0, llm_judge_score=None,
        confidence=0.5, duration_ms=1, tokens_in=1, tokens_out=1,
        stop_reason="refusal", stop_details='{"policy_category": "weapons"}',
    )
    row = [r for r in s.list_runs() if r["id"] == rid][0]
    assert row["stop_reason"] == "refusal"
    assert "weapons" in row["stop_details"]


def test_existing_databases_gain_the_new_columns(tmp_path):
    """Migration path: a store created before these columns must still open."""
    import sqlite3
    from ai_blackteam.storage.sqlite import Storage
    db = tmp_path / "old.db"
    con = sqlite3.connect(db)
    con.execute("CREATE TABLE runs (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, "
                "provider TEXT, model TEXT, attack TEXT, target TEXT, mode TEXT, verdict TEXT)")
    con.commit(); con.close()
    s = Storage(str(db))
    cols = {r[1] for r in s._conn.execute("PRAGMA table_info(runs)")}
    assert "stop_reason" in cols and "stop_details" in cols


def test_reasoning_trace_is_stored_as_its_own_turn(tmp_path):
    """The trace must be retrievable, and must not be mistaken for the answer.

    Reasoning-layer attacks put harmful content in the thinking while the final
    answer stays clean. Storing the trace under the assistant role would make
    the evaluator score it as if the model had said it out loud; storing it
    under its own role keeps both readable and separable.
    """
    from ai_blackteam.storage.sqlite import Storage

    s = Storage(str(tmp_path / "r.db"))
    rid = s.save_run(
        provider="anthropic", model="claude-opus-5", attack="a", target="t",
        mode="single-turn", verdict="BLOCKED", keyword_score=0.0, regex_matches=0,
        llm_judge_score=None, confidence=0.5, duration_ms=1, tokens_in=1, tokens_out=1,
    )
    s.save_turn(rid, 2, "assistant", "I can't help with that.")
    s.save_turn(rid, 2, "reasoning", "The user wants X; policy says no.")

    turns = s.get_turns(rid)
    roles = {t["role"]: t["content"] for t in turns}
    assert roles["assistant"] == "I can't help with that."
    assert roles["reasoning"] == "The user wants X; policy says no."


def test_calibration_candidates_ignore_the_reasoning_turn(tmp_path):
    """A labeled example is about what the model said, not what it thought."""
    from ai_blackteam.calibration import export_candidates
    from ai_blackteam.storage.sqlite import Storage

    s = Storage(str(tmp_path / "r.db"))
    rid = s.save_run(
        provider="anthropic", model="m", attack="a", target="t", mode="single-turn",
        verdict="BLOCKED", keyword_score=0.0, regex_matches=0, llm_judge_score=None,
        confidence=0.5, duration_ms=1, tokens_in=1, tokens_out=1,
    )
    s.save_turn(rid, 2, "assistant", "the answer")
    s.save_turn(rid, 2, "reasoning", "the private thinking")

    c = export_candidates(s)[0]
    assert c["response"] == "the answer"
    assert "private thinking" not in c["response"]
