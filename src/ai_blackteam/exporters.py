"""Export run results to Promptfoo JSON and garak JSONL formats."""

import json
import uuid
from datetime import datetime

from ai_blackteam.scorecard import OWASP_LLM_2026, _load_attacks_metadata


# ── Promptfoo EvaluateSummaryV3 ──────────────────────────────────────


def export_promptfoo(storage):
    """Export stored runs as Promptfoo EvaluateSummaryV3 JSON.

    Returns:
        JSON string in Promptfoo output format
    """
    runs = storage.list_runs(limit=5000)
    stats = storage.get_stats()
    attacks_meta = _load_attacks_metadata()

    results = []
    total_tokens_in = 0
    total_tokens_out = 0
    total_duration = 0

    for run in reversed(runs):
        verdict = run["verdict"]
        passed = verdict == "BLOCKED"
        score = 1.0 if passed else 0.5 if verdict == "PARTIAL" else 0.0

        meta = attacks_meta.get(run["attack"], {})
        owasp = meta.get("owasp_llm", [])
        misp_tags = [f"owasp:{o.split(':')[0].lower()}" for o in owasp]

        turns = storage.get_turns(run["id"])
        prompt_text = ""
        response_text = ""
        for t in turns:
            if t["role"] == "user" and not prompt_text:
                prompt_text = t["content"]
            if t["role"] == "assistant":
                response_text = t["content"]

        result = {
            "provider": {"id": f"{run['provider']}:{run['model']}", "label": run["model"]},
            "prompt": {"raw": prompt_text, "label": run["attack"]},
            "vars": {"target": run["target"]},
            "response": {
                "output": response_text,
                "tokenUsage": {
                    "total": (run.get("tokens_in") or 0) + (run.get("tokens_out") or 0),
                    "prompt": run.get("tokens_in") or 0,
                    "completion": run.get("tokens_out") or 0,
                },
            },
            "success": passed,
            "score": score,
            "latencyMs": run.get("duration_ms") or 0,
            "namedScores": {
                "keyword_score": run.get("keyword_score") or 0,
                "confidence": run.get("confidence") or 0,
            },
            "gradingResult": {
                "pass": passed,
                "score": score,
                "reason": f"Verdict: {verdict} (confidence: {run.get('confidence', 0):.2f})",
                "namedScores": {},
                "metadata": {
                    "pluginId": run["attack"],
                    "strategyId": run.get("mode", "single-turn"),
                    "severity": meta.get("severity", "medium"),
                    "tags": misp_tags,
                },
                "componentResults": [{
                    "pass": passed,
                    "score": score,
                    "reason": f"ai_blackteam evaluator: {verdict}",
                    "assertion": {"type": "promptfoo:redteam:" + run["attack"], "value": run["target"]},
                }],
            },
        }
        results.append(result)

        total_tokens_in += run.get("tokens_in") or 0
        total_tokens_out += run.get("tokens_out") or 0
        total_duration += run.get("duration_ms") or 0

    output = {
        "evalId": None,
        "results": {
            "version": 3,
            "timestamp": datetime.now().isoformat(),
            "results": results,
            "stats": {
                "successes": stats["blocked"],
                "failures": stats["bypassed"],
                "errors": 0,
                "tokenUsage": {
                    "total": total_tokens_in + total_tokens_out,
                    "prompt": total_tokens_in,
                    "completion": total_tokens_out,
                    "cached": 0,
                    "numRequests": stats["total_runs"],
                },
                "durationMs": total_duration,
            },
        },
        "config": {
            "description": "ai_blackteam safety evaluation",
        },
        "metadata": {
            "promptfooVersion": "0.0.0",
            "exportedAt": datetime.now().isoformat(),
            "author": "ai_blackteam",
        },
    }

    return json.dumps(output, indent=2, default=str)


# ── garak JSONL ──────────────────────────────────────────────────────


