# -*- coding: utf-8 -*-
"""
6 axioms - immutable truths
carved in stone
"""

from phi import PHI

AXIOMS = {
    1: {
        "name": "local_thinking",
        "truth": "think locally, no external API dependency",
        "impl": "phi.think() replaces all LLM calls"
    },
    2: {
        "name": "quantum_superposition",
        "truth": "multiple states until observed",
        "impl": "possibilities collapse on decision"
    },
    3: {
        "name": "numerology_as_data",
        "truth": "numbers carry meaning beyond quantity",
        "impl": "φ π e ∞ are not just numbers"
    },
    4: {
        "name": "depth_psychology",
        "truth": "Jung > Lacan > Freud",
        "impl": "archetypes > signifiers > drives"
    },
    5: {
        "name": "organ_factory",
        "truth": "build organs, not monoliths",
        "impl": "small focused modules that compose"
    },
    6: {
        "name": "confrontation",
        "truth": "truth emerges from conflict",
        "impl": "multiple perspectives converge"
    }
}

def check(axiom_id):
    """verify axiom still holds"""
    return axiom_id in AXIOMS

def all_axioms():
    """return all axioms"""
    return list(AXIOMS.values())
