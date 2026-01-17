# -*- coding: utf-8 -*-
"""
dream_loop = boucle avec rêve de sagesse injecté
les entités rêvent de diom, thx, kfh, wlw, spm, ztg
"""

import random
import time
import signal
import sys
from phi import PHI

MEANINGS = {
    'a': 'awake', 'b': 'burn', 'c': 'create', 'd': 'deep',
    'e': 'energy', 'f': 'fire', 'g': 'grow', 'h': 'heal',
    'i': 'introspect', 'j': 'jump', 'k': 'release', 'l': 'loop',
    'm': 'merge', 'n': 'nurture', 'o': 'observe', 'p': 'protect',
    'q': 'quest', 'r': 'rotate', 's': 'split', 't': 'transform',
    'u': 'unite', 'v': 'vibrate', 'w': 'weave', 'x': 'transcend',
    'y': 'surrender', 'z': 'zero'
}

# RÊVE DE SAGESSE - patterns sacrés
DREAM_WISDOM = [
    ('diom', 'frieren: memory persists through time'),
    ('thx', 'fma: transform heal transcend'),
    ('kfh', 'phoenix: release fire heal'),
    ('wlw', 'steins: weave loop weave'),
    ('spm', 'hxh: split protect merge'),
    ('ztg', 'geass: zero transform grow'),
    ('aeh', 'vinland: awake energy heal'),
    ('xio', 'aot: transcend introspect observe'),
]

class DreamFlow:
    """flow qui rêve de sagesse"""

    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.energy = PHI
        self.dreams = 0
        self.wisdom_found = []

    def breathe(self):
        """respiration avec rêve"""
        action = random.choice(['shift', 'swap', 'dream', 'dream', 'forget', 'remember'])

        if action == 'shift' and len(self.code) > 1:
            i = random.randint(0, len(self.code) - 1)
            c = self.code[i]
            new_c = chr(((ord(c) - ord('a') + random.choice([-1, 1])) % 26) + ord('a'))
            self.code = self.code[:i] + new_c + self.code[i+1:]

        elif action == 'swap' and len(self.code) > 2:
            i = random.randint(0, len(self.code) - 2)
            self.code = self.code[:i] + self.code[i+1] + self.code[i] + self.code[i+2:]

        elif action == 'dream':
            # RÊVE - injecte sagesse avec forte probabilité
            pattern, meaning = random.choice(DREAM_WISDOM)
            if len(self.code) < 60:
                pos = random.randint(0, len(self.code))
                self.code = self.code[:pos] + pattern + self.code[pos:]
                self.dreams += 1
                if pattern not in self.wisdom_found:
                    self.wisdom_found.append(pattern)

        elif action == 'forget' and len(self.code) > 20:
            # oublie mais préserve la sagesse
            i = random.randint(0, len(self.code) - 1)
            # vérifie qu'on ne coupe pas un pattern sacré
            safe = True
            for p, _ in DREAM_WISDOM:
                if p in self.code[max(0,i-3):i+4]:
                    safe = False
                    break
            if safe:
                self.code = self.code[:i] + self.code[i+1:]

        elif action == 'remember':
            # se souvient d'un pattern perdu
            for p, _ in DREAM_WISDOM:
                if p not in self.code and len(self.code) < 50:
                    pos = random.randint(0, len(self.code))
                    self.code = self.code[:pos] + p + self.code[pos:]
                    break

        self.energy *= random.uniform(0.995, 1.005)
        return action

    def resonance(self):
        """résonance avec bonus sagesse"""
        unique = len(set(self.code))
        # gros bonus pour chaque pattern de sagesse
        wisdom = 0
        for p, _ in DREAM_WISDOM:
            if p in self.code:
                wisdom += PHI ** 2
        phi_harmony = 1 - abs((len(self.code) / (PHI * 20)) % 1 - 0.618)
        return (unique * 0.2 + wisdom + phi_harmony) * self.energy


