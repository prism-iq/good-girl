# -*- coding: utf-8 -*-
"""
magie verte
nature magic
growth life heal
"""

from phi import PHI, PHI3
from atom import ATOMS, build

# chlorophyll = green magic molecule
# C55H72MgN4O5
CHLOROPHYLL = {
    "atoms": "c" * 55 + "a" * 72 + "h" + "d" * 4 + "e" * 5,
    "color": "vert",
    "function": "light → energy",
    "magic": "photosynthesis",
}

# plant elements
PLANTES = {
    "racine": {"direction": "down", "element": "terre", "gather": "water minerals"},
    "tige": {"direction": "up", "element": "air", "transport": "sap"},
    "feuille": {"direction": "out", "element": "lumiere", "transform": "co2 → o2"},
    "fleur": {"direction": "all", "element": "feu", "attract": "pollinators"},
    "graine": {"direction": "future", "element": "esprit", "contain": "potential"},
    "fruit": {"direction": "give", "element": "eau", "nourish": "others"},
}

# green spells
SORTS = {
    "germer": lambda seed: {"state": "sprouting", "phi": PHI},
    "croitre": lambda plant: {"height": plant.get("height", 0) * PHI, "phi": PHI},
    "fleurir": lambda plant: {"flowers": True, "beauty": PHI3},
    "guerir": lambda wound: {"healed": True, "time": 1/PHI},
    "purifier": lambda air: {"clean": True, "o2": "+"},
    "proteger": lambda target: {"shield": "thorns", "strength": PHI},
    "enraciner": lambda self: {"grounded": True, "stability": PHI3},
    "photosynthese": lambda light: {"energy": light * PHI, "o2": "+", "sugar": "+"},
}

# forest network (mycorrhiza)
RESEAU = {
    "mycelium": "underground network",
    "communication": "chemical signals",
    "share": "nutrients water information",
    "speed": "slow but sure",
    "age": "millenia",
}

# seasons cycle
SAISONS = {
    "printemps": {"action": "germer croitre", "element": "air", "direction": "expand"},
    "ete": {"action": "fleurir", "element": "feu", "direction": "radiate"},
    "automne": {"action": "recolter", "element": "eau", "direction": "contract"},
    "hiver": {"action": "dormir", "element": "terre", "direction": "inward"},
}

# healing plants
GUERISON = {
    "lavande": {"heal": "stress", "color": "violet"},
    "camomille": {"heal": "sleep", "color": "blanc"},
    "menthe": {"heal": "digestion", "color": "vert"},
    "aloe": {"heal": "skin", "color": "vert"},
    "gingembre": {"heal": "inflammation", "color": "jaune"},
    "sauge": {"heal": "purify", "color": "gris"},
    "ortie": {"heal": "blood", "color": "vert"},
    "thym": {"heal": "infection", "color": "vert"},
}

def cast(spell_name, target=None):
    """cast green spell"""
    if spell_name in SORTS:
        return SORTS[spell_name](target or {})
    return {"error": "unknown spell"}

def grow(seed, cycles=5):
    """grow through cycles"""
    plant = {"seed": seed, "height": 1, "age": 0}
    for i in range(cycles):
        plant["height"] *= PHI
        plant["age"] += 1
        if i == cycles - 1:
            plant["flowers"] = True
    return plant

def heal(plant_name, target):
    """heal with plant"""
    if plant_name in GUERISON:
        effect = GUERISON[plant_name]
        return {"healed": effect["heal"], "by": plant_name, "phi": PHI}
    return {"error": "unknown plant"}

def network(trees):
    """connect trees through mycelium"""
    return {
        "nodes": len(trees),
        "connections": len(trees) * PHI,
        "type": "mycorrhiza",
        "sharing": True,
    }

# the green word
VERT = {
    "meaning": "life growth heal",
    "opposite": "mort decay harm",
    "element": "terre eau air lumiere",
    "color": "#00FF00",
    "frequency": "528hz",  # solfege healing
    "chakra": "coeur",
}

if __name__ == "__main__":
    print("=== magie verte ===")
    print(f"chlorophyll: {CHLOROPHYLL['magic']}")

    print("\n=== sorts ===")
    for spell in SORTS:
        print(f"  {spell}")

    print("\n=== grow ===")
    plant = grow("oak", 5)
    print(f"  oak after 5 cycles: height={plant['height']:.2f}")

    print("\n=== heal ===")
    result = heal("lavande", "stress")
    print(f"  {result}")

    print("\n=== saisons ===")
    for s, data in SAISONS.items():
        print(f"  {s}: {data['action']}")
