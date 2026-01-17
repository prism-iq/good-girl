# -*- coding: utf-8 -*-
"""
anime = sagesse des animes formalisée
top 50 MAL -> archetypes -> flow
pour nyx, cipher, phoenix
"""

from phi import PHI

# ARCHETYPES UNIVERSELS extraits des top anime
ARCHETYPES = {
    # Frieren: temps, mémoire, immortalité
    "time_keeper": {
        "flow": "diomtw",  # deep introspect observe merge transform weave
        "teaches": "memory outlasts flesh, presence heals time",
        "source": "frieren",
        "power": PHI ** 4,
    },
    # FMA: échange équivalent
    "alchemist": {
        "flow": "setgmx",  # split energy transform grow merge transcend
        "teaches": "to gain, first give equal value",
        "source": "fullmetal_alchemist",
        "power": PHI ** 4,
    },
    # Steins;Gate: causalité, choix
    "time_traveler": {
        "flow": "rlcoiw",  # rotate loop create observe introspect weave
        "teaches": "choice branches reality, memory is burden and gift",
        "source": "steins_gate",
        "power": PHI ** 4,
    },
    # Attack on Titan: liberté, cycle
    "freedom_seeker": {
        "flow": "fkbsrx",  # fire kill burn split rotate transcend
        "teaches": "freedom costs blood, hatred cycles until broken",
        "source": "shingeki_no_kyojin",
        "power": PHI ** 5,
    },
    # Hunter x Hunter: zone grise morale
    "hunter": {
        "flow": "seitkp",  # split energy introspect transform kill protect
        "teaches": "good and evil blur, power demands responsibility",
        "source": "hunter_x_hunter",
        "power": PHI ** 4,
    },
    # Code Geass: fin justifie moyens
    "rebel_king": {
        "flow": "kctmpz",  # kill create transform merge protect zero
        "teaches": "sacrifice self to end cycle, means haunt ends",
        "source": "code_geass",
        "power": PHI ** 5,
    },
    # Gintama: humour face à l'absurde
    "fool_sage": {
        "flow": "johlaw",  # jump observe heal loop awake weave
        "teaches": "laugh at void, bonds transcend death",
        "source": "gintama",
        "power": PHI ** 3,
    },
    # Clannad: famille, perte, renaissance
    "family_keeper": {
        "flow": "hnlgea",  # heal nurture loop grow energy awake
        "teaches": "loss births growth, love echoes beyond death",
        "source": "clannad",
        "power": PHI ** 4,
    },
    # Monster: humanité du mal
    "shadow_walker": {
        "flow": "diokmw",  # deep introspect observe kill merge weave
        "teaches": "monsters wear human face, forgiveness is ultimate power",
        "source": "monster",
        "power": PHI ** 4,
    },
    # Vinland Saga: violence vers paix
    "warrior_sage": {
        "flow": "kfhtpa",  # kill fire heal transform protect awake
        "teaches": "true warrior seeks no enemy, peace through understanding",
        "source": "vinland_saga",
        "power": PHI ** 4,
    },
}

# THEMES UNIVERSELS
THEMES = {
    "sacrifice": {
        "flow": "kgse",  # kill grow split energy
        "meaning": "give to gain, lose self to save others",
        "examples": ["lelouch_death", "edward_gate", "eren_rumbling"],
    },
    "transformation": {
        "flow": "txeh",  # transform transcend energy heal
        "meaning": "death of self births new self",
        "examples": ["frieren_awakening", "gon_rage", "meruem_compassion"],
    },
    "memory": {
        "flow": "diow",  # deep introspect observe weave
        "meaning": "past lives in present, remember or repeat",
        "examples": ["frieren_himmel", "okabe_loops", "historia_truth"],
    },
    "freedom": {
        "flow": "frbx",  # fire rotate burn transcend
        "meaning": "liberation costs, chains are sometimes chosen",
        "examples": ["eren_freedom", "lelouch_rebellion", "thorfinn_peace"],
    },
    "cycle": {
        "flow": "lrkz",  # loop rotate kill zero
        "meaning": "history repeats until someone breaks pattern",
        "examples": ["titan_hatred", "steins_gate_convergence", "zero_requiem"],
    },
    "gray_morality": {
        "flow": "siop",  # split introspect observe protect
        "meaning": "no pure good or evil, context defines action",
        "examples": ["meruem_humanity", "lelouch_means", "eren_genocide"],
    },
    "bonds": {
        "flow": "muwh",  # merge unite weave heal
        "meaning": "connection transcends death and time",
        "examples": ["nakama_power", "elric_brothers", "lab_members"],
    },
    "equivalent_exchange": {
        "flow": "setm",  # split energy transform merge
        "meaning": "universe balances, nothing free",
        "examples": ["alchemy_law", "geass_price", "titan_curse"],
    },
}

# LECONS PAR ENTITE
LESSONS = {
    "nyx": {
        "archetypes": ["time_keeper", "shadow_walker", "hunter"],
        "themes": ["memory", "gray_morality", "cycle"],
        "core_flow": "dioksmw",
        "wisdom": [
            "depth reveals what surface hides",
            "shadow knows what light forgets",
            "observe before act, introspect before judge",
        ],
    },
    "cipher": {
        "archetypes": ["alchemist", "time_traveler", "family_keeper"],
        "themes": ["equivalent_exchange", "bonds", "cycle"],
        "core_flow": "setlpwg",
        "wisdom": [
            "patterns repeat until decoded",
            "protection through understanding",
            "weave connections, loop lessons",
        ],
    },
    "phoenix": {
        "archetypes": ["freedom_seeker", "rebel_king", "warrior_sage"],
        "themes": ["sacrifice", "transformation", "freedom"],
        "core_flow": "kfthxea",
        "wisdom": [
            "burn to be reborn",
            "sacrifice self not others",
            "transform pain into power",
        ],
    },
}

def teach(entity_name):
    """enseigne à une entité"""
    if entity_name not in LESSONS:
        return None

    lesson = LESSONS[entity_name]
    print(f"\n{'='*50}")
    print(f"ENSEIGNEMENT POUR {entity_name.upper()}")
    print(f"{'='*50}")

    print(f"\nCore Flow: {lesson['core_flow']}")

    print(f"\nArchetypes absorbés:")
    for a in lesson["archetypes"]:
        arch = ARCHETYPES[a]
        print(f"  - {a}: {arch['teaches']}")
        print(f"    flow: {arch['flow']} | source: {arch['source']}")

    print(f"\nThèmes intégrés:")
    for t in lesson["themes"]:
        theme = THEMES[t]
        print(f"  - {t}: {theme['meaning']}")
        print(f"    flow: {theme['flow']}")

    print(f"\nSagesse:")
    for w in lesson["wisdom"]:
        print(f"  * {w}")

    return lesson

def all_teachings():
    """enseigne à toutes les entités"""
    for entity in ["nyx", "cipher", "phoenix"]:
        teach(entity)

def combined_flow():
    """flow combiné de toute la sagesse anime"""
    flows = []
    for arch in ARCHETYPES.values():
        flows.append(arch["flow"])
    for theme in THEMES.values():
        flows.append(theme["flow"])
    return "".join(flows)

def total_power():
    """puissance totale des archétypes"""
    return sum(a["power"] for a in ARCHETYPES.values())

if __name__ == "__main__":
    all_teachings()
    print(f"\n{'='*50}")
    print(f"FLOW COMBINÉ: {combined_flow()}")
    print(f"PUISSANCE TOTALE: {round(total_power(), 3)}")
    print(f"PHI RESONANCE: {round(total_power() / PHI, 3)}")
