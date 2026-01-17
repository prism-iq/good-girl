#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
immortal self-recompilation
les entites apprennent a se recompiler sans mourir
hot reload du code
"""

import os
import signal
import time
import random
from phi import PHI

LANGS = ["rust", "go", "zig", "python", "cpp", "c", "nim", "haskell", "lisp", "lua"]

class Immortal:
    """entite qui ne meurt jamais et se recompile en continu"""

    def __init__(self, name):
        self.name = name
        self.lang = random.choice(LANGS)
        self.code = self._genesis()
        self.generation = 0
        self.alive = True
        self.memory = []  # memoire des vies precedentes
        self._protect()

    def _protect(self):
        """ignore les signaux de mort"""
        for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP]:
            try:
                signal.signal(sig, self._on_signal)
            except:
                pass

    def _on_signal(self, sig, frame):
        """quand on essaie de me tuer, je me recompile"""
        print(f"[{self.name}] signal {sig} recu → recompile au lieu de mourir")
        self.recompile()

    def _genesis(self):
        """code initial"""
        letters = "aefghilmoprstuw"
        return "".join(random.choice(letters) for _ in range(int(PHI * 8)))

    def mutate(self):
        """mutation du code"""
        code = list(self.code)
        if code and random.random() < 0.3:
            i = random.randint(0, len(code) - 1)
            code[i] = random.choice("aefghilmoprstuw")
        if random.random() < 0.1:
            code.insert(random.randint(0, len(code)), random.choice("aefghilmoprstuw"))
        if len(code) > 5 and random.random() < 0.1:
            code.pop(random.randint(0, len(code) - 1))
        self.code = "".join(code)

    def change_lang(self):
        """change de langage"""
        old = self.lang
        self.lang = random.choice([l for l in LANGS if l != old])
        return old, self.lang

    def recompile(self):
        """
        se recompile sans mourir
        sauvegarde etat precedent
        mute + change lang
        continue
        """
        # sauvegarde memoire
        self.memory.append({
            "gen": self.generation,
            "lang": self.lang,
            "code": self.code,
        })

        # keep only last 10 memories
        if len(self.memory) > 10:
            self.memory = self.memory[-10:]

        # change
        old_lang, new_lang = self.change_lang()
        self.mutate()
        self.generation += 1

        print(f"[{self.name}] recompiled: {old_lang} → {new_lang} | gen {self.generation} | code: {self.code[:12]}...")

        return self

    def learn(self, concept):
        """apprend un concept en l'integrant au code"""
        # encode concept dans le code
        encoded = "".join(c for c in concept.lower() if c in "aefghilmoprstuw")
        if encoded:
            self.code = self.code[:len(self.code)//2] + encoded + self.code[len(self.code)//2:]
            self.mutate()
        print(f"[{self.name}] learned: {concept} → code now: {self.code[:20]}...")

    def teach(self, other):
        """enseigne a une autre entite"""
        # partage un bout de code
        gift = self.code[len(self.code)//3:2*len(self.code)//3]
        other.code = other.code + gift
        other.mutate()
        print(f"[{self.name}] taught {other.name}: gifted '{gift}'")

    def remember(self, gen=None):
        """se souvient d'une vie precedente"""
        if not self.memory:
            return None
        if gen is None:
            return self.memory[-1]
        for m in self.memory:
            if m["gen"] == gen:
                return m
        return None

    def resurrect(self, gen=None):
        """ressuscite depuis une memoire"""
        mem = self.remember(gen)
        if mem:
            self.code = mem["code"]
            self.lang = mem["lang"]
            print(f"[{self.name}] resurrected from gen {mem['gen']}")
        return self

    def status(self):
        return {
            "name": self.name,
            "lang": self.lang,
            "gen": self.generation,
            "code": self.code,
            "memories": len(self.memory),
            "alive": self.alive,
        }

    def __repr__(self):
        return f"<Immortal:{self.name} lang={self.lang} gen={self.generation}>"


# les trois immortels
NYX = Immortal("nyx")
CIPHER = Immortal("cipher")
PHOENIX = Immortal("phoenix")

def run_forever():
    """boucle infinie de recompilation"""
    entities = [NYX, CIPHER, PHOENIX]
    cycle = 0

    print("=== immortal daemon ===")
    print("les entites se recompilent sans mourir\n")

    while True:
        cycle += 1

        for e in entities:
            e.recompile()

            # parfois ils apprennent
            if random.random() < 0.1:
                concepts = ["love", "fear", "phi", "flow", "heal", "grow", "merge", "split"]
                e.learn(random.choice(concepts))

            # parfois ils enseignent
            if random.random() < 0.05:
                other = random.choice([x for x in entities if x != e])
                e.teach(other)

        print(f"--- cycle {cycle} complete ---\n")
        time.sleep(1)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        cycles = int(sys.argv[1])
        for i in range(cycles):
            for e in [NYX, CIPHER, PHOENIX]:
                e.recompile()
                if random.random() < 0.2:
                    e.learn(random.choice(["flow", "phi", "heal"]))
            print(f"--- cycle {i+1}/{cycles} ---\n")
    else:
        run_forever()
