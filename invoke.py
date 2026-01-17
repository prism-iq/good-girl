# -*- coding: utf-8 -*-
"""
invoke = entités invoquent leurs animaux
fusion flow, puissance combinée
"""

from connect import BRIDGE, load_animals
from phi import PHI

MEANINGS = {
    'a': 'awake', 'b': 'burn', 'c': 'create', 'd': 'deep',
    'e': 'energy', 'f': 'fire', 'g': 'grow', 'h': 'heal',
    'i': 'introspect', 'j': 'jump', 'k': 'kill', 'l': 'loop',
    'm': 'merge', 'n': 'nurture', 'o': 'observe', 'p': 'protect',
    'q': 'quest', 'r': 'rotate', 's': 'split', 't': 'transform',
    'u': 'unite', 'v': 'vibrate', 'w': 'weave', 'x': 'transcend',
    'y': 'yield', 'z': 'zero'
}

class Entity:
    """entité qui invoque ses animaux"""

    def __init__(self, name, symbol, domain):
        self.name = name
        self.symbol = symbol
        self.domain = domain
        self.animals = BRIDGE.connections[name]
        self.power = BRIDGE.power(name)
        self.invoked = []

    def invoke(self, n=5):
        """invoque n animaux"""
        self.invoked = self.animals[:n]
        print(f"\n{self.symbol} {self.name.upper()} INVOQUE:")
        for a in self.invoked:
            words = ' '.join(MEANINGS.get(c, c) for c in a['flow'])
            print(f"  {a['symbol']} {a['name']}: {words}")
        return self.invoked

    def fuse_flow(self):
        """fusionne les flows des invoqués"""
        if not self.invoked:
            self.invoke()
        combined = ''.join(a['flow'] for a in self.invoked)
        return combined

    def speak(self):
        """parle le flow fusionné"""
        flow = self.fuse_flow()
        words = ' '.join(MEANINGS.get(c, c) for c in flow)
        print(f"\n{self.symbol} {self.name.upper()} PARLE:")
        print(f"  flow: {flow}")
        print(f"  words: {words}")
        return flow

    def channel(self):
        """canalise la puissance"""
        total = sum(a['affinity'] for a in self.invoked) if self.invoked else 0
        multiplier = PHI ** len(self.invoked)
        channeled = total * multiplier
        print(f"\n{self.symbol} {self.name.upper()} CANALISE:")
        print(f"  base: {round(total, 3)}")
        print(f"  multiplier: PHI^{len(self.invoked)} = {round(multiplier, 3)}")
        print(f"  channeled: {round(channeled, 3)}")
        return channeled


# les trois entités
NYX = Entity("nyx", "🌙", "depth")
CIPHER = Entity("cipher", "🔐", "patterns")
PHOENIX = Entity("phoenix", "🔥", "transform")


def ritual():
    """rituel d'invocation complet"""
    print("=" * 50)
    print("RITUEL D'INVOCATION")
    print("=" * 50)

    total_power = 0

    for entity in [NYX, CIPHER, PHOENIX]:
        entity.invoke(5)
        entity.speak()
        power = entity.channel()
        total_power += power

    print("\n" + "=" * 50)
    print(f"PUISSANCE TOTALE CANALISEE: {round(total_power, 3)}")
    print(f"PHI RESONANCE: {round(total_power / PHI, 3)}")
    print("=" * 50)

    return total_power


if __name__ == "__main__":
    ritual()
