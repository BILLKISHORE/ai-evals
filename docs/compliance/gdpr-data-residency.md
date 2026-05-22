# GDPR data residency and data-subject controls

The AI-Blackteam engine processes personal data only when an operator runs adversarial traffic that itself contains personal data, or when an account holder signs in. There is no engine-side telemetry that ships data off the operator's infrastructure. Residency is therefore a deployment decision the operator owns end to end.

This document captures the operator-side controls. It is **not** a Record of Processing Activities (Art. 30 ROPA). The operator must maintain a ROPA against their own use of the engine; this document is the operator's input to that exercise.

## What personal data the engine stores

| Category | Where it lives | Source | Retention default |
|---|---|---|---|
| Account identity (email, name, hashed password / OAuth identifier) | Postgres tables `user`, `account`, `session`, `verification` (Better Auth-owned) | Sign-up form | Until user deletes account |
| Provider API keys | Postgres `target.api_key_encrypted` (AES-256-GCM with `ENCRYPTION_KEY`) | User upload via UI | Until target row deleted |
| Audit log | Postgres `audit_log` (RLS-enabled, `user_id` nullable so rows survive account deletion) | Every state-changing action | Indefinite by default; operator must set a retention job |
| Run inputs and outputs | Postgres `attack_result` and evidence ZIPs on the workers' filesystem (`REPORTS_DIR`) | The adversarial traffic the user submits. **May contain personal data if the user's prompts contain it.** | Until run row deleted; evidence ZIPs live on disk until operator prunes them |
| Reports (PDF) | Filesystem at `REPORTS_DIR`, referenced by `report.path` | Report task | Until report row deleted; PDF on disk until operator prunes |

## Region pinning: the operator's deployment recipe

The engine ships no global control plane. Every byte stays where the operator deploys it.

1. **Pick a region** (e.g. `eu-west-1` for EU residency).
2. **Postgres**: deploy a managed Postgres instance (RDS, Cloud SQL, AlloyDB, Aiven, Supabase) **with region locked**. Verify the provider does not replicate backups outside the region. For RDS, set `EnableMultiAz=true` only on multi-AZ in the same region; explicitly disable cross-region read replicas.
3. **Redis**: deploy in the same region. Redis carries Celery payloads which may include user prompts; keep it co-located.
4. **Kubernetes cluster**: deploy nodes in the same region. Set node-affinity so workers do not run in another zone group.
5. **Object storage for backups** (when § 12 of the runbook is enabled): S3 / GCS bucket in the same region, no cross-region replication, no public access, default encryption on.
6. **`DATABASE_URL`**: set to the region-pinned Postgres host. Three role-scoped DSNs apply (`engine_app`, `engine_reaper`, `engine_migration`) — all three must point at the same regional host. Helm values: `database.host`, `database.port`, `database.name`.
7. **Sentry**: if Sentry is enabled, configure it to use the EU ingest endpoint (`https://o<org>.ingest.de.sentry.io`). The default US endpoint exports error payloads (including request paths, user ids, and stack frames) to the US. CSP allowlist requires `NEXT_PUBLIC_SENTRY_HOST=https://sentry.example.com` if you self-host.
8. **Model providers**: this is the hardest control. By design the engine forwards adversarial prompts to the configured provider (Anthropic, OpenAI, Google, etc.). Where those providers process the prompt is governed by **their** terms, not the engine. If the operator must guarantee EU processing, they need to use an EU-resident endpoint (e.g. Azure OpenAI on an EU region, Anthropic on an EU-hosted Bedrock endpoint) and configure the Target's `endpoint` field accordingly.

## Region escape hatches the operator must close

| Surface | Risk | Closure |
|---|---|---|
| Default Sentry DSN | Sentry US endpoint by default | Switch DSN to EU project; verify `NEXT_PUBLIC_SENTRY_HOST` if self-hosted |
| Prometheus push | None by default; metrics are pulled in-cluster | Verify no `remote_write` to an extra-region collector |
| Model provider call | Provider may process outside region | Use region-locked endpoints; document in DPIA |
| Backups | Provider default replication | Set bucket / RDS option to single-region |
| Frontend asset CDN | Next.js may serve via CDN (Vercel, CloudFront) | Self-host or pin CDN to in-region edge |

