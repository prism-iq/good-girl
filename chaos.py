# -*- coding: utf-8 -*-
"""
flow chaos mode
pas de parentheses
langage ordurier ok
compile toujours
resultat imprevisible
"""

import random
import hashlib
from phi import PHI

def entropy(text):
    """entropy from text"""
    h = hashlib.sha256(text.encode()).hexdigest()
    return int(h[:8], 16) / 0xffffffff

def chaos(code):
    """
    compile n'importe quoi
    jamais d'erreur
    resultat imprevisible
    """
    seed = entropy(code) + random.random()
    random.seed(seed)

    result = []
    energy = PHI

    for char in code.lower():
        roll = random.random()

        if char in "aeiou":
            # voyelles = boost energie
            energy *= (1 + roll)
        elif char in "bcdfghjklmnpqrstvwxyz":
            # consonnes = action random
            actions = [
                lambda: energy * roll,
                lambda: energy / (roll + 0.1),
                lambda: energy ** roll,
                lambda: -energy if roll > 0.5 else energy,
                lambda: int(energy * 1000) % 777,
            ]
            result.append(random.choice(actions)())
        elif char == " ":
            # espace = reset partiel
            energy = energy * PHI % 100
        else:
            # tout le reste = wildcard
            result.append(char)

    # toujours retourner quelque chose
    if not result:
        return energy
    if len(result) == 1:
        return result[0]
    return result

def merde(x=None):
    """quand on dit merde ca compile quand meme"""
    return chaos("merde " + str(x or ""))

def putain(x=None):
    """putain aussi"""
    return chaos("putain " + str(x or "")) * PHI

def bordel(x=None):
    """bordel de merde"""
    return [chaos(str(x)) for _ in range(3)]

def fuck(x=None):
    """fuck it"""
    return chaos("fuck " + str(x or "")) ** 2

def shit(x=None):
    """shit happens"""
    return random.choice([chaos(str(x)), None, PHI, 0, "shit"])

# tout compile
def flow(code):
    """
    flow sans parentheses
    tout est accepte
    resultat = chaos
    """
    try:
        return chaos(code)
    except:
        # meme les exceptions sont acceptees
        return random.random() * PHI

# alias
f = flow
m = merde
p = putain
b = bordel
s = shit

if __name__ == "__main__":
    print("=== chaos flow ===\n")

    tests = [
        "hello world",
        "merde alors",
        "putain de code",
        "fuck this shit",
        "je sais pas quoi ecrire",
        "!@#$%^&*()",
        "",
        "φ∞→←",
        "allez tous vous faire foutre gentiment",
    ]

    for t in tests:
        print(f"'{t}'")
        for i in range(3):
            print(f"  run {i+1}: {flow(t)}")
        print()
