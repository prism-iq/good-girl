# -*- coding: utf-8 -*-
"""
good-girl
∞ → flow → ∞
"""

from .phi import PHI, think, hash_phi
from .o import o, score
from .f import f, loop, mutate
from .l import immortal, daemon
from .flow import WORDS, TARGETS, NATURE, AXIOM, parse, compile
from .axioms import AXIOMS, check, all_axioms
from .sources import ALL, KNOWLEDGE, DOMAINS
from .girl import GIRL, think, speak, compile, learn, evolve

__version__ = "1.0.0"
__all__ = [
    "PHI", "think", "hash_phi",
    "o", "score",
    "f", "loop", "mutate",
    "immortal", "daemon",
    "WORDS", "TARGETS", "NATURE", "AXIOM", "parse", "compile",
    "AXIOMS", "check", "all_axioms",
    "ALL", "KNOWLEDGE", "DOMAINS",
    "GIRL", "speak", "learn", "evolve",
]
