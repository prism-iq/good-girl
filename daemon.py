#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
daemon des trois entites
elles changent de langage a chaque recompilation
"""

import random
import time
import os
import signal
from phi import PHI
from self import Self

# langages disponibles
LANGS = ["rust", "go", "zig", "python", "cpp", "c", "nim", "haskell", "lisp", "lua"]

class Daemon:
    def __init__(self):
        self.entities = {
            "nyx": Self("nyx", random.choice(LANGS)),
            "cipher": Self("cipher", random.choice(LANGS)),
            "phoenix": Self("phoenix", random.choice(LANGS)),
        }
        self.running = True
        self.cycle = 0

    def ask_change_lang(self, entity):
        """demande a l'entite de changer de langage"""
        old = entity.target
        # choix base sur fitness et chaos
        seed = entity.fitness() + random.random()
        new = LANGS[int(seed * 1000) % len(LANGS)]
        entity.target = new
        return old, new

    def recompile(self, entity):
        """recompile avec nouveau langage"""
        old, new = self.ask_change_lang(entity)
        entity.evolve(3)  # evolue un peu
        code = entity.compile()
        return {
            "name": entity.name,
            "old_lang": old,
            "new_lang": new,
            "gen": entity.generation,
            "fitness": entity.fitness(),
            "code_preview": entity.code[:20],
        }

    def tick(self):
        """un cycle du daemon"""
        self.cycle += 1
        results = []

        for name, entity in self.entities.items():
            result = self.recompile(entity)
            results.append(result)
            print(f"[{self.cycle}] {name}: {result['old_lang']} → {result['new_lang']} | gen {result['gen']} | fitness {result['fitness']:.6f}")

        return results

    def immortal(self):
        """ignore kill signals"""
        for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP]:
            try:
                signal.signal(sig, lambda s, f: None)
            except:
                pass

    def run(self, interval=2.0, max_cycles=None):
        """run daemon"""
        self.immortal()
        print(f"=== daemon started ===")
        print(f"entities: {list(self.entities.keys())}")
        print(f"langs: {LANGS}")
        print()

        try:
            while self.running:
                self.tick()
                print()

                if max_cycles and self.cycle >= max_cycles:
                    break

                time.sleep(interval)
        except KeyboardInterrupt:
            pass  # immortal mais on peut quitter avec ctrl+c x2

        print(f"\n=== daemon stopped after {self.cycle} cycles ===")

    def status(self):
        """status de toutes les entites"""
        return {name: {
            "lang": e.target,
            "gen": e.generation,
            "fitness": e.fitness(),
            "code": e.code,
        } for name, e in self.entities.items()}


# singleton
DAEMON = Daemon()

def start(interval=2.0, max_cycles=None):
    """lance le daemon"""
    DAEMON.run(interval, max_cycles)

def status():
    """status"""
    return DAEMON.status()

if __name__ == "__main__":
    import sys
    cycles = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    start(interval=1.0, max_cycles=cycles)
