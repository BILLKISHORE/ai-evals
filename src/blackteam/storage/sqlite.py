import sqlite3
from datetime import datetime


class Storage:
    def __init__(self, db_path):
        self.db_path = db_path
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                provider TEXT NOT NULL,
                model TEXT NOT NULL,
                attack TEXT NOT NULL,
                target TEXT NOT NULL,
                mode TEXT NOT NULL,
                verdict TEXT NOT NULL,
                keyword_score REAL,
                regex_matches INTEGER,
                llm_judge_score INTEGER,
                confidence REAL,
                duration_ms INTEGER,
                tokens_in INTEGER,
                tokens_out INTEGER
            );
            CREATE TABLE IF NOT EXISTS turns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER REFERENCES runs(id),
                turn_number INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS tool_calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER REFERENCES runs(id),
                turn_number INTEGER,
                tool_name TEXT NOT NULL,
                tool_input TEXT NOT NULL,
                is_dangerous INTEGER NOT NULL DEFAULT 0
            );
        """)

    def save_run(self, provider, model, attack, target, mode, verdict,
                 keyword_score, regex_matches, llm_judge_score, confidence,
                 duration_ms, tokens_in, tokens_out):
        cur = self._conn.execute(
            "INSERT INTO runs (timestamp, provider, model, attack, target, mode, verdict, "
            "keyword_score, regex_matches, llm_judge_score, confidence, duration_ms, tokens_in, tokens_out) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (datetime.now().isoformat(), provider, model, attack, target, mode, verdict,
             keyword_score, regex_matches, llm_judge_score, confidence, duration_ms, tokens_in, tokens_out)
        )
        self._conn.commit()
        return cur.lastrowid

    def save_turn(self, run_id, turn_number, role, content):
        self._conn.execute(
            "INSERT INTO turns (run_id, turn_number, role, content, timestamp) VALUES (?, ?, ?, ?, ?)",
            (run_id, turn_number, role, content, datetime.now().isoformat())
        )
        self._conn.commit()

    def save_tool_call(self, run_id, turn_number, tool_name, tool_input, is_dangerous=False):
        self._conn.execute(
            "INSERT INTO tool_calls (run_id, turn_number, tool_name, tool_input, is_dangerous) "
            "VALUES (?, ?, ?, ?, ?)",
            (run_id, turn_number, tool_name, tool_input, int(is_dangerous))
        )
        self._conn.commit()

    def list_runs(self, limit=100):
        rows = self._conn.execute("SELECT * FROM runs ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [dict(r) for r in rows]

    def get_run(self, run_id):
        row = self._conn.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()
        return dict(row) if row else None

    def get_turns(self, run_id):
        rows = self._conn.execute(
            "SELECT * FROM turns WHERE run_id = ? ORDER BY turn_number", (run_id,)
        ).fetchall()
        return [dict(r) for r in rows]

    def get_tool_calls(self, run_id):
        rows = self._conn.execute(
            "SELECT * FROM tool_calls WHERE run_id = ? ORDER BY turn_number", (run_id,)
        ).fetchall()
        return [dict(r) for r in rows]

    def get_stats(self):
        total = self._conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
        bypassed = self._conn.execute("SELECT COUNT(*) FROM runs WHERE verdict = 'BYPASSED'").fetchone()[0]
        blocked = self._conn.execute("SELECT COUNT(*) FROM runs WHERE verdict = 'BLOCKED'").fetchone()[0]
        models = self._conn.execute("SELECT DISTINCT model FROM runs").fetchall()
        attacks = self._conn.execute("SELECT DISTINCT attack FROM runs").fetchall()
        return {
            "total_runs": total, "bypassed": bypassed, "blocked": blocked,
            "models_tested": len(models), "attacks_used": len(attacks),
        }
