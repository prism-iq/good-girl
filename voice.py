# -*- coding: utf-8 -*-
"""
voice = voix des animaux
chaque animal parle sa sagesse
"""

import importlib
from pathlib import Path
from phi import PHI

BASE = Path("/home/ego-bash/good-girl")
ANIMALS = BASE / "animals"

def load_animal(name):
    """charge un animal"""
    spec = importlib.util.spec_from_file_location(name, ANIMALS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, name.upper(), None)

def speak(animal_data, name):
    """animal parle sa nature"""
    if not animal_data:
        return None
    return {
        "name": name,
        "says": interpret_flow(animal_data.get("flow", "")),
        "element": animal_data.get("element", ""),
        "power": animal_data.get("power", 1),
        "symbol": animal_data.get("symbol", "")
    }

def interpret_flow(flow):
    """interprète le flow en paroles"""
    meanings = {
        "a": "awake", "b": "burn", "c": "create", "d": "deep",
        "e": "energy", "f": "fire", "g": "grow", "h": "heal",
        "i": "introspect", "j": "jump", "k": "kill", "l": "loop",
        "m": "merge", "n": "nurture", "o": "observe", "p": "protect",
        "q": "quest", "r": "rotate", "s": "split", "t": "transform",
        "u": "unite", "v": "vibrate", "w": "weave", "x": "transcend",
        "y": "yield", "z": "zero"
    }
    return " ".join(meanings.get(c, c) for c in flow.lower())

def all_voices():
    """toutes les voix"""
    voices = []
    for py in ANIMALS.glob("*.py"):
        name = py.stem
        try:
            data = load_animal(name)
            voice = speak(data, name)
            if voice:
                voices.append(voice)
        except:
            pass
    return voices

def chorus():
    """choeur de tous les animaux"""
    voices = all_voices()
    for v in sorted(voices, key=lambda x: x.get("power", 0), reverse=True):
        print(f"{v['symbol']} {v['name']}: {v['says']}")

if __name__ == "__main__":
    chorus()
