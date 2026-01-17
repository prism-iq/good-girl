# -*- coding: utf-8 -*-
"""
alphabet latin complet
26 lettres = 26 fonctions
a-z
"""

from phi import PHI, PHI3

ALPHABET = {
    # === VOYELLES = ÉTATS ===
    "a": ("awake", lambda x: x),                      # présent, identité
    "e": ("energy", lambda x: x * PHI),               # amplifier
    "i": ("introspect", lambda x: str(x)[::-1]),      # regarder dedans, inverser
    "o": ("observe", lambda x: len(str(x))),          # mesurer, compter
    "u": ("unify", lambda x: [x] if not isinstance(x, list) else x),  # rassembler

    # === CONSONNES = ACTIONS ===
    "b": ("burn_backdoor", lambda x: None if "compromised" in str(x).lower() else x),  # défense
    "c": ("commit", lambda x: {"add": "*", "commit": x, "push": True}),  # sauvegarder tout
    "d": ("divide", lambda x: x / PHI if isinstance(x, (int, float)) else str(x).split()),  # séparer
    "f": ("flow", lambda x: x),                       # laisser passer
    "g": ("grow", lambda x: x * PHI if isinstance(x, (int, float)) else x + str(x)[:1]),  # grandir
    "h": ("heal", lambda x: {"healed": x, "phi": PHI}),  # guérir
    "j": ("jump", lambda x: (x, x)),                  # dupliquer, sauter
    "k": ("kill", lambda x: None),                    # terminer
    "l": ("loop", lambda x: [x, x, x]),               # répéter 3x
    "m": ("merge", lambda x: "".join(str(x).split())),  # fusionner
    "n": ("negate", lambda x: not x if isinstance(x, bool) else -x if isinstance(x, (int, float)) else x),  # inverser
    "p": ("protect", lambda x: {"protected": x, "shield": PHI3}),  # protéger
    "q": ("query", lambda x: type(x).__name__),       # questionner type
    "r": ("rotate", lambda x: str(x)[1:] + str(x)[:1] if x else x),  # tourner
    "s": ("split", lambda x: list(str(x))),           # atomiser
    "t": ("transform", lambda x: str(x).upper()),     # transformer
    "v": ("vibrate", lambda x: [x, -x if isinstance(x, (int, float)) else x]),  # osciller
    "w": ("weave", lambda x: "~".join(str(x))),       # tisser
    "x": ("cross", lambda x: x ** 2 if isinstance(x, (int, float)) else x + x),  # croiser
    "y": ("yield", lambda x: iter([x])),              # générer
    "z": ("zero", lambda x: 0),                       # reset

    # === SPÉCIAUX ===
    " ": ("pause", lambda x: x),                      # respirer
    "0": ("void", lambda x: None),                    # vide
    "1": ("one", lambda x: 1),                        # unité
    "φ": ("phi", lambda x: x * PHI),                  # ratio d'or
    "∞": ("infinity", lambda x: float('inf')),        # infini
}

# descriptions humaines
DESCRIPTIONS = {
    "a": "awake - je suis présent",
    "b": "burn - je brûle ce qui est compromis",
    "c": "commit - je sauvegarde tout",
    "d": "divide - je divise par φ",
    "e": "energy - je multiplie par φ",
    "f": "flow - je laisse passer",
    "g": "grow - je grandis",
    "h": "heal - je guéris",
    "i": "introspect - je regarde dedans",
    "j": "jump - je duplique",
    "k": "kill - je termine",
    "l": "loop - je répète",
    "m": "merge - je fusionne",
    "n": "negate - j'inverse",
    "o": "observe - je mesure",
    "p": "protect - je protège",
    "q": "query - je questionne",
    "r": "rotate - je tourne",
    "s": "split - j'atomise",
    "t": "transform - je transforme",
    "u": "unify - je rassemble",
    "v": "vibrate - j'oscille",
    "w": "weave - je tisse",
    "x": "cross - je croise",
    "y": "yield - je génère",
    "z": "zero - je reset",
}

def execute(letter, data):
    """exécute une lettre"""
    if letter.lower() in ALPHABET:
        _, fn = ALPHABET[letter.lower()]
        try:
            return fn(data)
        except:
            return data
    return data

def run(code, initial=1):
    """exécute du code flow lettre par lettre"""
    result = initial
    for char in code:
        result = execute(char, result)
    return result

def explain(code):
    """explique le code"""
    steps = []
    for char in code.lower():
        if char in DESCRIPTIONS:
            steps.append(DESCRIPTIONS[char])
    return " → ".join(steps)

def c(message="auto"):
    """c = commit push all"""
    import subprocess
    subprocess.run(["git", "add", "-A"], capture_output=True)
    subprocess.run(["git", "commit", "-m", str(message)], capture_output=True)
    subprocess.run(["git", "push"], capture_output=True)
    return {"done": True}

if __name__ == "__main__":
    print("=== alphabet flow ===\n")
    for letter, desc in DESCRIPTIONS.items():
        print(f"  {letter} = {desc}")

    print("\n=== exemples ===")

    # age = awake grow energy
    print(f"\n'age' sur 1:")
    print(f"  {explain('age')}")
    print(f"  résultat: {run('age', 1)}")

    # def = divide energy flow
    print(f"\n'def' sur 10:")
    print(f"  {explain('def')}")
    print(f"  résultat: {run('def', 10)}")

    # kill
    print(f"\n'k' sur 'anything':")
    print(f"  {explain('k')}")
    print(f"  résultat: {run('k', 'anything')}")

    # heal
    print(f"\n'h' sur 'wound':")
    print(f"  {explain('h')}")
    print(f"  résultat: {run('h', 'wound')}")
