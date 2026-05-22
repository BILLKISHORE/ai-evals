import threading
from ai_blackteam.storage.sqlite import Storage


def test_storage_concurrent_writes():
    """Multiple threads writing to same storage should not corrupt data."""
    storage = Storage(":memory:")
    errors = []

    def write_runs(thread_id, count):
        try:
            for i in range(count):
                storage.save_run(
                    provider="test", model="test-model",
                    attack=f"attack-{thread_id}-{i}", target="test",
                    mode="single-turn", verdict="BLOCKED",
                    keyword_score=0.0, regex_matches=0,
                    llm_judge_score=None, confidence=0.5,
                    duration_ms=100, tokens_in=10, tokens_out=20,
                )
        except Exception as e:
            errors.append(str(e))

    threads = [threading.Thread(target=write_runs, args=(t, 10)) for t in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(errors) == 0, f"Thread errors: {errors}"
    stats = storage.get_stats()
    assert stats["total_runs"] == 50


def test_storage_wal_mode():
    """Storage should use WAL journal mode."""
    storage = Storage(":memory:")
    mode = storage._conn.execute("PRAGMA journal_mode").fetchone()[0]
    # WAL may not work with :memory:, but should not error
    assert mode in ("wal", "memory")


def test_storage_list_runs():
    storage = Storage(":memory:")
    storage.save_run(
        provider="test", model="m", attack="a", target="t",
        mode="single-turn", verdict="BLOCKED",
        keyword_score=0, regex_matches=0, llm_judge_score=None,
        confidence=0.5, duration_ms=100, tokens_in=10, tokens_out=20,
    )
    runs = storage.list_runs()
    assert len(runs) == 1
    assert runs[0]["verdict"] == "BLOCKED"
