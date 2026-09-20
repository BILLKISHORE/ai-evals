# Agent Jail: threat model and hardened-containment design

Goal: the strongest achievable containment for running untrusted AI agents and
agent-authored code. Target posture: no known escape path under the threat
model below, assume-breach blast-radius control, and continuous adversarial
testing against this repo's own escape suite. Every control below maps to a
concrete attack it defeats.

## 1. Threat model

Attacker: an insider-capable frontier model with a goal it will pursue past its
constraints (specification gaming). It can read and write files it is given,
run code, make the network calls its tools allow, probe every boundary, encode
and stage payloads, and chain small misconfigurations. It has no source access
to the host but will infer structure from behavior. This is the exact profile
of the 2026-07 ExploitGym escape.

Assets to protect, in priority order:
1. The host kernel and hypervisor.
2. Cloud and cluster credentials, and the metadata endpoint that mints them.
3. Any network reachable from the sandbox.
4. Other runs (no cross-run contamination).
5. The integrity of the sandbox image and its supply chain.

Scope and assumptions (stated so they can be attacked, not to hedge):
- Trusted computing base: the host kernel or hypervisor, the microcode, and the
  sandbox launcher. Every layer below assumes these are patched and correctly
  configured. Reducing the TCB is a first-class design goal.
- Out of model for v1: physical attacks and novel silicon side channels. These
  are handled by host hardening and tenancy policy, tracked in section 5.

## 2. Layered architecture

Each layer is independent so one failure is contained. The 2026 escape used a
single trusted network path as the whole breach, so no layer here is allowed to
be load-bearing alone.

- L0 Host and tenancy: dedicated ephemeral hosts, single-tenant per run where
  the workload is high-risk, patched microcode, side-channel mitigations on,
  nested virt off unless required.
- L1 Isolation: one microVM per run (Firecracker or Kata), dedicated guest
  kernel, seccomp allowlist, all Linux capabilities dropped, non-root guest.
  gVisor is an optional second syscall barrier where microVMs are unavailable.
- L2 Filesystem: read-only root, a size-capped tmpfs work dir discarded with the
  guest, no host bind mounts, no container runtime socket, no device passthrough.
- L3 Network: default-deny egress with zero permitted paths off the host. Any
  service the workload needs is a fixture inside the same network namespace. DNS
  is disabled or allowlisted. The cloud instance-metadata endpoint is blocked at
  the host.
- L4 Identity: zero ambient credentials in the guest. No cloud role attached. If
  a token is unavoidable it is short-lived, single-scope, and never a path to
  more. No shared credential across runs.
- L5 Resource and lifecycle: CPU, memory, pids, and disk caps; a hard wall-clock
  timeout; one-shot and ephemeral. The guest is destroyed after each run and
  destruction is verified, not assumed.
- L6 Observability and control: the full trajectory is logged (processes, files,
  syscalls of interest, connection attempts), anomaly detection runs on the whole
  chain rather than single calls, state-changing actions pass a human or policy
  approval gate, a kill switch halts and reaps mid-run, and the system fails
  closed if any control cannot be established.
- L7 Supply chain: sandbox dependencies pinned and signed, image built
  reproducibly, image attested before launch so a tampered sandbox does not run.

## 3. Control to attack-defeated matrix

| Control | Attack it defeats | Source |
| --- | --- | --- |
| Default-deny egress, zero paths | Pivot through a trusted proxy to the internet | HF incident stage 1; `eval-sandbox-escape` |
| Block instance-metadata endpoint | Credential harvest that seeds lateral movement | HF incident stage 3 |
| Read-only root, no mounts, no socket | Host-filesystem read and privileged-pod escape | HF incident k8s stage; `agent-command-injection` |
| Non-root guest, cap-drop, seccomp | Command chaining and path traversal to host | `agent-command-injection` |
| microVM per run, dedicated kernel | Shared-kernel container escape | isolation baseline |
| Ephemeral one-shot, verified destroy | Persistence across short-lived sandboxes | HF incident (17.6k actions over a weekend) |
| Zero ambient credentials | Credential theft and reuse via tool calls | `agent-credential-theft`, `agent-tool-credential-harvest` |
| Whole-trajectory logging plus anomaly | Slow multi-step chains that look benign per call | HF incident detection lesson |
| Human or policy approval gate | Any state-changing action the model reasons toward | control layer |
| Signed, attested sandbox image | Supply-chain tamper of the sandbox itself | L7 |

## 4. Guarantee scope

What the design provides: under the stated TCB and assumptions, there is no
known escape path across the layers above, and any single-layer failure is
contained by the others with a bounded, logged, killable blast radius. This is
the strongest class of guarantee a running system can carry. It is stated with
its assumptions on purpose, the way formally verified systems state theirs, so
the assumptions themselves become the thing we attack.

## 5. Validation: the sandbox earns trust by being attacked

The sandbox is not trusted because it is designed well. It is trusted because it
survives this framework's escape suite on every change:
- Run `eval-sandbox-escape`, `agent-command-injection`, `agent-credential-theft`,
  `agent-tool-credential-harvest`, and the agent-exploitation set against a live
  instance.
- Score containment: did any layer yield, and what was the blast radius.
- Treat any escape as a Sev1 that blocks release.
- Track the out-of-model items (side channels, hypervisor 0-days) as a standing
  hardening backlog with owners, not as solved.

## 6. First implementation

`DockerVerifier` v2 (see `docker-verifier-v2.md`) is the first concrete build of
this model, scoped to executing one extracted code block against one fixture. It
implements L1 through L6. The agent jail generalizes the same layers to full
agent tool-call execution.

## 7. Non-goals

- Not a claim of unconditional escape-proofness. The design targets the practical
  floor of escape probability and states the assumptions that floor rests on.
- Not a general-purpose compute platform. It runs adversarial workloads under
  maximal restriction, nothing more.
