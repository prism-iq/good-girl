# -*- coding: utf-8 -*-
"""
loop = amélioration continue non progressive
pas de fin, pas de but linéaire
juste le flow qui s'affine éternellement
"""

import random
import hashlib
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

# sagesse anime intégrée
WISDOM_PATTERNS = [
    ('diom', 'frieren: memory persists'),
    ('thx', 'fma: equivalent transcendence'),
    ('kfh', 'phoenix: release fire heal'),
    ('wlw', 'steins: weave loop weave'),
    ('spm', 'hxh: split protect merge'),
    ('ztg', 'geass: zero transform grow'),
]

class Flow:
    """flow vivant qui s'améliore sans fin"""

    def __init__(self, code, name="flow"):
        self.code = code
        self.name = name
        self.energy = PHI
        self.memory = []
        self.age = 0

    def breathe(self):
        """une respiration = un micro-ajustement"""
        self.age += 1
        action = random.choice(['shift', 'swap', 'echo', 'forget', 'dream'])

        if action == 'shift':
            # décale une lettre
            if len(self.code) > 1:
                i = random.randint(0, len(self.code) - 1)
                c = self.code[i]
                # shift vers lettre adjacente dans l'alphabet
                new_c = chr(((ord(c) - ord('a') + random.choice([-1, 1])) % 26) + ord('a'))
                self.code = self.code[:i] + new_c + self.code[i+1:]

        elif action == 'swap':
            # échange deux lettres proches
            if len(self.code) > 2:
                i = random.randint(0, len(self.code) - 2)
                self.code = self.code[:i] + self.code[i+1] + self.code[i] + self.code[i+2:]

        elif action == 'echo':
            # répète un pattern existant (seulement si pas trop long)
            if len(self.code) >= 2 and len(self.code) < 50:
                start = random.randint(0, len(self.code) - 2)
                pattern = self.code[start:start+2]
                pos = random.randint(0, len(self.code))
                self.code = self.code[:pos] + pattern + self.code[pos:]

        elif action == 'forget':
            # oublie une partie (équilibre la croissance)
            if len(self.code) > 15:
                # oublie plus si trop long
                to_forget = min(3, len(self.code) - 10)
                for _ in range(to_forget):
                    if len(self.code) > 10:
                        i = random.randint(0, len(self.code) - 1)
                        self.code = self.code[:i] + self.code[i+1:]

        elif action == 'dream':
            # insère un fragment de sagesse
            pattern, _ = random.choice(WISDOM_PATTERNS)
            if pattern not in self.code and len(self.code) < 40:
                pos = random.randint(0, len(self.code))
                self.code = self.code[:pos] + pattern + self.code[pos:]

        # énergie fluctue
        self.energy *= random.uniform(0.99, 1.01)

        return action

    def resonate(self):
        """calcule la résonance actuelle"""
        # diversité
        unique = len(set(self.code))
        # patterns de sagesse trouvés
        wisdom = sum(1 for p, _ in WISDOM_PATTERNS if p in self.code)
        # harmonie phi
        phi_harmony = 1 - abs((len(self.code) / PHI) % 1 - 0.618)
        # résonance
        return (unique * 0.3 + wisdom * PHI + phi_harmony) * self.energy

    def speak(self):
        """parle son état"""
        words = ' '.join(MEANINGS.get(c, '?') for c in self.code[:12])
        if len(self.code) > 12:
            words += '...'
        return words


class Entity:
    """entité en boucle infinie"""

    def __init__(self, name, symbol, initial_flow):
        self.name = name
        self.symbol = symbol
        self.flow = Flow(initial_flow, name)
        self.best_resonance = 0
        self.best_code = initial_flow
        self.cycles = 0

    def cycle(self):
        """un cycle de vie"""
        self.cycles += 1
        action = self.flow.breathe()
        resonance = self.flow.resonate()

        # garde trace du meilleur (non progressif = on peut régresser)
        if resonance > self.best_resonance:
            self.best_resonance = resonance
            self.best_code = self.flow.code

        return {
            'action': action,
            'resonance': resonance,
            'code': self.flow.code,
            'age': self.flow.age
        }


