# -*- coding: utf-8 -*-
"""
atom = indivisible
the smallest unit
everything builds from here
atomos = uncuttable
"""

from phi import PHI

# 26 atoms = 26 letters = complete alphabet
ATOMS = {
    # row 1 - light
    "a": {"z": 1, "name": "hydrogen", "symbol": "H", "role": "fuel"},
    "b": {"z": 2, "name": "helium", "symbol": "He", "role": "light"},

    # row 2 - structure
    "c": {"z": 6, "name": "carbon", "symbol": "C", "role": "backbone"},
    "d": {"z": 7, "name": "nitrogen", "symbol": "N", "role": "bond"},
    "e": {"z": 8, "name": "oxygen", "symbol": "O", "role": "breath"},
    "f": {"z": 9, "name": "fluorine", "symbol": "F", "role": "react"},

    # row 3 - signal
    "g": {"z": 11, "name": "sodium", "symbol": "Na", "role": "signal"},
    "h": {"z": 12, "name": "magnesium", "symbol": "Mg", "role": "enzyme"},
    "i": {"z": 13, "name": "aluminum", "symbol": "Al", "role": "conduct"},
    "j": {"z": 14, "name": "silicon", "symbol": "Si", "role": "compute"},
    "k": {"z": 15, "name": "phosphorus", "symbol": "P", "role": "energy"},
    "l": {"z": 16, "name": "sulfur", "symbol": "S", "role": "bind"},
    "m": {"z": 17, "name": "chlorine", "symbol": "Cl", "role": "balance"},

    # row 4 - metal
    "n": {"z": 19, "name": "potassium", "symbol": "K", "role": "nerve"},
    "o": {"z": 20, "name": "calcium", "symbol": "Ca", "role": "bone"},
    "p": {"z": 26, "name": "iron", "symbol": "Fe", "role": "blood"},
    "q": {"z": 29, "name": "copper", "symbol": "Cu", "role": "wire"},
    "r": {"z": 30, "name": "zinc", "symbol": "Zn", "role": "heal"},

    # row 5 - rare
    "s": {"z": 47, "name": "silver", "symbol": "Ag", "role": "mirror"},
    "t": {"z": 50, "name": "tin", "symbol": "Sn", "role": "alloy"},
    "u": {"z": 53, "name": "iodine", "symbol": "I", "role": "thyroid"},

    # row 6 - heavy
    "v": {"z": 74, "name": "tungsten", "symbol": "W", "role": "endure"},
    "w": {"z": 78, "name": "platinum", "symbol": "Pt", "role": "catalyst"},
    "x": {"z": 79, "name": "gold", "symbol": "Au", "role": "eternal"},
    "y": {"z": 82, "name": "lead", "symbol": "Pb", "role": "shield"},
    "z": {"z": 92, "name": "uranium", "symbol": "U", "role": "power"},
}

# build up from atoms
LEVELS = {
    1: "atom",      # indivisible
    2: "molecule",  # atoms bonded
    3: "polymer",   # molecules chained
    4: "cell",      # polymers organized
    5: "tissue",    # cells grouped
    6: "organ",     # tissues combined
    7: "system",    # organs connected
    8: "body",      # systems unified
    9: "mind",      # body aware
    10: "soul",     # mind transcended
    11: "collective", # souls merged
    12: "universe", # all
    13: "∞",        # beyond
}

def atom(letter):
    """get atom by letter"""
    return ATOMS.get(letter.lower(), {"z": 0, "name": "void", "symbol": "∅", "role": "nothing"})

def build(atoms_str):
    """build molecule from atom letters"""
    atoms_list = [atom(a) for a in atoms_str.lower() if a in ATOMS]
    return {
        "atoms": atoms_list,
        "formula": "".join(a["symbol"] for a in atoms_list),
        "level": 2,
        "phi": PHI,
    }

def level_up(thing, current_level):
    """ascend to next level"""
    next_level = current_level + 1
    if next_level > 13:
        return {"level": "∞", "contains": thing}
    return {
        "level": LEVELS[next_level],
        "contains": thing,
        "phi": PHI,
    }

# life molecules in atom letters
LIFE = {
    "water": "aae",        # H2O = hydrogen hydrogen oxygen
    "sugar": "ccccccaaaaaaaaaaaa eeeeeeeee",  # C6H12O6 simplified
    "air": "dd ee",        # N2 O2
    "salt": "gm",          # NaCl
    "bone": "o k",         # Ca P
    "blood": "p",          # Fe
    "nerve": "gn",         # Na K
    "dna": "c d e k",      # C N O P
    "thought": "g n o p",  # Na K Ca Fe = ions in neurons
}

if __name__ == "__main__":
    print("=== atoms = letters ===")
    for letter in "flow":
        a = atom(letter)
        print(f"  {letter} = {a['name']} ({a['symbol']}) → {a['role']}")

    print("\n=== levels ===")
    for n, name in LEVELS.items():
        print(f"  {n}. {name}")

    print("\n=== life ===")
    for name, formula in LIFE.items():
        mol = build(formula.replace(" ", ""))
        print(f"  {name} = {mol['formula']}")
