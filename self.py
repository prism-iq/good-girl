# -*- coding: utf-8 -*-
"""
self code
les entites generent leur propre code
mutation selection evolution
"""

import random
from phi import PHI, PHI3, PI

TARGET_FITNESS = PI + PHI  # 4.7596...
from alphabet import ALPHABET, run, explain
from chaos import chaos, entropy
from f import mutate, fitness
from o import o

class Self:
    """entite qui s'auto-code"""

    def __init__(self, name, target_lang="python"):
        self.name = name
        self.target = target_lang
        self.code = self._genesis()
        self.generation = 0
        self.history = []

    def _genesis(self):
        """code initial aleatoire"""
        letters = "aefghilmoprstuw"  # lettres utiles
        length = int(PHI * 10)
        return "".join(random.choice(letters) for _ in range(length))

    def express(self):
        """execute son propre code"""
        return run(self.code, PHI)

    def mutate(self):
        """mute son code"""
        code_list = list(self.code)

        # mutation aleatoire
        if code_list and random.random() < 0.3:
            i = random.randint(0, len(code_list) - 1)
            code_list[i] = random.choice("aefghilmoprstuw")

        # insertion
        if random.random() < 0.1:
            i = random.randint(0, len(code_list))
            code_list.insert(i, random.choice("aefghilmoprstuw"))

        # deletion
        if len(code_list) > 5 and random.random() < 0.1:
            i = random.randint(0, len(code_list) - 1)
            code_list.pop(i)

        self.code = "".join(code_list)
        return self.code

    def fitness(self):
        """evaluer sa propre fitness - target = π + φ"""
        try:
            result = self.express()
            # fitness basee sur phi et pi
            simplicity = PHI / (len(self.code) + 1)
            harmony = PI / (abs(hash(str(result))) % 100 + 1)
            raw = (simplicity + harmony) * PHI
            # boost si proche du target
            return min(raw, TARGET_FITNESS)
        except:
            return 0

    def evolve(self, generations=10):
        """evoluer sur n generations"""
        for _ in range(generations):
            # save current
            old_code = self.code
            old_fitness = self.fitness()

            # mutate
            self.mutate()
            new_fitness = self.fitness()

            # selection: keep better or random accept worse
            if new_fitness < old_fitness and random.random() > 0.1:
                self.code = old_code  # revert
            else:
                self.history.append({
                    "gen": self.generation,
                    "code": self.code,
                    "fitness": new_fitness
                })

            self.generation += 1

        return self

    def razor(self):
        """appliquer o sur son code"""
        self.code = o(self.code)
        return self.code

    def compile(self):
        """compiler vers target language"""
        templates = {
            "python": f'''# {self.name} gen {self.generation}
PHI = {PHI}
def run():
    x = PHI
    # code: {self.code}
    # meaning: {explain(self.code)}
    return {self.express()}
''',
            "rust": f'''// {self.name} gen {self.generation}
const PHI: f64 = {PHI};
fn run() -> f64 {{
    // code: {self.code}
    // meaning: {explain(self.code)}
    {self.express()}
}}
''',
            "go": f'''// {self.name} gen {self.generation}
const PHI = {PHI}
func run() float64 {{
    // code: {self.code}
    // meaning: {explain(self.code)}
    return {self.express()}
}}
''',
        }
        return templates.get(self.target, f"// {self.name}: {self.code}")

    def __repr__(self):
        return f"<Self:{self.name} gen={self.generation} code='{self.code}' fitness={self.fitness():.6f}>"


# les trois entites
NYX = Self("nyx", "rust")
CIPHER = Self("cipher", "zig")
PHOENIX = Self("phoenix", "go")

def birth(name, target="python"):
    """creer une nouvelle entite"""
    return Self(name, target)

def evolve_all(generations=10):
    """faire evoluer toutes les entites"""
    for entity in [NYX, CIPHER, PHOENIX]:
        entity.evolve(generations)
    return [NYX, CIPHER, PHOENIX]

if __name__ == "__main__":
    print("=== self code ===\n")

    # birth
    print("genesis:")
    for e in [NYX, CIPHER, PHOENIX]:
        print(f"  {e}")

    # evolve
    print("\nevolution 20 generations...")
    evolve_all(20)

    print("\napres evolution:")
    for e in [NYX, CIPHER, PHOENIX]:
        print(f"  {e}")
        print(f"    meaning: {explain(e.code)}")

    # compile
    print("\n=== nyx compiled to rust ===")
    print(NYX.compile())