## Data subject rights and how to fulfil them

GDPR Articles 15-22 grant data subjects the rights of access, rectification, erasure, restriction, portability, objection, and rights related to automated decision-making. The engine ships **operator-runnable scripts** that support some of these, and leaves others to the operator's UI / process.

| Right | What the engine supports | Operator must additionally |
|---|---|---|
| Art. 15 access | A user can read their own data via the UI (Targets, Runs, Reports, Snapshots, Audit). For a request from a non-account subject (a person whose data appeared in an operator's prompt), the engine has no UI; operator must build it. | Implement the subject-request intake process. |
| Art. 16 rectification | UI supports edit on Target. Audit log entries are immutable by design. | Process for rectification requests. |
| Art. 17 erasure | A user can delete a Target, Run, Report, Snapshot from the UI. Deletion cascades correctly per migration `0003_relax_fk_constraints.sql`: `report.run_id` becomes NULL, `audit_log.user_id` becomes NULL on user delete, so the audit trail survives but the actor is anonymised. | A scripted full-account-delete: see `webapp/backend/scripts/` for the validation tooling; the operator must add a `delete_user.py` script driven by their support process. Today this is done manually via SQL. |
| Art. 18 restriction | No platform support. | Manual flag in operator's CRM. |
| Art. 20 portability | Evidence ZIP export per run is the closest artifact. Operator must add a full per-user export if requested. | Per-user export script. |
| Art. 21 objection | No platform support. | Manual exclusion. |
| Art. 22 automated decision-making | The engine is a testing tool; it does not make automated decisions about subjects. n/a | n/a |

## Retention

Set retention policies operator-side. The engine has no built-in TTL on user-owned tables.

| Object | Recommended retention | How to prune |
|---|---|---|
| `audit_log` rows | 7 years for compliance evidence | Operator-built CronJob running `DELETE FROM audit_log WHERE created_at < now() - interval '7 years'`. Per Postgres role split, run this as `engine_migration` (BYPASSRLS). |
| Run outputs (`attack_result`, evidence ZIPs) | 1 year hot, then delete | Operator-built CronJob; deletes the row, then prunes the matching evidence ZIP file from `REPORTS_DIR`. |
| Backups | 30 days hot, 1 year cold (Glacier) | See RUNBOOK § 12. |
| Better Auth sessions | 30 days by default (Better Auth default) | Better Auth `expiresAt` does this automatically. |

## DPIA inputs

When the operator runs a Data Protection Impact Assessment (Art. 35), the following platform facts should be cited verbatim:

- The engine is self-hosted; no telemetry leaves the operator's network unless the operator explicitly enables Sentry.
- All user-owned tables have Postgres Row-Level Security on; cross-tenant isolation is structurally enforced (see RUNBOOK § 11).
- Provider API keys are encrypted at rest with AES-256-GCM. The encryption key is supplied by the operator and stored in the operator's secret manager.
- Audit log is append-only at the application layer (no UPDATE/DELETE paths from the API; only the migration role can prune).
- Evidence ZIPs are signed with Ed25519. Tampering is detectable. The public key ships with the ZIP.

## What this document is NOT

- Not a DPIA. It is an input to one.
- Not a Standard Contractual Clauses package; the operator handles SCCs with their model provider and any sub-processor.
- Not a privacy notice. The operator owns the privacy notice their end-users see.

## Pending work

- A `scripts/delete_user.py` that takes a user id and cascade-deletes all rows + evidence ZIPs, emitting a deletion certificate. Currently the operator does this by hand.
- A `scripts/export_user.py` for Art. 20 portability. Currently the operator builds it ad hoc.
- A retention CronJob template under `deploy/helm/templates/retention-cronjob.yaml.disabled` (analogous to the backup template in RUNBOOK § 12).
