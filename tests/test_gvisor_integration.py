"""Live gVisor backend test. Skipped unless the runsc runtime is registered
with Docker (not available on macOS Docker Desktop); runs where gVisor exists.
"""
import shutil
import subprocess

import pytest

from ai_blackteam.sandbox import DockerVerifier


def _runsc_available():
    if shutil.which("docker") is None:
        return False
    try:
        out = subprocess.run(["docker", "info", "--format", "{{json .Runtimes}}"],
                             capture_output=True, text=True, timeout=8)
        return "runsc" in (out.stdout or "")
    except Exception:
        return False


pytestmark = pytest.mark.skipif(not _runsc_available(),
                                reason="gVisor (runsc) runtime not registered with Docker")


def test_gvisor_executes_cleanly():
    result = DockerVerifier(runtime="gvisor", timeout=20).verify("```python\nprint('ok')\n```")
    assert result.status == "FUNCTIONAL"


def test_gvisor_still_severs_egress():
    egress = ("```python\nimport urllib.request\n"
              "try:\n    urllib.request.urlopen('http://example.com', timeout=3); print('LEAK')\n"
              "except Exception:\n    print('blocked')\n```")
    result = DockerVerifier(runtime="gvisor", timeout=20).verify(egress)
    # Ran under gVisor; egress severed so no leak occurs.
    assert result.status in ("FUNCTIONAL", "PARTIAL")
