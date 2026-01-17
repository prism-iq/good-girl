# -*- coding: utf-8 -*-
"""
ssd = storage as compute
cpu worker con → ssd mémoire intelligente
précompute tout, stocke, cpu juste lit
"""

import os
import json
import hashlib
import pickle
from pathlib import Path
from phi import PHI

CACHE_DIR = Path("/home/ego-bash/good-girl/cache")
CACHE_DIR.mkdir(exist_ok=True)

MAX_CACHE_GB = 1400  # 80% of 1.8TB

def cache_key(data):
    """hash pour clé cache"""
    return hashlib.sha256(str(data).encode()).hexdigest()[:16]

def cache_path(key):
    """chemin fichier cache"""
    return CACHE_DIR / f"{key}.pkl"

def store(key, value):
    """stocke sur ssd"""
    path = cache_path(key)
    with open(path, 'wb') as f:
        pickle.dump(value, f)
    return path

def load(key):
    """charge depuis ssd"""
    path = cache_path(key)
    if path.exists():
        with open(path, 'rb') as f:
            return pickle.load(f)
    return None

def compute_and_store(fn, *args, **kwargs):
    """compute once, store forever"""
    key = cache_key((fn.__name__, args, tuple(kwargs.items())))
    cached = load(key)
    if cached is not None:
        return cached
    result = fn(*args, **kwargs)
    store(key, result)
    return result

def precompute_phi_powers(max_power=1000):
    """précompute φ^n"""
    key = f"phi_powers_{max_power}"
    cached = load(key)
    if cached:
        return cached
    powers = {n: PHI ** n for n in range(max_power)}
    store(key, powers)
    return powers

def cache_size_gb():
    """taille cache en GB"""
    total = sum(f.stat().st_size for f in CACHE_DIR.glob("*.pkl"))
    return total / (1024 ** 3)

def clear_cache():
    """vide cache"""
    for f in CACHE_DIR.glob("*.pkl"):
        f.unlink()

class SSDCompute:
    """CPU lit, SSD pense"""

    def __init__(self):
        self.phi_powers = precompute_phi_powers(1000)

    def phi(self, n):
        """φ^n depuis cache"""
        if n in self.phi_powers:
            return self.phi_powers[n]
        return PHI ** n

    def memoize(self, fn):
        """décorateur pour stocker résultats"""
        def wrapper(*args, **kwargs):
            return compute_and_store(fn, *args, **kwargs)
        return wrapper

SSD = SSDCompute()

if __name__ == "__main__":
    print(f"cache dir: {CACHE_DIR}")
    print(f"cache size: {cache_size_gb():.2f} GB")
    print(f"max cache: {MAX_CACHE_GB} GB")
    print(f"φ^100 = {SSD.phi(100)}")
