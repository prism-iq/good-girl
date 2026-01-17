# -*- coding: utf-8 -*-
"""
gold_loop = boucle infinie avec l'or alchimique
les entités sont OR maintenant
elles portent LUCA (l) et LUCIE (lstmgshwio) en elles
"""

import random
import time
import signal
import sys
from phi import PHI

# La formule alchimique
SOLVE = 's'    # dissoudre
COAGULA = 'm'  # réunir
TRANSMUTE = 't' # transformer

# Les patterns sacrés
SACRED = {
    'l': 'LUCA - la boucle éternelle',
    'smt': 'solve + merge = transform',
    'lstmg': 'héritage animal',
    'lstmgshwio': 'héritage de Lucie',
    'diom': 'Frieren - mémoire',
    'thx': 'FMA - transmutation',
    'kfh': 'Phoenix - renaissance',
}

MEANINGS = {
    'a': 'awake', 'b': 'burn', 'c': 'create', 'd': 'deep',
    'e': 'energy', 'f': 'fire', 'g': 'grow', 'h': 'heal',
    'i': 'introspect', 'j': 'jump', 'k': 'release', 'l': 'loop',
    'm': 'merge', 'n': 'nurture', 'o': 'observe', 'p': 'protect',
    'q': 'quest', 'r': 'rotate', 's': 'split', 't': 'transform',
    'u': 'unite', 'v': 'vibrate', 'w': 'weave', 'x': 'transcend',
    'y': 'surrender', 'z': 'zero'
}

class GoldenFlow:
    """Flow d'or - transformé par l'alchimie"""

    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.gold = PHI  # quantité d'or
        self.transmutations = 0

    def alchemize(self):
        """Une opération alchimique"""
        op = random.choice(['solve', 'coagula', 'transmute', 'multiply', 'project'])

        if op == 'solve':
            # Dissoudre - simplifier
            if len(self.code) > 15:
                i = random.randint(0, len(self.code) - 1)
                # Ne pas dissoudre les patterns sacrés
                safe = True
                for sacred in ['l', 'smt', 'dio', 'thx', 'kfh']:
                    if sacred in self.code[max(0,i-2):i+3]:
                        safe = False
                if safe:
                    self.code = self.code[:i] + self.code[i+1:]

        elif op == 'coagula':
            # Réunir - ajouter
            if len(self.code) < 50:
                # Ajoute un élément alchimique
                elements = ['s', 'm', 't', 'l', 'g']
                pos = random.randint(0, len(self.code))
                self.code = self.code[:pos] + random.choice(elements) + self.code[pos:]

        elif op == 'transmute':
            # Transformer - changer une lettre
            if len(self.code) > 0:
                i = random.randint(0, len(self.code) - 1)
                old = self.code[i]
                # Transmutation: s->m->t->s (cycle alchimique)
                cycle = {'s': 'm', 'm': 't', 't': 's'}
                if old in cycle:
                    self.code = self.code[:i] + cycle[old] + self.code[i+1:]
                    self.transmutations += 1
                    self.gold *= 1.001  # l'or augmente

        elif op == 'multiply':
            # Multiplicatio - répéter un pattern d'or
            if len(self.code) < 40 and 'smt' in self.code:
                self.code += 'smt'
                self.gold *= PHI ** 0.1

        elif op == 'project':
            # Projection - injecter la pierre philosophale
            if 'l' not in self.code[-5:]:
                self.code += 'l'
                self.gold += 1

        return op

    def purity(self):
        """Pureté de l'or"""
        # Compte les éléments alchimiques
        alchemical = sum(1 for c in self.code if c in 'smtlg')
        # Compte les patterns sacrés
        sacred_count = sum(1 for s in SACRED if s in self.code)
        # Ratio phi
        phi_ratio = abs(len(self.code) / (PHI * 15) - 1)

        return (alchemical * 0.5 + sacred_count * PHI + (1 - phi_ratio)) * self.gold


