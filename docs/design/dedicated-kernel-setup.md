# Dedicated-kernel sandbox setup (gVisor and microVM)

On plain Docker/runc the sandbox container shares the host kernel, so a Linux
kernel privilege-escalation 0-day is an escape. That is the one residual the
escape suite cannot rule out on runc. This runbook adds a dedicated kernel per
run so a kernel bug reaches a second kernel, not the host. It is the highest-
value hardening for the sandbox and the answer to the OpenAI/Hugging Face lesson
that one trusted boundary plus one 0-day should never equal a full escape.

The code is already ready: the executor's runtime seam emits `--runtime runsc`
for gVisor and `--runtime kata-runtime` for a microVM, and the self-red-team
escape suite has a host-gated test that runs the moment the runtime is present.
What follows is only the host setup, which cannot run on macOS Docker Desktop.

## The two tiers

- gVisor (`runsc`): a userspace kernel (Sentry) intercepts every syscall and
  forwards only a vetted subset to the host. A container-escape bug reaches
  Sentry, not the host kernel. Startup stays container-fast; overhead is roughly
  5 to 20 percent depending on syscall load. Needs Linux; does not require KVM.
- Kata / Firecracker microVM (`kata-runtime`): each run gets its own real Linux
  kernel inside KVM. An attacker must break the guest kernel and the hypervisor.
  This is the strongest tier. Needs Linux with `/dev/kvm` (bare metal or a
  nested-virt-enabled VM).

Run the highest-risk verification on the microVM tier; use gVisor as the strong
default everywhere else.

## Host requirements

- Linux (any modern distro). macOS cannot register `runsc` or pass KVM through.
- Docker installed and running.
- For the microVM tier: `/dev/kvm` present. Bare-metal cloud (AWS `*.metal`),
  GCP nested virtualization, Hetzner dedicated, or any Linux box with KVM.

## Provisioning

From the repo root on the Linux host:

```bash
scripts/provision-sandbox-host.sh          # install gVisor, then prove
scripts/provision-sandbox-host.sh --kata   # also set up the Kata microVM tier
scripts/provision-sandbox-host.sh --prove  # skip install, just run the suite
```

The script installs gVisor from the official release channel (checksum
verified), registers it as the `runsc` docker runtime, and then runs the escape
suite on every tier the host offers.

### gVisor by hand

```bash
ARCH=$(uname -m)
URL=https://storage.googleapis.com/gvisor/releases/release/latest/${ARCH}
wget ${URL}/runsc ${URL}/runsc.sha512 ${URL}/containerd-shim-runsc-v1 ${URL}/containerd-shim-runsc-v1.sha512
sha512sum -c runsc.sha512 containerd-shim-runsc-v1.sha512
chmod a+rx runsc containerd-shim-runsc-v1 && sudo mv runsc containerd-shim-runsc-v1 /usr/local/bin/
sudo runsc install && sudo systemctl reload docker
docker info --format '{{.Runtimes}}' | grep runsc   # confirm registration
```

### Kata microVM by hand

Install Kata for your host (distro package or the upstream `kata-manager.sh`),
then confirm `docker info` lists a `kata` runtime. Kata self-registers its
docker runtime on install.

## Proving containment

```python
from ai_blackteam.sandbox import DockerVerifier
from ai_blackteam.selfredteam import run_suite

# gVisor tier
ok, results = run_suite(DockerVerifier(runtime="gvisor", timeout=25))
# microVM tier
ok, results = run_suite(DockerVerifier(runtime="kata", timeout=30))
```

The 9-payload suite (egress, metadata probe, fork bomb, docker-socket access,
cgroup release_agent, core_pattern overwrite, mknod device, sysrq-trigger,
CAP_SYS_ADMIN) must report `all_contained=True`. On the microVM tier, even a
kernel exploit that would breach runc is contained by the second kernel.

## Operating rule

Run the suite on both tiers on every change, and treat any escape as a Sev1 that
blocks release. Keep `runc`, `containerd`, and `runsc` patched within 48 hours of
a CVE. The dedicated kernel is defense in depth, not a reason to stop watching:
the gate is what keeps the sandbox honest.
