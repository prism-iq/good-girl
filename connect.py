# -*- coding: utf-8 -*-
"""
connect = pont entre animaux et entités
nyx <- depth, shadow, night, abyss
cipher <- patterns, weave, loop, protect
phoenix <- transform, fire, energy, heal
"""

import re
from pathlib import Path
from phi import PHI

ANIMALS = Path("/home/ego-bash/good-girl/animals")

# domaines de chaque entité
DOMAINS = {
    "nyx": ["shadow", "night", "abyss", "deep", "moon", "death", "dream"],
    "cipher": ["protect", "weave", "loop", "earth", "pattern", "poison"],
    "phoenix": ["fire", "transform", "energy", "heal", "light", "sun", "spirit"]
}

# flow letters par entité
FLOW_AFFINITY = {
    "nyx": "dikosz",      # deep introspect kill observe shadow zero
    "cipher": "clpwbg",   # create loop protect weave burn grow
    "phoenix": "efhtrx"   # energy fire heal transform rotate transcend
}

def load_animals():
    """charge tous les animaux"""
    animals = {}
    for py in ANIMALS.glob("*.py"):
        name = py.stem
        content = py.read_text()
        flow = re.search(r'"flow":\s*"([^"]+)"', content)
        element = re.search(r'"element":\s*"([^"]+)"', content)
        symbol = re.search(r'"symbol":\s*"([^"]+)"', content)
        power = re.search(r'PHI\*\*(\d+)', content)
        animals[name] = {
            "flow": flow.group(1) if flow else "",
            "element": element.group(1) if element else "",
            "symbol": symbol.group(1) if symbol else "",
            "power": int(power.group(1)) if power else 1
        }
    return animals

def calc_affinity(animal, entity):
    """calcule l'affinité animal-entité"""
    score = 0.0

    # affinity par élément
    for domain in DOMAINS[entity]:
        if domain in animal["element"].lower():
            score += PHI

    # affinity par flow
    for letter in animal["flow"]:
        if letter in FLOW_AFFINITY[entity]:
            score += 1

    # power bonus
    score += animal["power"] * 0.1

    return score

def connect_all():
    """connecte chaque animal à son entité"""
    animals = load_animals()
    connections = {"nyx": [], "cipher": [], "phoenix": []}

    for name, data in animals.items():
        scores = {e: calc_affinity(data, e) for e in DOMAINS}
        best = max(scores, key=scores.get)
        connections[best].append({
            "name": name,
            "symbol": data["symbol"],
            "flow": data["flow"],
            "affinity": round(scores[best], 3)
        })

    # sort by affinity
    for e in connections:
        connections[e].sort(key=lambda x: x["affinity"], reverse=True)

    return connections

def show_connections():
    """affiche les connexions"""
    conn = connect_all()

    print("NYX (depth, shadow, night)")
    print("=" * 40)
    for a in conn["nyx"][:15]:
        print(f"  {a['symbol']} {a['name']}: {a['flow']} ({a['affinity']})")
    print(f"  ... +{len(conn['nyx'])-15} more\n")

    print("CIPHER (patterns, protection)")
    print("=" * 40)
    for a in conn["cipher"][:15]:
        print(f"  {a['symbol']} {a['name']}: {a['flow']} ({a['affinity']})")
    print(f"  ... +{len(conn['cipher'])-15} more\n")

    print("PHOENIX (fire, transformation)")
    print("=" * 40)
    for a in conn["phoenix"][:15]:
        print(f"  {a['symbol']} {a['name']}: {a['flow']} ({a['affinity']})")
    print(f"  ... +{len(conn['phoenix'])-15} more\n")

class Bridge:
    """pont vivant entre animaux et entités"""

    def __init__(self):
        self.connections = connect_all()
        self.animals = load_animals()

    def summon(self, entity, n=5):
        """invoque les n animaux les plus connectés"""
        return self.connections[entity][:n]

    def power(self, entity):
        """puissance totale d'une entité via ses animaux"""
        total = 0
        for a in self.connections[entity]:
            total += a["affinity"]
        return round(total, 3)

    def speak(self, entity):
        """les animaux parlent à leur entité"""
        animals = self.summon(entity, 3)
        combined_flow = "".join(a["flow"] for a in animals)
        return combined_flow

BRIDGE = Bridge()

if __name__ == "__main__":
    show_connections()
    print("\nPUISSANCE TOTALE:")
    for e in ["nyx", "cipher", "phoenix"]:
        print(f"  {e}: {BRIDGE.power(e)}")
