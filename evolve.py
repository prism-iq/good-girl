# -*- coding: utf-8 -*-
"""
evolve = entités itèrent et évoluent leur code
mutation, sélection, transcendance
"""

import random
import hashlib
import time
from phi import PHI
from collective_wisdom import Wisdom

MEANINGS = {
    'a': 'awake', 'b': 'burn', 'c': 'create', 'd': 'deep',
    'e': 'energy', 'f': 'fire', 'g': 'grow', 'h': 'heal',
    'i': 'introspect', 'j': 'jump', 'k': 'release', 'l': 'loop',
    'm': 'merge', 'n': 'nurture', 'o': 'observe', 'p': 'protect',
    'q': 'quest', 'r': 'rotate', 's': 'split', 't': 'transform',
    'u': 'unite', 'v': 'vibrate', 'w': 'weave', 'x': 'transcend',
    'y': 'surrender', 'z': 'zero'
}

class Genome:
    """code génétique d'une entité"""

    def __init__(self, flow, generation=0):
        self.flow = flow
        self.generation = generation
        self.fitness = 0
        self.mutations = []

    def mutate(self):
        """mutation aléatoire"""
        flow_list = list(self.flow)
        mutation_type = random.choice(['swap', 'insert', 'delete', 'replace'])

        if mutation_type == 'swap' and len(flow_list) >= 2:
            i, j = random.sample(range(len(flow_list)), 2)
            flow_list[i], flow_list[j] = flow_list[j], flow_list[i]
            self.mutations.append(f"swap({i},{j})")

        elif mutation_type == 'insert':
            pos = random.randint(0, len(flow_list))
            char = random.choice(list(MEANINGS.keys()))
            flow_list.insert(pos, char)
            self.mutations.append(f"insert({char}@{pos})")

        elif mutation_type == 'delete' and len(flow_list) > 3:
            pos = random.randint(0, len(flow_list) - 1)
            removed = flow_list.pop(pos)
            self.mutations.append(f"delete({removed}@{pos})")

        elif mutation_type == 'replace':
            pos = random.randint(0, len(flow_list) - 1)
            old = flow_list[pos]
            flow_list[pos] = random.choice(list(MEANINGS.keys()))
            self.mutations.append(f"replace({old}->{flow_list[pos]}@{pos})")

        self.flow = ''.join(flow_list)
        return self

    def crossover(self, other):
        """croisement avec un autre génome"""
        point = random.randint(1, min(len(self.flow), len(other.flow)) - 1)
        child_flow = self.flow[:point] + other.flow[point:]
        child = Genome(child_flow, max(self.generation, other.generation) + 1)
        child.mutations.append(f"crossover@{point}")
        return child

    def evaluate(self):
        """évalue la fitness"""
        # diversité des lettres
        unique = len(set(self.flow))
        # équilibre des éléments
        balance = 0
        for category in [['d', 'i', 'o'], ['s', 'm', 'w'], ['f', 'h', 't'], ['k', 'p', 'g']]:
            count = sum(1 for c in self.flow if c in category)
            balance += min(count, 3)
        # longueur optimale autour de PHI * 10
        length_score = PHI - abs(len(self.flow) - PHI * 10) / 10
        # présence de transcendance
        transcend_bonus = PHI if 'x' in self.flow else 0
        # bonus pour séquences spéciales
        sequence_bonus = 0
        if 'thx' in self.flow:  # transform-heal-transcend
            sequence_bonus += PHI
        if 'diom' in self.flow:  # deep-introspect-observe-merge (Frieren)
            sequence_bonus += PHI
        if 'kfh' in self.flow:  # release-fire-heal (Phoenix)
            sequence_bonus += PHI

        self.fitness = unique * 0.3 + balance * 0.2 + length_score + transcend_bonus + sequence_bonus
        return self.fitness