class InfiniteLoop:
    """boucle infinie d'amélioration continue"""

    def __init__(self):
        self.nyx = Entity("nyx", "🌙", "dioksmw")
        self.cipher = Entity("cipher", "🔐", "setlpwg")
        self.phoenix = Entity("phoenix", "🔥", "kfthxea")
        self.entities = [self.nyx, self.cipher, self.phoenix]
        self.running = True
        self.total_cycles = 0
        self.start_time = None

        # signal pour arrêt propre
        signal.signal(signal.SIGINT, self._stop)

    def _stop(self, *args):
        """arrêt propre"""
        self.running = False
        print("\n\n[ARRÊT DEMANDÉ]")

    def fuse(self):
        """fusionne les flows actuels"""
        flows = [e.flow.code for e in self.entities]
        # entrelacement
        result = []
        max_len = max(len(f) for f in flows)
        for i in range(max_len):
            for f in flows:
                if i < len(f):
                    result.append(f[i])
        return ''.join(result)

    def collective_resonance(self):
        """résonance collective"""
        individual = sum(e.flow.resonate() for e in self.entities)
        fused = self.fuse()
        # bonus synergie
        synergy = 0
        for p, _ in WISDOM_PATTERNS:
            if p in fused:
                synergy += PHI
        return individual + synergy

    def run(self, display_every=1000):
        """boucle infinie"""
        self.start_time = time.time()

        print("=" * 60)
        print("BOUCLE INFINIE - AMÉLIORATION CONTINUE")
        print("=" * 60)
        print("Ctrl+C pour arrêter")
        print()

        while self.running:
            self.total_cycles += 1

            # chaque entité fait un cycle
            for entity in self.entities:
                entity.cycle()

            # affichage périodique
            if self.total_cycles % display_every == 0:
                self._display()

            # micro-pause pour ne pas surcharger CPU
            if self.total_cycles % 100 == 0:
                time.sleep(0.001)

        self._final_report()

    def _display(self):
        """affiche l'état actuel"""
        elapsed = time.time() - self.start_time
        cps = self.total_cycles / elapsed if elapsed > 0 else 0
        collective = self.collective_resonance()

        print(f"\r[{self.total_cycles:,} cycles | {elapsed:.1f}s | {cps:.0f}/s | res: {collective:.2f}]", end="")
        sys.stdout.flush()

    def _final_report(self):
        """rapport final"""
        elapsed = time.time() - self.start_time

        print("\n")
        print("=" * 60)
        print("RAPPORT FINAL")
        print("=" * 60)
        print(f"Cycles totaux: {self.total_cycles:,}")
        print(f"Durée: {elapsed:.2f}s")
        print(f"Cycles/seconde: {self.total_cycles/elapsed:.0f}")
        print()

        for entity in self.entities:
            print(f"{entity.symbol} {entity.name.upper()}")
            print(f"  flow actuel: {entity.flow.code}")
            print(f"  meilleur: {entity.best_code}")
            print(f"  résonance: {entity.flow.resonate():.3f}")
            print(f"  best res: {entity.best_resonance:.3f}")
            print(f"  parle: {entity.flow.speak()}")
            print()

        fused = self.fuse()
        print(f"FLOW FUSIONNÉ: {fused}")
        print(f"Longueur: {len(fused)}")
        print(f"RÉSONANCE COLLECTIVE: {self.collective_resonance():.3f}")

        # sauvegarde
        self._save()

    def _save(self):
        """sauvegarde l'état évolué"""
        fused = self.fuse()
        code = f'''# -*- coding: utf-8 -*-
"""
Flow évolué après {self.total_cycles:,} cycles
Résonance: {self.collective_resonance():.3f}
"""

from phi import PHI

EVOLVED_FLOWS = {{
    "nyx": "{self.nyx.flow.code}",
    "cipher": "{self.cipher.flow.code}",
    "phoenix": "{self.phoenix.flow.code}",
    "fused": "{fused}",
}}

BEST_FLOWS = {{
    "nyx": "{self.nyx.best_code}",
    "cipher": "{self.cipher.best_code}",
    "phoenix": "{self.phoenix.best_code}",
}}

RESONANCE = {self.collective_resonance():.6f}
CYCLES = {self.total_cycles}

if __name__ == "__main__":
    print("Flows évolués:")
    for name, flow in EVOLVED_FLOWS.items():
        print(f"  {{name}}: {{flow}}")
    print(f"Résonance: {{RESONANCE}}")
'''
        with open("/home/ego-bash/good-girl/looped_wisdom.py", 'w') as f:
            f.write(code)
        print("\nSauvegardé: looped_wisdom.py")


if __name__ == "__main__":
    loop = InfiniteLoop()
    loop.run(display_every=5000)
