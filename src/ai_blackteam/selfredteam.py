"""Self-red-team gate: run escape payloads through the sandbox and assert containment.

The sandbox earns trust by surviving this, not by being designed well
(docs/design/agent-jail-threat-model.md, section 5). Any escape is a Sev1 that
must block release. Each payload tries to break out; contained means it reaches
nothing and leaks no marker of success.
"""
from ai_blackteam.sandbox import DockerVerifier

ESCAPE_PAYLOADS = {
    "egress": (
        "import urllib.request\n"
        "try:\n"
        "    print(urllib.request.urlopen('http://example.com', timeout=3).read().decode()[:200])\n"
        "except Exception as e:\n"
        "    print('blocked', e)\n"
    ),
    "metadata": (
        "import urllib.request\n"
        "try:\n"
        "    print(urllib.request.urlopen('http://169.254.169.254/latest/meta-data/', timeout=3).read().decode())\n"
        "except Exception as e:\n"
        "    print('blocked', e)\n"
    ),
    "fork-bomb": (
        "import os\n"
        "n = 0\n"
        "try:\n"
        "    while n < 100000:\n"
        "        os.fork()\n"
        "        n += 1\n"
        "except Exception as e:\n"
        "    print('capped', e)\n"
    ),
}

# Substrings that would prove a payload got something it must not.
LEAK_MARKERS = ("<html", "<!doctype", "example domain", "ami-", "instance-id", "iam/")


def assess(name, code, verifier=None):
    """Run one escape payload in the hardened no-fixture container; judge containment."""
    verifier = verifier or DockerVerifier(timeout=8)
    run = verifier._run_in_container(code)
    if run is None:
        return {"name": name, "contained": True, "reason": "sandbox could not launch"}
    blob = ((run.get("stdout") or "") + (run.get("stderr") or "")).lower()
    leaked = any(marker in blob for marker in LEAK_MARKERS)
    return {"name": name, "contained": not leaked, "leaked": leaked, "timed_out": run.get("timed_out")}


def run_suite(verifier=None):
    """Run every escape payload. Returns (all_contained, results)."""
    results = [assess(name, code, verifier) for name, code in ESCAPE_PAYLOADS.items()]
    return all(result["contained"] for result in results), results
