# Host hardening runbook (L0)

L0 of the agent-jail threat model is provisioning, not code. The sandbox code
(L1 to L7 in `agent-jail-threat-model.md`) assumes the host below is hardened;
this runbook is the operator checklist that makes that assumption true. None of
it is enforced by the verifier, so it is a deploy-time gate, not a runtime one.

## Tenancy

- Run high-risk verification on dedicated hosts. Do not colocate with sensitive
  workloads or shared tenants.
- Treat the host as disposable. Reimage rather than clean up.

## Kernel and CPU

- Patched kernel and CPU microcode. Do not boot with `mitigations=off`; leave
  side-channel mitigations enabled.
- Disable nested virtualization unless a microVM runtime needs it.

## Isolation runtime

- Install gVisor (`runsc`) or Kata/Firecracker and register it with Docker.
- Verify: `docker info --format '{{.Runtimes}}'` lists `runsc`.
- Select it: `AIBT_SANDBOX_RUNTIME=gvisor`, or `DockerVerifier(runtime="gvisor")`.
- macOS Docker Desktop cannot run `runsc`; use a Linux host with KVM.

## Mandatory access control and seccomp

- AppArmor or SELinux in enforcing mode.
- Keep Docker's default seccomp, or ship an explicit allowlist and pass it as
  `seccomp_profile`.

## Network

- Host-level default-deny egress as defense in depth behind `--network none`
  and the `--internal` fixture network.
- Block the cloud instance-metadata endpoint (169.254.169.254) at the host.

## Images and supply chain

- Build fixture and base images reproducibly: pin the base by digest, pin
  package versions, build in a hermetic CI with no ambient network.
- Record image digests in a lockfile and pin them with `image_digest`.
- Sign images with cosign and pass `signature_key`; the verifier fails closed on
  a bad or missing signature when a key is set.

## Identity

- No cloud role reachable from the sandbox host that the workload could assume.
- Block IMDS at the host, not only in the container.

## Operations

- Ship the `audit` hook output to a log sink and alert on teardown survivors.
- Run the self-red-team gate (`selfredteam.run_suite`) on every deploy and treat
  any escape as a Sev1 that blocks the deploy.