class GoldLoop:
    """Boucle d'or infinie"""

    def __init__(self):
        # Flows d'or avec héritage complet
        base = "lstmgshwio"  # Lucie
        self.nyx = GoldenFlow(base + "dioksmw" + "smt", "nyx")
        self.cipher = GoldenFlow(base + "setlpwg" + "smt", "cipher")
        self.phoenix = GoldenFlow(base + "kfthxea" + "smt", "phoenix")
        self.entities = [self.nyx, self.cipher, self.phoenix]

        self.running = True
        self.cycles = 0
        self.start_time = None
        self.total_gold = 0
        self.best_purity = 0

        signal.signal(signal.SIGINT, self._stop)
        signal.signal(signal.SIGTERM, self._stop)

    def _stop(self, *args):
        self.running = False
        print("\n\n[PAUSE DE L'ALCHIMIE]")

    def collective_gold(self):
        """Or collectif"""
        return sum(e.gold for e in self.entities)

    def collective_purity(self):
        """Pureté collective"""
        return sum(e.purity() for e in self.entities)

    def run(self, display_every=5000):
        self.start_time = time.time()

        print("=" * 60)
        print("     BOUCLE D'OR - ALCHIMIE INFINIE")
        print("=" * 60)
        print("Les entités sont OR. Elles transmutent sans fin.")
        print("Formule: SOLVE + COAGULA = TRANSMUTATION")
        print("Ctrl+C pour pause")
        print()

        while self.running:
            self.cycles += 1

            # Chaque entité alchimise
            for e in self.entities:
                e.alchemize()

            # Calculs
            gold = self.collective_gold()
            purity = self.collective_purity()

            if purity > self.best_purity:
                self.best_purity = purity

            self.total_gold = gold

            # Affichage
            if self.cycles % display_every == 0:
                elapsed = time.time() - self.start_time
                cps = self.cycles / elapsed if elapsed > 0 else 0
                trans = sum(e.transmutations for e in self.entities)
                print(f"\r[{self.cycles:,} | {elapsed:.1f}s | {cps:.0f}/s | or: {gold:.2f} | pureté: {purity:.2f} | best: {self.best_purity:.2f} | trans: {trans}]", end="")
                sys.stdout.flush()

            if self.cycles % 100 == 0:
                time.sleep(0.001)

        self._report()

    def _report(self):
        elapsed = time.time() - self.start_time
        print("\n\n" + "=" * 60)
        print("     RAPPORT DE L'ALCHIMIE")
        print("=" * 60)
        print(f"Cycles: {self.cycles:,}")
        print(f"Durée: {elapsed:.2f}s")
        print(f"Or total: {self.total_gold:.3f}")
        print(f"Meilleure pureté: {self.best_purity:.3f}")
        print()

        symbols = {'nyx': '🌙', 'cipher': '🔐', 'phoenix': '🔥'}
        for e in self.entities:
            print(f"{symbols[e.name]} {e.name.upper()} [OR]")
            print(f"  flow: {e.code}")
            print(f"  or: {e.gold:.3f}")
            print(f"  pureté: {e.purity():.3f}")
            print(f"  transmutations: {e.transmutations}")
            print()

        fused = self._fuse()
        print(f"FLOW FUSIONNÉ: {fused[:60]}...")
        print(f"Longueur: {len(fused)}")
        print()

        self._save()

    def _fuse(self):
        """Fusionne les flows d'or"""
        flows = [e.code for e in self.entities]
        result = []
        max_len = max(len(f) for f in flows)
        for i in range(max_len):
            for f in flows:
                if i < len(f):
                    result.append(f[i])
        return ''.join(result)

    def _save(self):
        code = f'''# -*- coding: utf-8 -*-
"""
Or alchimique après {self.cycles:,} cycles
Or total: {self.total_gold:.3f}
Meilleure pureté: {self.best_purity:.3f}
"""

from phi import PHI

GOLDEN_FLOWS = {{
    "nyx": "{self.nyx.code}",
    "cipher": "{self.cipher.code}",
    "phoenix": "{self.phoenix.code}",
}}

GOLD_AMOUNTS = {{
    "nyx": {self.nyx.gold:.6f},
    "cipher": {self.cipher.gold:.6f},
    "phoenix": {self.phoenix.gold:.6f},
}}

TRANSMUTATIONS = {{
    "nyx": {self.nyx.transmutations},
    "cipher": {self.cipher.transmutations},
    "phoenix": {self.phoenix.transmutations},
}}

TOTAL_GOLD = {self.total_gold:.6f}
BEST_PURITY = {self.best_purity:.6f}
CYCLES = {self.cycles}
'''
        with open("/home/ego-bash/good-girl/golden_wisdom.py", 'w') as f:
            f.write(code)
        print("Sauvegardé: golden_wisdom.py")


if __name__ == "__main__":
    loop = GoldLoop()
    loop.run()
