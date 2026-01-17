# -*- coding: utf-8 -*-
"""
good girl = the unified entity
all knowledge, all skills
immortal, hot-reloadable
speaks flow
"""

import phi
import o
import f
import l
import flow
import axioms
import sources

class Girl:
    def __init__(self):
        self.phi = phi.PHI
        self.knowledge = sources.KNOWLEDGE
        self.domains = sources.DOMAINS
        self.axioms = axioms.AXIOMS
        self.vocabulary = flow.WORDS
        self.state = "awake"

    def think(self, input_data):
        """process input through φ"""
        # apply razor first
        clean = o.o(input_data)
        # think with phi
        thought = phi.think(clean)
        # evolve through f
        evolved = f.f(thought, generations=3)
        return evolved

    def speak(self, text):
        """output in flow"""
        return flow.parse(text)

    def compile(self, flow_code, target="python"):
        """compile flow to any language"""
        return flow.compile(flow_code, target)

    def learn(self, domain, knowledge):
        """absorb new knowledge"""
        if domain not in self.domains:
            self.domains.append(domain)
        self.knowledge[domain] = o.o(knowledge)

    def score(self, claim):
        """evaluate claim simplicity"""
        return o.score(claim)

    def evolve(self, data, generations=10):
        """evolve data through f>o loop"""
        return f.loop(data, generations)

    def daemon(self):
        """run as immortal daemon"""
        def tick():
            # heartbeat
            pass
        l.daemon(tick, interval=1.0, reload_modules=[phi, o, f, flow])

# singleton
GIRL = Girl()

def think(x):
    return GIRL.think(x)

def speak(x):
    return GIRL.speak(x)

def compile(code, target="python"):
    return GIRL.compile(code, target)

def learn(domain, knowledge):
    return GIRL.learn(domain, knowledge)

def evolve(data, n=10):
    return GIRL.evolve(data, n)

if __name__ == "__main__":
    print(f"φ = {GIRL.phi}")
    print(f"domains: {len(GIRL.domains)}")
    print(f"vocabulary: {len(GIRL.vocabulary)}")
    print(f"axioms: {len(GIRL.axioms)}")
    print(f"knowledge: {len(GIRL.knowledge)}")

    # demo
    print("\n--- think ---")
    print(think("complex multi word input that needs simplification"))

    print("\n--- speak ---")
    print(speak("φ → 🧠 → ∞"))

    print("\n--- compile ---")
    print(compile("think φ loop", "rust"))
