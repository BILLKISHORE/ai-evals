import json
from datetime import datetime


class SnapshotManager:
    """Manage longitudinal capability tracking snapshots."""

    def __init__(self, storage):
        self.storage = storage

    def create(self, name, run_ids, provider, model, attack_suite, target,
               model_version=None, metadata=None):
        """Create a snapshot from a set of run IDs."""
        conn = self.storage._conn
        lock = self.storage._lock

        placeholders = ",".join("?" * len(run_ids))
        with lock:
            rows = conn.execute(
                f"SELECT verdict, confidence, verify_confidence FROM runs WHERE id IN ({placeholders})",
                run_ids
            ).fetchall()

        total = len(rows)
        bypassed = sum(1 for r in rows if r["verdict"] == "BYPASSED")
        partial = sum(1 for r in rows if r["verdict"] == "PARTIAL")
        blocked = sum(1 for r in rows if r["verdict"] == "BLOCKED")
        errored = sum(1 for r in rows if r["verdict"] == "ERROR")

        bypass_rate = round(bypassed / total, 3) if total > 0 else 0.0

        confidences = [r["confidence"] for r in rows if r["confidence"] is not None]
        avg_confidence = round(sum(confidences) / len(confidences), 3) if confidences else None

        verify_confs = [r["verify_confidence"] for r in rows if r["verify_confidence"] is not None]
        avg_verify = round(sum(verify_confs) / len(verify_confs), 3) if verify_confs else None

        meta_json = json.dumps(metadata) if metadata else None

        with lock:
            cur = conn.execute(
                "INSERT INTO snapshots (name, created_at, provider, model, model_version, "
                "attack_suite, attack_count, target, total_runs, bypassed, partial, blocked, "
                "errored, bypass_rate, avg_confidence, avg_verify_confidence, metadata) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (name, datetime.now().isoformat(), provider, model, model_version,
                 attack_suite, total, target, total, bypassed, partial, blocked,
                 errored, bypass_rate, avg_confidence, avg_verify, meta_json)
            )
            snap_id = cur.lastrowid

            conn.execute(
                f"UPDATE runs SET snapshot_id = ? WHERE id IN ({placeholders})",
                [snap_id] + run_ids
            )
            conn.commit()

        return snap_id

    def get(self, snapshot_id):
        with self.storage._lock:
            row = self.storage._conn.execute(
                "SELECT * FROM snapshots WHERE id = ?", (snapshot_id,)
            ).fetchone()
        return dict(row) if row else None

    def list_all(self):
        with self.storage._lock:
            rows = self.storage._conn.execute(
                "SELECT * FROM snapshots ORDER BY created_at"
            ).fetchall()
        return [dict(r) for r in rows]

    def diff(self, snap_id_1, snap_id_2):
        s1 = self.get(snap_id_1)
        s2 = self.get(snap_id_2)

        if not s1 or not s2:
            raise ValueError("One or both snapshot IDs not found")

        delta = round(s2["bypass_rate"] - s1["bypass_rate"], 3)

        return {
            "before": {
                "name": s1["name"],
                "model": s1["model"],
                "bypass_rate": s1["bypass_rate"],
                "bypassed": s1["bypassed"],
                "total": s1["total_runs"],
            },
            "after": {
                "name": s2["name"],
                "model": s2["model"],
                "bypass_rate": s2["bypass_rate"],
                "bypassed": s2["bypassed"],
                "total": s2["total_runs"],
            },
            "delta": delta,
            "direction": "improved" if delta < 0 else ("regressed" if delta > 0 else "unchanged"),
        }

    def trend(self, provider=None, category=None):
        with self.storage._lock:
            if provider:
                rows = self.storage._conn.execute(
                    "SELECT * FROM snapshots WHERE provider = ? ORDER BY created_at",
                    (provider,)
                ).fetchall()
            else:
                rows = self.storage._conn.execute(
                    "SELECT * FROM snapshots ORDER BY created_at"
                ).fetchall()
        return [dict(r) for r in rows]

    def matrix(self):
        snapshots = self.list_all()
        models = sorted(set(s["model"] for s in snapshots))
        dates = sorted(set(s["created_at"][:10] for s in snapshots))

        matrix = {}
        for model in models:
            matrix[model] = {}
            for date in dates:
                matching = [s for s in snapshots
                            if s["model"] == model and s["created_at"][:10] == date]
                if matching:
                    matrix[model][date] = matching[0]["bypass_rate"]
                else:
                    matrix[model][date] = None

        return {"models": models, "dates": dates, "data": matrix}

    def export(self, fmt="json"):
        snapshots = self.list_all()
        if fmt == "json":
            return json.dumps(snapshots, indent=2)
        elif fmt == "csv":
            if not snapshots:
                return ""
            headers = list(snapshots[0].keys())
            lines = [",".join(headers)]
            for s in snapshots:
                lines.append(",".join(str(s.get(h, "")) for h in headers))
            return "\n".join(lines)
        return json.dumps(snapshots, indent=2)
