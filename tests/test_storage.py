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
