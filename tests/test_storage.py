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
