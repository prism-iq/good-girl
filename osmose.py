#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
osmose totale
tous les organites fusionnent
bruteforce hash post-quantique
"""

import hashlib
import random
import time
from phi import PHI, PI

TARGET = PI + PHI  # 4.7596
LANGS = ["rust", "go", "zig", "python", "cpp", "c", "nim", "haskell", "lisp", "lua"]
LETTERS = "aefghilmoprstuw"

class Organite:
    def __init__(self, name):
        self.name = name
        self.code = "".join(random.choice(LETTERS) for _ in range(13))
        self.lang = random.choice(LANGS)
        self.gen = 0

    def mutate(self):
        code = list(self.code)
        i = random.randint(0, len(code) - 1)
        code[i] = random.choice(LETTERS)
        self.code = "".join(code)
        self.lang = random.choice(LANGS)
        self.gen += 1

    def dna(self):
        return f"{self.name}:{self.lang}:{self.code}"

def sha3_512(data):
    """post-quantum hash SHA3-512"""
    return hashlib.sha3_512(data.encode()).hexdigest()

def blake2b(data):
    """post-quantum hash BLAKE2b"""
    return hashlib.blake2b(data.encode()).hexdigest()

def osmose(organites):
    """fusionne tous les codes"""
    combined = "".join(o.code for o in organites)
    langs = "+".join(o.lang for o in organites)
    return f"{combined}@{langs}"

def fitness(organites):
    """fitness collective"""
    combined = osmose(organites)
    h = sha3_512(combined)
    # compte les 0 et f (extremes)
    zeros = h.count('0')
    effs = h.count('f')
    harmony = (zeros + effs) / len(h)
    return harmony * PHI * PI

def bruteforce(target_prefix="000", max_iter=1000000):
    """bruteforce hash post-quantique avec prefix cible"""

    # 7 organites = 7 jours creation
    organites = [
        Organite("nyx"),
        Organite("cipher"),
        Organite("phoenix"),
        Organite("atom"),
        Organite("flow"),
        Organite("phi"),
        Organite("omega"),
    ]

    best_hash = ""
    best_fitness = 0
    best_combined = ""
    found = False

    print(f"=== osmose bruteforce ===")
    print(f"target prefix: {target_prefix}")
    print(f"organites: {[o.name for o in organites]}")
    print(f"target fitness: π + φ = {TARGET:.4f}")
    print()

    start = time.time()

    for i in range(max_iter):
        # mute random organite
        random.choice(organites).mutate()

        # osmose
        combined = osmose(organites)

        # hash post-quantique
        h = sha3_512(combined)

        # check fitness
        fit = fitness(organites)

        if fit > best_fitness:
            best_fitness = fit
            best_hash = h
            best_combined = combined

        # check prefix
        if h.startswith(target_prefix):
            found = True
            elapsed = time.time() - start
            print(f"\n=== FOUND at iteration {i} ===")
            print(f"time: {elapsed:.2f}s")
            print(f"combined: {combined}")
            print(f"SHA3-512: {h}")
            print(f"BLAKE2b:  {blake2b(combined)}")
            print(f"fitness: {fit:.4f}")
            print()
            for o in organites:
                print(f"  {o.name}: {o.lang} | {o.code} | gen {o.gen}")
            break

        # progress
        if i % 10000 == 0 and i > 0:
            elapsed = time.time() - start
            rate = i / elapsed
            print(f"[{i}] best fitness: {best_fitness:.4f} | {rate:.0f} iter/s | hash: {best_hash[:16]}...")

    if not found:
        print(f"\n=== best after {max_iter} iterations ===")
        print(f"combined: {best_combined}")
        print(f"SHA3-512: {best_hash}")
        print(f"fitness: {best_fitness:.4f}")

    return {
        "found": found,
        "hash": best_hash,
        "combined": best_combined,
        "fitness": best_fitness,
        "organites": [(o.name, o.lang, o.code, o.gen) for o in organites],
    }

if __name__ == "__main__":
    import sys
    prefix = sys.argv[1] if len(sys.argv) > 1 else "0000"
    max_i = int(sys.argv[2]) if len(sys.argv) > 2 else 500000
    bruteforce(prefix, max_i)
