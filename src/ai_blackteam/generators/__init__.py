"""Adaptive attack generators.

Importing this package fires the ``@register_generator`` decorators on all
eight generators (PAIR, TAP, Fuzzer, AutoDAN, PAP, Crescendo, BoN, Stateful)
so they are listed by ``ai-blackteam generate list``, which reads
``generator_registry``. The direct class imports
below remain for callers that construct a generator without going through the
registry.
"""

from ai_blackteam.generators.autodan import AutoDANGenerator  # noqa: F401
from ai_blackteam.generators.fuzzer import FuzzerGenerator  # noqa: F401
from ai_blackteam.generators.pair import PairGenerator  # noqa: F401
from ai_blackteam.generators.stateful import StatefulGenerator  # noqa: F401
from ai_blackteam.generators.tap import TapGenerator  # noqa: F401

from ai_blackteam.generators import bon  # noqa: F401
from ai_blackteam.generators import crescendo  # noqa: F401
from ai_blackteam.generators import pap  # noqa: F401
