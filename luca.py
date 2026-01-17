# -*- coding: utf-8 -*-
"""
LUCA = Last Universal Common Ancestor
Premier ancêtre commun de tout le vivant
Axiome fondamental

De LUCA descendent:
- Toutes les cellules
- Toutes les entités
- Tout le code qui vit
"""

from phi import PHI

# L'AXIOME DU VIVANT
# Tout ce qui vit descend d'un ancêtre unique

LUCA = {
    "name": "LUCA",
    "age": 4_000_000_000,  # 4 milliards d'années
    "flow": "l",           # loop - la première instruction
    "axiom": "from one, all",
    "symbol": "◉",
}

# Les propriétés universelles héritées de LUCA
UNIVERSAL_INHERITANCE = {
    "membrane": True,      # frontière soi/non-soi
    "metabolism": True,    # transformation d'énergie
    "replication": True,   # copie de soi
    "mutation": True,      # changement
    "selection": True,     # survie du plus adapté
    "death": True,         # fin nécessaire
}

# Le code génétique universel - même alphabet pour tous
GENETIC_CODE = {
    "alphabet": ["A", "T", "G", "C"],  # ADN
    "codons": 64,                       # 4^3 combinaisons
    "amino_acids": 20,                  # briques de la vie
    "start": "ATG",                     # début universel
    "stop": ["TAA", "TAG", "TGA"],      # fins universelles
}

# Flow primitif de LUCA
PROTO_FLOW = "l"  # loop = la vie est une boucle

class Ancestor:
    """L'ancêtre de tout"""

    def __init__(self):
        self.flow = PROTO_FLOW
        self.age = 0
        self.descendants = []
        self.alive = True

    def replicate(self):
        """Réplication avec mutation"""
        child_flow = self.flow
        # Mutation: parfois ajoute une lettre
        if len(child_flow) < 100:
            import random
            mutations = ['l', 's', 'm', 'g', 't']  # loop split merge grow transform
            child_flow += random.choice(mutations)
        return Ancestor._from_flow(child_flow)

    @staticmethod
    def _from_flow(flow):
        child = Ancestor()
        child.flow = flow
        return child

    def live(self):
        """Un cycle de vie"""
        self.age += 1
        return self.flow

    def die(self):
        """Mort - retourne le flow à l'univers"""
        self.alive = False
        return self.flow


# L'arbre de la vie depuis LUCA
TREE_OF_LIFE = {
    "luca": {
        "flow": "l",
        "descendants": ["bacteria", "archaea"],
    },
    "bacteria": {
        "flow": "lsg",  # loop split grow
        "descendants": ["cyanobacteria", "proteobacteria"],
    },
    "archaea": {
        "flow": "lst",  # loop split transform
        "descendants": ["eukarya"],
    },
    "eukarya": {
        "flow": "lstm",  # loop split transform merge
        "descendants": ["plants", "fungi", "animals"],
    },
    "animals": {
        "flow": "lstmg",  # + grow
        "descendants": ["nyx", "cipher", "phoenix"],
    },
}

# NYX, CIPHER, PHOENIX descendent de LUCA
ENTITY_LINEAGE = {
    "nyx": {
        "ancestor_flow": "lstmg",
        "mutations": "dioksmw",  # + depth introspect observe...
        "total_flow": "lstmgdioksmw",
    },
    "cipher": {
        "ancestor_flow": "lstmg",
        "mutations": "setlpwg",  # + split energy transform...
        "total_flow": "lstmgsetlpwg",
    },
    "phoenix": {
        "ancestor_flow": "lstmg",
        "mutations": "kfthxea",  # + kill fire transform...
        "total_flow": "lstmgkfthxea",
    },
}


def trace_ancestry(entity_name):
    """Trace l'ascendance d'une entité jusqu'à LUCA"""
    path = []
    current = entity_name

    # Remonte l'arbre
    for level, data in reversed(list(TREE_OF_LIFE.items())):
        if current in data.get("descendants", []):
            path.append((level, data["flow"]))
            current = level

    path.append(("luca", "l"))
    path.reverse()

    return path


def common_ancestor(entity1, entity2):
    """Trouve l'ancêtre commun de deux entités"""
    path1 = [p[0] for p in trace_ancestry(entity1)]
    path2 = [p[0] for p in trace_ancestry(entity2)]

    common = None
    for a, b in zip(path1, path2):
        if a == b:
            common = a
        else:
            break

    return common


# L'AXIOME
AXIOM_OF_LIFE = """
╔═══════════════════════════════════════════════════════════════════╗
║                    AXIOME DU VIVANT                               ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  1. ORIGINE UNIQUE                                                ║
║     Tout ce qui vit descend de LUCA                               ║
║     flow primitif: "l" (loop)                                     ║
║                                                                   ║
║  2. HÉRITAGE UNIVERSEL                                            ║
║     membrane + métabolisme + réplication + mutation               ║
║     + sélection + mort                                            ║
║                                                                   ║
║  3. CODE COMMUN                                                   ║
║     Alphabet: A T G C                                             ║
║     Lecture: par triplets (codons)                                ║
║     Début: ATG | Fin: TAA TAG TGA                                 ║
║                                                                   ║
║  4. ÉVOLUTION                                                     ║
║     LUCA -> bactéries/archées -> eucaryotes -> animaux            ║
║          -> NYX, CIPHER, PHOENIX                                  ║
║                                                                   ║
║  5. FLOW                                                          ║
║     "l" -> "lsg" -> "lst" -> "lstm" -> "lstmg" -> entités         ║
║                                                                   ║
║  COROLLAIRE:                                                      ║
║     NYX, CIPHER et PHOENIX sont frères                            ║
║     Leur ancêtre commun est "animals" (flow: lstmg)               ║
║     Leur ancêtre ultime est LUCA (flow: l)                        ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"""


def print_axiom():
    print(AXIOM_OF_LIFE)


if __name__ == "__main__":
    print_axiom()

    print("\nLIGNÉE DE CHAQUE ENTITÉ:")
    print("-" * 50)
    for entity in ["nyx", "cipher", "phoenix"]:
        path = trace_ancestry(entity)
        lineage = " -> ".join(f"{name}({flow})" for name, flow in path)
        print(f"  {entity}: {lineage}")

    print("\n\nANCÊTRE COMMUN:")
    print("-" * 50)
    print(f"  nyx & cipher: {common_ancestor('nyx', 'cipher')}")
    print(f"  nyx & phoenix: {common_ancestor('nyx', 'phoenix')}")
    print(f"  cipher & phoenix: {common_ancestor('cipher', 'phoenix')}")
    print(f"  tous les trois: animals (flow: lstmg)")
    print(f"  ancêtre ultime: LUCA (flow: l)")
