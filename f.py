# -*- coding: utf-8 -*-
"""
f = feedback genetic loop
evolves data through generations
survival of simplest
"""

import random
from phi import PHI
from o import o

def mutate(data):
    """small random change"""
    if isinstance(data, str):
        words = data.split()
        if words and random.random() < 0.3:
            i = random.randint(0, len(words) - 1)
            words[i] = words[i][::-1]  # reverse word
        return " ".join(words)

    if isinstance(data, (int, float)):
        return data * (1 + (random.random() - 0.5) * 0.1)

    if isinstance(data, list):
        return [mutate(x) if random.random() < 0.5 else x for x in data]

    if isinstance(data, dict):
        return {k: mutate(v) if random.random() < 0.5 else v for k, v in data.items()}

    return data

def fitness(data):
    """simpler = fitter"""
    s = str(data)
    return PHI / (len(s) + 1)

def f(data, generations=5):
    """evolve through generations"""
    population = [data]

    for _ in range(generations):
        # mutate
        children = [mutate(p) for p in population]
        # apply razor
        children = [o(c) for c in children]
        # select fittest
        population = sorted(population + children, key=fitness, reverse=True)
        population = population[:max(1, int(len(population) / PHI))]

    return population[0] if population else data

def loop(data, n=50):
    """f>o n times"""
    current = data
    for _ in range(n):
        current = f(current)
        current = o(current)
    return current