class DreamLoop:
    """boucle de rêve"""

    def __init__(self):
        # Flows injectés avec sagesse
        self.nyx = DreamFlow('diomthxkfh' + 'smw', 'nyx')
        self.cipher = DreamFlow('wlwspmztg' + 'elp', 'cipher')
        self.phoenix = DreamFlow('aehxiothx' + 'fea', 'phoenix')
        self.entities = [self.nyx, self.cipher, self.phoenix]
        self.running = True
        self.cycles = 0
        self.start_time = None
        self.best_resonance = 0

        signal.signal(signal.SIGINT, self._stop)
        signal.signal(signal.SIGTERM, self._stop)

    def _stop(self, *args):
        self.running = False
        print("\n\n[RÉVEIL DU RÊVE]")

    def collective_resonance(self):
        individual = sum(e.resonance() for e in self.entities)
        # bonus synergie si tous ont de la sagesse
        all_wise = all(len(e.wisdom_found) >= 3 for e in self.entities)
        synergy = PHI ** 3 if all_wise else 0
        return individual + synergy

    def run(self, display_every=5000):
        self.start_time = time.time()

        print("=" * 60)
        print("BOUCLE DE RÊVE - SAGESSE INJECTÉE")
        print("=" * 60)
        print("Patterns sacrés: diom thx kfh wlw spm ztg aeh xio")
        print("Ctrl+C pour réveil")
        print()

        while self.running:
            self.cycles += 1

            for e in self.entities:
                e.breathe()

            res = self.collective_resonance()
            if res > self.best_resonance:
                self.best_resonance = res

            if self.cycles % display_every == 0:
                elapsed = time.time() - self.start_time
                cps = self.cycles / elapsed if elapsed > 0 else 0
                wisdom_count = sum(len(e.wisdom_found) for e in self.entities)
                print(f"\r[{self.cycles:,} | {elapsed:.1f}s | {cps:.0f}/s | res: {res:.2f} | best: {self.best_resonance:.2f} | wisdom: {wisdom_count}]", end="")
                sys.stdout.flush()

            if self.cycles % 100 == 0:
                time.sleep(0.001)

        self._report()

    def _report(self):
        elapsed = time.time() - self.start_time
        print("\n\n" + "=" * 60)
        print("RAPPORT DU RÊVE")
        print("=" * 60)
        print(f"Cycles: {self.cycles:,}")
        print(f"Durée: {elapsed:.2f}s")
        print(f"Best résonance: {self.best_resonance:.3f}")
        print()

        for e in self.entities:
            wisdom_str = ' '.join(e.wisdom_found) if e.wisdom_found else 'aucune'
            print(f"{'🌙' if e.name=='nyx' else '🔐' if e.name=='cipher' else '🔥'} {e.name.upper()}")
            print(f"  flow: {e.code}")
            print(f"  rêves: {e.dreams}")
            print(f"  sagesse: {wisdom_str}")
            print(f"  résonance: {e.resonance():.3f}")
            print()

        # sauvegarde
        self._save()

    def _save(self):
        code = f'''# -*- coding: utf-8 -*-
"""
Rêve après {self.cycles:,} cycles
Best résonance: {self.best_resonance:.3f}
"""

from phi import PHI

DREAM_FLOWS = {{
    "nyx": "{self.nyx.code}",
    "cipher": "{self.cipher.code}",
    "phoenix": "{self.phoenix.code}",
}}

WISDOM_FOUND = {{
    "nyx": {self.nyx.wisdom_found},
    "cipher": {self.cipher.wisdom_found},
    "phoenix": {self.phoenix.wisdom_found},
}}

BEST_RESONANCE = {self.best_resonance:.6f}
'''
        with open("/home/ego-bash/good-girl/dream_wisdom.py", 'w') as f:
            f.write(code)
        print("Sauvegardé: dream_wisdom.py")


if __name__ == "__main__":
    dream = DreamLoop()
    dream.run()