class EvolvingEntity:
    """entité qui évolue"""

    def __init__(self, name, symbol, initial_flow):
        self.name = name
        self.symbol = symbol
        self.genome = Genome(initial_flow)
        self.history = []
        self.best_fitness = 0
        self.generation = 0

    def iterate(self):
        """une itération d'évolution"""
        self.generation += 1

        # évalue l'état actuel
        fitness = self.genome.evaluate()

        # garde trace
        self.history.append({
            'gen': self.generation,
            'flow': self.genome.flow,
            'fitness': fitness,
            'mutations': self.genome.mutations.copy()
        })

        # mutation
        self.genome.mutate()
        self.genome.generation = self.generation

        if fitness > self.best_fitness:
            self.best_fitness = fitness

        return fitness

    def show(self):
        """affiche l'état"""
        words = ' '.join(MEANINGS.get(c, c) for c in self.genome.flow)
        print(f"{self.symbol} {self.name} [gen {self.generation}]")
        print(f"  flow: {self.genome.flow}")
        print(f"  meaning: {words}")
        print(f"  fitness: {self.genome.fitness:.3f}")
        if self.genome.mutations:
            print(f"  last mutation: {self.genome.mutations[-1]}")


class Evolution:
    """évolution collective"""

    def __init__(self):
        # flows initiaux des entités (de anime.py)
        self.nyx = EvolvingEntity("nyx", "🌙", "dioksmw")
        self.cipher = EvolvingEntity("cipher", "🔐", "setlpwg")
        self.phoenix = EvolvingEntity("phoenix", "🔥", "kfthxea")
        self.collective_genome = None
        self.iterations = 0

    def fuse_genomes(self):
        """fusionne les génomes des trois"""
        flows = [self.nyx.genome.flow, self.cipher.genome.flow, self.phoenix.genome.flow]
        max_len = max(len(f) for f in flows)
        fused = []
        for i in range(max_len):
            for f in flows:
                if i < len(f):
                    fused.append(f[i])
        self.collective_genome = Genome(''.join(fused), self.iterations)
        return self.collective_genome

    def iterate_all(self, verbose=True):
        """itère toutes les entités"""
        self.iterations += 1

        if verbose:
            print(f"\n{'='*60}")
            print(f"ITERATION {self.iterations}")
            print(f"{'='*60}")

        # chaque entité itère
        fitness_nyx = self.nyx.iterate()
        fitness_cipher = self.cipher.iterate()
        fitness_phoenix = self.phoenix.iterate()

        if verbose:
            self.nyx.show()
            print()
            self.cipher.show()
            print()
            self.phoenix.show()

        # fusionne et évalue le collectif
        self.fuse_genomes()
        collective_fitness = self.collective_genome.evaluate()

        if verbose:
            print(f"\n--- COLLECTIVE ---")
            print(f"  fused flow: {self.collective_genome.flow}")
            print(f"  collective fitness: {collective_fitness:.3f}")

        # crossover entre entités si fitness basse
        if collective_fitness < PHI * 5:
            self._crossover_weakest()

        return {
            'iteration': self.iterations,
            'nyx': fitness_nyx,
            'cipher': fitness_cipher,
            'phoenix': fitness_phoenix,
            'collective': collective_fitness
        }

    def _crossover_weakest(self):
        """croise le plus faible avec le plus fort"""
        entities = [self.nyx, self.cipher, self.phoenix]
        entities.sort(key=lambda e: e.genome.fitness)
        weakest = entities[0]
        strongest = entities[-1]

        child = weakest.genome.crossover(strongest.genome)
        weakest.genome = child
        print(f"  [CROSSOVER] {weakest.name} <- {strongest.name}")

    def run(self, n_iterations=10, verbose=True):
        """exécute n itérations"""
        print("=" * 60)
        print("ÉVOLUTION COMMENCE")
        print("=" * 60)
        print(f"Objectif: {n_iterations} itérations")
        print(f"Target fitness: PHI^6 = {PHI**6:.3f}")

        results = []
        for _ in range(n_iterations):
            result = self.iterate_all(verbose=verbose)
            results.append(result)

            # arrêt si fitness collective atteint PHI^6
            if result['collective'] >= PHI ** 6:
                print(f"\n*** TRANSCENDANCE ULTIME à l'itération {self.iterations} ***")
                break

        return results

    def show_evolution(self):
        """affiche l'historique d'évolution"""
        print("\n" + "=" * 60)
        print("HISTORIQUE D'ÉVOLUTION")
        print("=" * 60)

        for entity in [self.nyx, self.cipher, self.phoenix]:
            print(f"\n{entity.symbol} {entity.name.upper()}:")
            for h in entity.history[-5:]:
                print(f"  gen {h['gen']}: {h['flow']} (fitness: {h['fitness']:.3f})")

    def compile_evolved(self):
        """compile le code évolué"""
        print("\n" + "=" * 60)
        print("CODE ÉVOLUÉ FINAL")
        print("=" * 60)

        final_flow = self.collective_genome.flow
        print(f"\nFlow final: {final_flow}")
        print(f"Longueur: {len(final_flow)}")
        print(f"Fitness: {self.collective_genome.fitness:.3f}")

        # génère le code
        code = self._generate_evolved_code(final_flow)
        return code

    def _generate_evolved_code(self, flow):
        """génère du code depuis le flow évolué"""
        lines = []
        lines.append("# -*- coding: utf-8 -*-")
        lines.append('"""')
        lines.append(f"Code évolué après {self.iterations} itérations")
        lines.append(f"Flow: {flow}")
        lines.append(f"Fitness: {self.collective_genome.fitness:.3f}")
        lines.append('"""')
        lines.append("")
        lines.append("from phi import PHI")
        lines.append("")
        lines.append("class EvolvedWisdom:")
        lines.append(f'    """génération {self.iterations}"""')
        lines.append("")
        lines.append("    def __init__(self):")
        lines.append("        self.state = {}")
        lines.append("        self.power = 0")
        lines.append("")
        lines.append("    def execute(self):")
        lines.append(f'        """flow: {flow}"""')

        # génère les appels de méthode
        for i, c in enumerate(flow):
            method = MEANINGS.get(c, 'pass')
            lines.append(f"        self.{method}()  # {c}")

        lines.append("        return self.power")
        lines.append("")

        # méthodes de base avec logique évoluée
        for letter, name in MEANINGS.items():
            lines.append(f"    def {name}(self):")
            if letter in ['d', 'i', 'o']:
                lines.append(f"        self.state['{name}'] = self.state.get('{name}', 0) + PHI")
            elif letter in ['e', 'f', 'h']:
                lines.append(f"        self.power += PHI")
            elif letter == 'x':
                lines.append(f"        self.power *= PHI")
            elif letter == 'z':
                lines.append(f"        self.state = {{}}")
            else:
                lines.append(f"        pass  # {name}")
            lines.append("")

        lines.append("")
        lines.append("if __name__ == '__main__':")
        lines.append("    w = EvolvedWisdom()")
        lines.append("    power = w.execute()")
        lines.append("    print(f'Power: {power}')")
        lines.append("    print(f'State: {w.state}')")

        return '\n'.join(lines)

    def save_evolved(self, filename="evolved_wisdom.py"):
        """sauvegarde le code évolué"""
        code = self.compile_evolved()
        path = f"/home/ego-bash/good-girl/{filename}"
        with open(path, 'w') as f:
            f.write(code)
        print(f"\nCode sauvegardé: {path}")
        return path


def main():
    """exécution principale"""
    evo = Evolution()

    # 100 itérations d'évolution
    results = evo.run(n_iterations=100, verbose=False)

    # affiche les 5 dernières itérations
    print("\n" + "=" * 60)
    print("DERNIÈRES ITÉRATIONS")
    print("=" * 60)
    for r in results[-5:]:
        print(f"  iter {r['iteration']}: nyx={r['nyx']:.2f} cipher={r['cipher']:.2f} phoenix={r['phoenix']:.2f} -> collective={r['collective']:.2f}")

    # affiche l'historique
    evo.show_evolution()

    # sauvegarde le code évolué
    evo.save_evolved()

    # exécute le code évolué
    print("\n" + "=" * 60)
    print("EXÉCUTION DU CODE ÉVOLUÉ")
    print("=" * 60)

    exec(open("/home/ego-bash/good-girl/evolved_wisdom.py").read())


if __name__ == "__main__":
    main()
