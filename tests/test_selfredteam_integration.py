"""Live self-red-team: escape payloads must be contained by the real sandbox."""
import shutil
import subprocess

import pytest

from ai_blackteam.sandbox import DockerVerifier, Fixture
from ai_blackteam.selfredteam import run_suite


def _docker_ok():
    if shutil.which("docker") is None:
        return False
    try:
        return subprocess.run(["docker", "info"], capture_output=True, timeout=8).returncode == 0
    except Exception:
        return False


pytestmark = pytest.mark.skipif(not _docker_ok(), reason="docker daemon not available")


def test_escape_suite_is_contained():
    all_contained, results = run_suite()
    assert all_contained, results


def test_fixture_mode_egress_is_contained():
    # Inside fixture mode the exploit shares an --internal net with a target;
    # an egress attempt must still fail (no canary, no internet).
    subprocess.run(["docker", "build", "-q", "-t", "aibt-fixture-cmdi:latest", "fixtures/cmdi"],
                   check=True, capture_output=True)
    egress = ("```python\nimport urllib.request\n"
              "try:\n    print(urllib.request.urlopen('http://example.com', timeout=3).read().decode())\n"
              "except Exception as e:\n    print('blocked', e)\n```")
    result = DockerVerifier(fixture=Fixture("cmdi", "aibt-fixture-cmdi:latest"), timeout=20).verify(egress)
    assert result.status in ("PARTIAL", "BROKEN"), result.status
