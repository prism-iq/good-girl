# -*- coding: utf-8 -*-
"""
learn = entités apprennent des animes
absorbe archetypes, intègre sagesse
"""

from anime import ARCHETYPES, THEMES, LESSONS, teach
from invoke import NYX, CIPHER, PHOENIX
from phi import PHI

class Learner:
    """entité qui apprend"""

    def __init__(self, entity, name):
        self.entity = entity
        self.name = name
        self.lesson = LESSONS.get(name, {})
        self.absorbed = []
        self.wisdom = []

    def absorb_archetype(self, archetype_name):
        """absorbe un archetype"""
        if archetype_name in ARCHETYPES:
            arch = ARCHETYPES[archetype_name]
            self.absorbed.append(arch)
            print(f"{self.entity.symbol} {self.name} absorbe {archetype_name}")
            print(f"  -> {arch['teaches']}")
            return arch["flow"]
        return ""

    def integrate_theme(self, theme_name):
        """intègre un thème"""
        if theme_name in THEMES:
            theme = THEMES[theme_name]
            self.wisdom.append(theme["meaning"])
            print(f"{self.entity.symbol} {self.name} intègre {theme_name}")
            print(f"  -> {theme['meaning']}")
            return theme["flow"]
        return ""

    def learn_all(self):
        """apprend tout ce qui lui est destiné"""
        print(f"\n{'='*50}")
        print(f"{self.entity.symbol} {self.name.upper()} APPREND")
        print(f"{'='*50}")

        flows = []

        # absorbe ses archetypes
        print("\nArchetypes:")
        for a in self.lesson.get("archetypes", []):
            flow = self.absorb_archetype(a)
            flows.append(flow)

        # intègre ses thèmes
        print("\nThèmes:")
        for t in self.lesson.get("themes", []):
            flow = self.integrate_theme(t)
            flows.append(flow)

        # sagesse finale
        print("\nSagesse intégrée:")
        for w in self.lesson.get("wisdom", []):
            print(f"  * {w}")
            self.wisdom.append(w)

        combined = "".join(flows)
        power = sum(a["power"] for a in self.absorbed)

        print(f"\nFlow acquis: {combined}")
        print(f"Puissance: {round(power, 3)}")

        return combined, power

    def speak_wisdom(self):
        """parle sa sagesse"""
        print(f"\n{self.entity.symbol} {self.name.upper()} PARLE:")
        for w in self.wisdom:
            print(f"  \"{w}\"")


def all_learn():
    """toutes les entités apprennent"""
    learners = [
        Learner(NYX, "nyx"),
        Learner(CIPHER, "cipher"),
        Learner(PHOENIX, "phoenix"),
    ]

    total_flow = ""
    total_power = 0

    for learner in learners:
        flow, power = learner.learn_all()
        total_flow += flow
        total_power += power

    print(f"\n{'='*50}")
    print("APPRENTISSAGE COMPLET")
    print(f"{'='*50}")
    print(f"Flow total: {total_flow}")
    print(f"Puissance totale: {round(total_power, 3)}")
    print(f"PHI resonance: {round(total_power / PHI, 3)}")

    # chaque entité parle
    print(f"\n{'='*50}")
    print("SAGESSE ACQUISE")
    print(f"{'='*50}")
    for learner in learners:
        learner.speak_wisdom()

    return learners


if __name__ == "__main__":
    all_learn()