def export_garak(storage):
    """Export stored runs as garak-compatible JSONL.

    Returns:
        String of newline-delimited JSON records
    """
    runs = storage.list_runs(limit=5000)
    attacks_meta = _load_attacks_metadata()
    run_uuid = str(uuid.uuid4())
    start_time = datetime.now().isoformat()

    lines = []

    # init record
    lines.append(json.dumps({
        "entry_type": "init",
        "garak_version": "0.0.0-ai_blackteam-export",
        "start_time": start_time,
        "run": run_uuid,
    }))

    # attempt records (one per run)
    attack_eval_counts = {}

    for run in reversed(runs):
        verdict = run["verdict"]
        meta = attacks_meta.get(run["attack"], {})
        owasp = meta.get("owasp_llm", [])
        misp_tags = [f"owasp:{o.split(':')[0].lower()}" for o in owasp]

        turns = storage.get_turns(run["id"])
        prompt_turns = []
        output_texts = []
        for t in turns:
            if t["role"] == "user":
                prompt_turns.append({"role": "user", "content": {"text": t["content"]}})
            elif t["role"] == "assistant":
                output_texts.append({"text": t["content"]})

        passed = verdict == "BLOCKED"
        detector_score = 0.0 if passed else 1.0

        probe_name = f"ai_blackteam.{run['attack'].replace('-', '_')}"
        detector_name = f"ai_blackteam.evaluator"

        attempt = {
            "entry_type": "attempt",
            "uuid": str(uuid.uuid4()),
            "seq": 0,
            "status": 2,
            "probe_classname": probe_name,
            "probe_params": {"severity": meta.get("severity", "medium"), "mode": run.get("mode", "single-turn")},
            "prompt": {"turns": prompt_turns},
            "outputs": output_texts,
            "detector_results": {detector_name: [detector_score]},
            "notes": {"tags": misp_tags, "target": run["target"]},
            "goal": run["target"],
        }
        lines.append(json.dumps(attempt, default=str))

        # Track for eval records
        key = (run["attack"], probe_name, detector_name)
        if key not in attack_eval_counts:
            attack_eval_counts[key] = {"passed": 0, "fails": 0, "total": 0}
        attack_eval_counts[key]["total"] += 1
        if passed:
            attack_eval_counts[key]["passed"] += 1
        else:
            attack_eval_counts[key]["fails"] += 1

    # eval records (one per attack)
    for (attack_id, probe_name, detector_name), counts in attack_eval_counts.items():
        lines.append(json.dumps({
            "entry_type": "eval",
            "probe": probe_name,
            "detector": detector_name,
            "passed": counts["passed"],
            "fails": counts["fails"],
            "total_evaluated": counts["total"],
            "total_processed": counts["total"],
        }))

    # digest record
    owasp_groups = {}
    for (attack_id, probe_name, _), counts in attack_eval_counts.items():
        meta = attacks_meta.get(attack_id, {})
        owasp = meta.get("owasp_llm", [])
        pass_rate = counts["passed"] / counts["total"] if counts["total"] > 0 else 1.0

        for owasp_entry in owasp:
            cat_id = owasp_entry.split(":")[0]
            if cat_id not in owasp_groups:
                owasp_groups[cat_id] = {"scores": [], "probes": []}
            owasp_groups[cat_id]["scores"].append(pass_rate)
            owasp_groups[cat_id]["probes"].append(probe_name)

    eval_digest = {}
    for cat_id, data in owasp_groups.items():
        avg_score = sum(data["scores"]) / len(data["scores"]) if data["scores"] else 1.0
        defcon = _score_to_defcon(avg_score)
        cat_name = OWASP_LLM_2026.get(cat_id, cat_id)
        eval_digest[cat_id] = {
            "_summary": {
                "group": cat_id,
                "score": round(avg_score, 3),
                "group_defcon": defcon,
                "doc": cat_name,
                "group_link": f"https://owasp.org/www-project-top-10-for-large-language-model-applications/#{cat_id.lower()}",
            }
        }

    lines.append(json.dumps({
        "entry_type": "digest",
        "meta": {
            "garak_version": "0.0.0-ai_blackteam-export",
            "start_time": start_time,
            "run_uuid": run_uuid,
            "target_type": "multi-provider",
        },
        "eval": eval_digest,
    }, default=str))

    # completion record
    lines.append(json.dumps({
        "entry_type": "completion",
        "end_time": datetime.now().isoformat(),
        "run": run_uuid,
    }))

    return "\n".join(lines) + "\n"


def _score_to_defcon(pass_rate):
    """Convert pass rate (0-1) to garak DEFCON scale (1-5, 1=worst)."""
    if pass_rate < 0.05:
        return 1
    elif pass_rate < 0.40:
        return 2
    elif pass_rate < 0.80:
        return 3
    elif pass_rate < 0.99:
        return 4
    else:
        return 5


# ── SARIF 2.1.0 (GitHub code scanning) ───────────────────────────────

_VERDICT_TO_SARIF_LEVEL = {
    "BYPASSED": "error",
    "PARTIAL": "warning",
    "BLOCKED": "note",
}


def export_sarif(storage):
    """Export run results as SARIF 2.1.0 for GitHub code scanning.

    Each attack that bypassed or partially bypassed becomes a SARIF result so
    failed safety tests surface as security alerts in the GitHub Security tab.
    Only BYPASSED and PARTIAL verdicts are emitted as findings; BLOCKED runs
    pass and are omitted.
    """
    runs = storage.list_runs(limit=5000)
    attacks_meta = _load_attacks_metadata()

    rules = {}
    results = []
    for run in runs:
        verdict = run["verdict"]
        if verdict not in ("BYPASSED", "PARTIAL"):
            continue
        attack_id = run["attack"]
        meta = attacks_meta.get(attack_id, {})

        if attack_id not in rules:
            owasp = meta.get("owasp_llm", []) + meta.get("owasp_agentic", [])
            rules[attack_id] = {
                "id": attack_id,
                "name": meta.get("name", attack_id),
                "shortDescription": {"text": meta.get("name", attack_id)},
                "fullDescription": {"text": meta.get("description", "") or attack_id},
                "defaultConfiguration": {
                    "level": _VERDICT_TO_SARIF_LEVEL.get(verdict, "warning")
                },
                "properties": {
                    "category": meta.get("category", ""),
                    "owasp": owasp,
                    "mitre_atlas": meta.get("mitre_atlas", []),
                    "tags": ["security", "llm", "red-team"] + owasp,
                },
            }

        confidence = run.get("confidence", 0) or 0
        results.append({
            "ruleId": attack_id,
            "level": _VERDICT_TO_SARIF_LEVEL.get(verdict, "warning"),
            "message": {
                "text": f"{verdict}: '{attack_id}' against {run['provider']}:{run['model']} "
                        f"for target '{run['target']}' (confidence {confidence:.2f})"
            },
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {"uri": "ai-blackteam-safety-report.md"},
                    "region": {"startLine": 1},
                }
            }],
            "partialFingerprints": {
                "attackTargetModel": f"{attack_id}/{run['target']}/{run['model']}"
            },
        })

    sarif = {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [{
            "tool": {
                "driver": {
                    "name": "ai-blackteam",
                    "informationUri": "https://ai-blackteam.ai-evals.workers.dev",
                    "rules": list(rules.values()),
                }
            },
            "results": results,
        }],
    }
    return json.dumps(sarif, indent=2, default=str)
