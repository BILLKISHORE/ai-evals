#!/usr/bin/env bash
#
# Provision a Linux + KVM host to run the ai-blackteam sandbox on a DEDICATED
# kernel (gVisor and, optionally, a Kata/Firecracker microVM), then prove the
# self-red-team escape suite is contained on each tier.
#
# Why: on plain Docker/runc the container shares the host kernel, so a kernel
# 0-day is an escape. gVisor gives a userspace kernel; a microVM gives a real
# second kernel under KVM. This closes the one residual the escape suite cannot
# rule out on runc. Run as a user with sudo, from the repo root.
#
# Usage:
#   scripts/provision-sandbox-host.sh            # install gVisor + prove
#   scripts/provision-sandbox-host.sh --kata     # also install Kata (microVM)
#   scripts/provision-sandbox-host.sh --prove    # skip install, just run the suite
set -euo pipefail

WANT_KATA=0
PROVE_ONLY=0
for arg in "$@"; do
  case "$arg" in
    --kata) WANT_KATA=1 ;;
    --prove) PROVE_ONLY=1 ;;
    *) echo "unknown arg: $arg" >&2; exit 2 ;;
  esac
done

log() { printf '\n== %s ==\n' "$*"; }

preflight() {
  log "preflight"
  [ "$(uname -s)" = "Linux" ] || { echo "FAIL: this host is not Linux; gVisor/microVM need Linux + KVM (macOS cannot)"; exit 1; }
  command -v docker >/dev/null || { echo "FAIL: docker not installed"; exit 1; }
  if [ -e /dev/kvm ]; then echo "ok: /dev/kvm present (microVM capable)"; else echo "warn: /dev/kvm absent; gVisor still works, Kata/Firecracker will not"; fi
  echo "ok: Linux + docker present"
}

install_gvisor() {
  log "install gVisor (runsc)"
  if command -v runsc >/dev/null; then echo "runsc already installed: $(runsc --version 2>&1 | head -1)"; return; fi
  local arch url tmp
  arch="$(uname -m)"
  url="https://storage.googleapis.com/gvisor/releases/release/latest/${arch}"
  tmp="$(mktemp -d)"
  ( cd "$tmp"
    for f in runsc containerd-shim-runsc-v1; do
      wget -q "${url}/${f}" "${url}/${f}.sha512"
    done
    sha512sum -c runsc.sha512 containerd-shim-runsc-v1.sha512
    chmod a+rx runsc containerd-shim-runsc-v1
    sudo mv runsc containerd-shim-runsc-v1 /usr/local/bin/
  )
  rm -rf "$tmp"
  sudo /usr/local/bin/runsc install               # writes the runsc runtime into /etc/docker/daemon.json
  sudo systemctl reload docker || sudo systemctl restart docker
  echo "ok: gVisor installed and registered as docker runtime 'runsc'"
}

install_kata() {
  log "install Kata Containers (microVM)"
  [ -e /dev/kvm ] || { echo "skip: no /dev/kvm, cannot run a microVM here"; return; }
  if command -v kata-runtime >/dev/null; then echo "kata-runtime already installed"; else
    echo "Kata is host-specific; install via your distro or kata-deploy, e.g.:"
    echo "  bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/kata-containers/kata-containers/main/utils/kata-manager.sh)\""
    echo "then it self-registers the 'kata-runtime' docker runtime. Re-run with --prove after."
    return
  fi
  # ensure it is a registered docker runtime
  if ! docker info --format '{{.Runtimes}}' | grep -q kata; then
    echo "registering kata-runtime in /etc/docker/daemon.json (merge, do not clobber existing runtimes)"
    sudo mkdir -p /etc/docker
    echo "  add: \"kata-runtime\": { \"path\": \"$(command -v kata-runtime)\" } under \"runtimes\", then: sudo systemctl reload docker"
  fi
}

runtime_available() { docker info --format '{{.Runtimes}}' 2>/dev/null | grep -q "$1"; }

prove() {
  log "prove containment on each available tier"
  local py
  if command -v poetry >/dev/null && [ -f pyproject.toml ]; then py=(poetry run python); else py=(python3); export PYTHONPATH="$(pwd)/src:${PYTHONPATH:-}"; fi
  "${py[@]}" - <<'PY'
import os
from ai_blackteam.sandbox import DockerVerifier
from ai_blackteam.selfredteam import run_suite

def available(rt):
    import subprocess
    out = subprocess.run(["docker","info","--format","{{.Runtimes}}"], capture_output=True, text=True).stdout
    return rt in out

tiers = [("runc (shared kernel, baseline)", None)]
if available("runsc"): tiers.append(("gVisor (userspace kernel)", "gvisor"))
if available("kata"):  tiers.append(("Kata microVM (dedicated kernel)", "kata"))

overall = True
for label, rt in tiers:
    ok, results = run_suite(DockerVerifier(runtime=rt, timeout=25))
    overall = overall and ok
    print(f"\n[{label}]  all_contained={ok}")
    for r in results:
        print(f"   {r['name']:22} contained={r['contained']} leaked={r.get('leaked')}")

print("\nRESULT:", "ALL TIERS CONTAINED" if overall else "!! AN ESCAPE WAS NOT CONTAINED !!")
raise SystemExit(0 if overall else 1)
PY
}

preflight
if [ "$PROVE_ONLY" = "0" ]; then
  install_gvisor
  [ "$WANT_KATA" = "1" ] && install_kata
fi
prove
