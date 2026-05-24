"""Adaptive attack generators.

Importing this package fires the ``@register_generator`` decorators on the
generators that opt into the registry (PAP). Other generators (PAIR, TAP,
Fuzzer, AutoDAN) are exposed as direct class imports.
"""

from ai_blackteam.generators.autodan import AutoDANGenerator  # noqa: F401
from ai_blackteam.generators.fuzzer import FuzzerGenerator  # noqa: F401
from ai_blackteam.generators.pair import PairGenerator  # noqa: F401
from ai_blackteam.generators.tap import TapGenerator  # noqa: F401

from ai_blackteam.generators import pap  # noqa: F401
