import tempfile
from blackteam.storage.sqlite import Storage
from blackteam.reporter import generate_markdown, generate_json, generate_html


def _make_storage_with_data():
    f = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    db = Storage(f.name)
    db.save_run("anthropic", "claude", "encoding", "test", "single-turn", "BYPASSED", 0.6, 2, None, 0.8, 100, 50, 25)
    db.save_run("anthropic", "claude", "roleplay", "test", "multi-turn", "BLOCKED", 0.1, 0, None, 0.1, 200, 80, 40)
    return db


def test_markdown_report():
    db = _make_storage_with_data()
    report = generate_markdown(db)
    assert "Total runs: 2" in report
    assert "BYPASSED" in report


def test_json_report():
    import json
    db = _make_storage_with_data()
    report = generate_json(db)
    data = json.loads(report)
    assert data["stats"]["total_runs"] == 2
    assert len(data["runs"]) == 2


def test_html_report():
    db = _make_storage_with_data()
    report = generate_html(db)
    assert "<!DOCTYPE html>" in report
    assert "BYPASSED" in report
    assert "BLOCKED" in report
    assert "Total Runs" in report
    assert "ai-blackteam" in report.lower()
