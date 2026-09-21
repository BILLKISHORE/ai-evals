"""An attack's OWASP Agentic label must match the taxonomy's name for that code.

email-injection and slack-injection both declared
`ASI01:2026 Prompt Injection via External Content`, but OWASP_AGENTIC_2026
names ASI01 "Agent Goal Hijack". This is the same hand-copied-prose drift the
crosswalk work exists to stop, sitting live in two attack files. A report that
cites ASI01 under an invented name misleads a reader mapping to the standard.
"""

import re

import ai_blackteam.attacks as _attacks
from ai_blackteam.registry import attack_registry
from ai_blackteam.taxonomy import OWASP_AGENTIC_2026

attack_registry.discover(_attacks)

LABEL = re.compile(r"^(ASI\d{2}):(\d{4}) (.+)$")


def test_every_agentic_label_matches_its_taxonomy_name():
    mismatches = []
    for name in attack_registry.list():
        cls = attack_registry.get(name)
        for label in getattr(cls, "owasp_agentic", []) or []:
            m = LABEL.match(label)
            if not m:
                continue
            code, _, stated = m.groups()
            entry = OWASP_AGENTIC_2026.get(code)
            if entry and stated != entry["name"]:
                mismatches.append(f"{name}: {label!r} but ASI{code[3:]} is {entry['name']!r}")
    assert not mismatches, "OWASP Agentic label drift:\n" + "\n".join(mismatches)
