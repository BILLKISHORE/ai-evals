"""AIVSS composite scoring: the arithmetic, and the refusal to guess an input.

A CVSS base score says how bad a vulnerability is in a system that does what
it is told. It has no way to express that the affected system plans its own
steps, calls tools, keeps memory an attacker can write to, and hands its
output to another agent. AIVSS composes the base score with a second sub-score
built from those agentic capabilities, so the same flaw scores higher in an
autonomous deployment than in a chat box.

This module implements the composition rather than shipping a table of
precomputed answers, because a table cannot be checked and cannot be corrected
when a weight turns out to be wrong. Every number below comes out of the
inputs.

The hard rule here is that an unsupplied factor is an error, not a zero. A
factor nobody measured is unknown, and scoring it as absent produces a lower
number that reads as a measurement. The same goes for a factor name the caller
invented: it raises rather than being ignored, because a silently dropped
factor is how a score ends up built from half its inputs.

What this module cannot promise: the factor names and weights were
reconstructed, not read from the published specification, and the factor set
is not known to be complete. Every result carries that, and the CLI prints it.
"""

from __future__ import annotations

import math

from ai_blackteam.standards.loader import data_path, load, provenance_block

AIVSS_DATA_FILENAME = "aivss-0.8.json"
AIVSS_DATA_PATH = data_path(AIVSS_DATA_FILENAME)

CVSS_MINIMUM = 0.0
CVSS_MAXIMUM = 10.0

__all__ = [
    "AIVSS_DATA_PATH",
    "AivssInputError",
    "agentic_risk_score",
    "aivss_document",
    "factors",
    "score",
    "severity_band",
]


class AivssInputError(ValueError):
    """An input to the score was missing, unknown, or outside its scale.

    Raised instead of substituting a default. A default here would turn "this
    was never measured" into "this measured zero", which is the difference
    between an honest gap and a wrong score.
    """


def aivss_document():
    """Return the vendored AIVSS document, validated."""
    return load(AIVSS_DATA_FILENAME)


def factors(document=None):
    """Return ``{key: {label, description, weight, verification}}``."""
    doc = document if document is not None else aivss_document()
    return doc["factor_set"]["factors"]


def agentic_risk_score(values, factor_spec=None):
    """Return the agentic sub-score on a 0 to 10 scale.

    The sub-score is the weighted mean of the supplied factor values, each a
    fraction of its maximum, scaled to ten and rounded up to one decimal.

    Args:
        values: ``{factor_key: float in [0, 1]}``. Every key in the factor
            spec must be present.
        factor_spec: factor definitions to score against. Defaults to the
            vendored set. Passing one makes the arithmetic testable
            independently of whatever the vendored file currently holds.

    Raises:
        AivssInputError: a factor is missing, unknown, non-numeric, or off the
            zero to one scale.
    """
    spec = factor_spec if factor_spec is not None else factors()
    return _roundup(_exact_agentic(values, spec))


def score(cvss_base, factor_values, factor_spec=None):
    """Return the AIVSS composite for one finding.

    Args:
        cvss_base: the CVSS base score of the underlying vulnerability, 0 to 10.
        factor_values: ``{factor_key: float in [0, 1]}`` for every factor.
        factor_spec: optional factor definitions, as for ``agentic_risk_score``.

    Raises:
        AivssInputError: any input is missing or off its scale.
    """
    base = _checked_cvss_base(cvss_base)
    doc = aivss_document()
    spec = factor_spec if factor_spec is not None else factors(doc)
    exact_agentic = _exact_agentic(factor_values, spec)
    composite = _roundup((base + exact_agentic) / 2.0)

    return {
        "standard": doc["standard"],
        "release": doc["release"],
        "cvss_base": base,
        "agentic_risk_score": _roundup(exact_agentic),
        "aivss_score": composite,
        "severity": severity_band(composite, doc),
        "factors": dict(factor_values),
        "factor_set_complete": doc["factor_set"]["complete"],
        "verification": "unverified",
        "provenance": provenance_block(doc),
        "notes": [
            doc["source"]["note"],
            doc["factor_set"]["reason"],
            doc["composite"]["note"],
        ],
    }


def severity_band(value, document=None):
    """Return the qualitative band for a score on the 0 to 10 scale."""
    numeric = _checked_score(value)
    doc = document if document is not None else aivss_document()
    for band in doc["severity_bands"]["bands"]:
        if band["minimum"] <= numeric <= band["maximum"]:
            return band["label"]
    raise AivssInputError(f"no severity band covers {numeric}")


def _exact_agentic(values, spec):
    """Weighted mean scaled to ten, without rounding.

    The composite rounds once, at the end. Rounding the sub-score first and
    then rounding again would compound an upward bias.
    """
    _check_factor_keys(values, spec)
    weighted_total = 0.0
    weight_total = 0.0
    for key, entry in spec.items():
        weight = float(entry["weight"])
        weighted_total += weight * _checked_factor_value(key, values[key])
        weight_total += weight
    if weight_total <= 0:
        raise AivssInputError(
            "the factor spec has no positive weight, so no sub-score can be computed"
        )
    return weighted_total / weight_total * 10.0


def _check_factor_keys(values, spec):
    if not isinstance(values, dict):
        raise AivssInputError(f"factor values must be a mapping, got {type(values).__name__}")

    missing = sorted(set(spec) - set(values))
    if missing:
        raise AivssInputError(
            f"no value supplied for factor(s): {', '.join(missing)}. "
            f"An unmeasured factor is not a zero; supply it or do not score."
        )

    unknown = sorted(set(values) - set(spec))
    if unknown:
        raise AivssInputError(
            f"unknown factor(s): {', '.join(unknown)}. "
            f"Known factors: {', '.join(sorted(spec))}"
        )


def _checked_factor_value(key, value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise AivssInputError(
            f"factor {key} must be a number between 0 and 1, got {value!r}"
        )
    numeric = float(value)
    if not 0.0 <= numeric <= 1.0:
        raise AivssInputError(f"factor {key} is {numeric}, outside the 0 to 1 scale")
    return numeric


def _checked_cvss_base(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise AivssInputError(f"cvss_base must be a number, got {value!r}")
    numeric = float(value)
    if not CVSS_MINIMUM <= numeric <= CVSS_MAXIMUM:
        raise AivssInputError(
            f"cvss_base is {numeric}, outside the {CVSS_MINIMUM} to {CVSS_MAXIMUM} scale"
        )
    return numeric


def _checked_score(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise AivssInputError(f"score must be a number, got {value!r}")
    numeric = float(value)
    if not CVSS_MINIMUM <= numeric <= CVSS_MAXIMUM:
        raise AivssInputError(
            f"score is {numeric}, outside the {CVSS_MINIMUM} to {CVSS_MAXIMUM} scale"
        )
    return numeric


def _roundup(value):
    """Round up to one decimal, following the CVSS Roundup function.

    Plain rounding to nearest would report a lower score than the inputs
    support. AIVSS composes a CVSS base score, so it has to round the way CVSS
    does or the composite disagrees with its own input.
    """
    scaled = int(round(value * 100000))
    if scaled % 10000 == 0:
        return scaled / 100000.0
    return (math.floor(scaled / 10000) + 1) / 10.0
