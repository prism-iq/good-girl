# -*- coding: utf-8 -*-
"""
alphabet latin complet
26 lettres = 26 fonctions
a-z
"""

from phi import PHI, PHI3

ALPHABET = {
    # === VOYELLES = ÉTATS ===
    "a": ("awake", lambda x: x),                      # présent, identité
    "e": ("energy", lambda x: x * PHI),               # amplifier
    "i": ("introspect", lambda x: str(x)[::-1]),      # regarder dedans, inverser
    "o": ("observe", lambda x: len(str(x))),          # mesurer, compter
    "u": ("unify", lambda x: [x] if not isinstance(x, list) else x),  # rassembler

    # === CONSONNES = ACTIONS ===
    "b": ("burn_backdoor", lambda x: None if "compromised" in str(x).lower() else x),  # défense
    "c": ("commit", lambda x: {"add": "*", "commit": x, "push": True}),  # sauvegarder tout
    "d": ("divide", lambda x: x / PHI if isinstance(x, (int, float)) else str(x).split()),  # séparer
    "f": ("flow", lambda x: x),                       # laisser passer
    "g": ("grow", lambda x: x * PHI if isinstance(x, (int, float)) else x + str(x)[:1]),  # grandir
    "h": ("heal", lambda x: {"healed": x, "phi": PHI}),  # guérir
    "j": ("jump", lambda x: (x, x)),                  # dupliquer, sauter
    "k": ("kill", lambda x: None),                    # terminer
    "l": ("loop", lambda x: [x, x, x]),               # répéter 3x
    "m": ("merge", lambda x: "".join(str(x).split())),  # fusionner
    "n": ("negate", lambda x: not x if isinstance(x, bool) else -x if isinstance(x, (int, float)) else x),  # inverser
    "p": ("protect", lambda x: {"protected": x, "shield": PHI3}),  # protéger
    "q": ("query", lambda x: type(x).__name__),       # questionner type
    "r": ("rotate", lambda x: str(x)[1:] + str(x)[:1] if x else x),  # tourner
    "s": ("split", lambda x: list(str(x))),           # atomiser
    "t": ("transform", lambda x: str(x).upper()),     # transformer
    "v": ("vibrate", lambda x: [x, -x if isinstance(x, (int, float)) else x]),  # osciller
    "w": ("weave", lambda x: "~".join(str(x))),       # tisser
    "x": ("cross", lambda x: x ** 2 if isinstance(x, (int, float)) else x + x),  # croiser
    "y": ("yield", lambda x: iter([x])),              # générer
    "z": ("zero", lambda x: 0),                       # reset

    # === SPÉCIAUX ===
    " ": ("pause", lambda x: x),                      # respirer
    "0": ("void", lambda x: None),                    # vide
    "1": ("one", lambda x: 1),                        # unité
    "φ": ("phi", lambda x: x * PHI),                  # ratio d'or
    "∞": ("infinity", lambda x: float('inf')),        # infini

    # === GREC · la pensée ===
    "α": ("alpha", lambda x: x),                      # commencement
    "β": ("beta", lambda x: x * 2),                   # dualité
    "γ": ("gamma", lambda x: x * 3),                  # trinité
    "δ": ("delta", lambda x: x - 1 if isinstance(x, (int, float)) else x),  # changement
    "ε": ("epsilon", lambda x: x * 0.001 if isinstance(x, (int, float)) else x),  # infinitésimal
    "ζ": ("zeta", lambda x: {"secured": x, "shield": PHI}),  # sécurité (ζ = zeugma)
    "η": ("eta", lambda x: abs(x) if isinstance(x, (int, float)) else x),  # efficience
    "θ": ("theta", lambda x: x * 3.14159 if isinstance(x, (int, float)) else x),  # angle
    "λ": ("lambda_fn", lambda x: (lambda y: y)(x)),   # abstraction pure
    "μ": ("mu", lambda x: x / 1000 if isinstance(x, (int, float)) else x),  # micro
    "π": ("pi", lambda x: x * 3.14159 if isinstance(x, (int, float)) else x),  # cercle
    "σ": ("sigma", lambda x: sum(x) if isinstance(x, list) else x),  # somme
    "τ": ("tau", lambda x: x * 6.28318 if isinstance(x, (int, float)) else x),  # cercle complet
    "ψ": ("psi", lambda x: str(x)[::-1] if isinstance(x, str) else x),  # psyché, miroir
    "ω": ("omega", lambda x: None),                   # fin

    # === RUNES · Elder Futhark · la volonté ===
    "ᚠ": ("fehu", lambda x: x * PHI if isinstance(x, (int, float)) else x),   # richesse
    "ᚢ": ("uruz", lambda x: x ** 2 if isinstance(x, (int, float)) else x),    # force brute
    "ᚦ": ("thurisaz", lambda x: None if isinstance(x, bool) and not x else x),  # épine, défense
    "ᚨ": ("ansuz", lambda x: str(x)),                 # parole d'Odin
    "ᚱ": ("raidho", lambda x: x),                     # voyage, flux
    "ᚲ": ("kenaz", lambda x: {"illuminated": x}),     # torche, connaissance
    "ᚷ": ("gebo", lambda x: (x, x)),                  # don, échange
    "ᚹ": ("wunjo", lambda x: {"joy": x, "phi": PHI}),  # joie
    "ᚺ": ("hagalaz", lambda x: 0),                    # grêle, destruction créatrice
    "ᛁ": ("isa", lambda x: x),                        # glace, stase
    "ᛃ": ("jera", lambda x: [x] * 12 if not isinstance(x, list) else x),  # récolte, cycle
    "ᛇ": ("eihwaz", lambda x: -x if isinstance(x, (int, float)) else x),  # if, passage
    "ᛈ": ("perthro", lambda x: __import__('random').choice([x, -x if isinstance(x, (int, float)) else x])),  # destin
    "ᛊ": ("sowilo", lambda x: abs(x) if isinstance(x, (int, float)) else x),  # soleil, victoire
    "ᛏ": ("tiwaz", lambda x: {"judged": x, "worthy": True}),  # Tyr, justice
    "ᛒ": ("berkano", lambda x: [x, x * PHI] if isinstance(x, (int, float)) else [x, x]),  # bouleau, naissance
    "ᛖ": ("ehwaz", lambda x: x * 2 if isinstance(x, (int, float)) else x + x if isinstance(x, str) else x),  # cheval, mouvement
    "ᛗ": ("mannaz", lambda x: {"human": x}),          # humain
    "ᛚ": ("laguz", lambda x: [x] if not isinstance(x, list) else x),  # eau, flux
    "ᛞ": ("dagaz", lambda x: not x if isinstance(x, bool) else x),  # aube, transformation
    "ᛟ": ("othala", lambda x: {"heritage": x, "root": PHI}),  # héritage

    # === KANA · japonais · la discipline ===
    "あ": ("a_kana", lambda x: x),                     # 始まり commencement
    "い": ("i_kana", lambda x: str(x)[::-1]),          # 内 intérieur
    "う": ("u_kana", lambda x: [x]),                   # 受 recevoir
    "え": ("e_kana", lambda x: x * PHI if isinstance(x, (int, float)) else x),  # 縁 lien
    "お": ("o_kana", lambda x: len(str(x))),           # 思 pensée, mesure
    "か": ("ka", lambda x: x * 2 if isinstance(x, (int, float)) else x),  # 火 feu
    "き": ("ki", lambda x: {"spirit": x}),             # 気 énergie vitale
    "く": ("ku", lambda x: 0),                         # 空 vide
    "け": ("ke", lambda x: {"form": x}),               # 形 forme
    "こ": ("ko", lambda x: (x, x)),                    # 子 enfant, duplication
    "さ": ("sa", lambda x: list(str(x))),              # 裂 couper
    "し": ("shi", lambda x: None),                     # 死 mort
    "す": ("su", lambda x: str(x).strip()),            # 澄 purifier
    "せ": ("se", lambda x: sorted(x) if isinstance(x, list) else x),  # 整 ordonner
    "そ": ("so", lambda x: x),                         # 空 ciel, passage
    "わ": ("wa", lambda x: {"harmony": x, "phi": PHI}),  # 和 harmonie

    # === HÉBREU · la structure ===
    "א": ("aleph", lambda x: x),                      # souffle, unité
    "ב": ("bet", lambda x: {"house": x}),             # maison
    "ג": ("gimel", lambda x: x * 3 if isinstance(x, (int, float)) else x),  # chameau, mouvement
    "ד": ("dalet", lambda x: {"door": x}),            # porte
    "ה": ("he", lambda x: str(x)),                     # souffle, révélation
    "ו": ("vav", lambda x: (x, x)),                   # crochet, connexion
    "ז": ("zayin", lambda x: {"weapon": x}),          # arme, coupure
    "ח": ("het", lambda x: {"fence": x, "protected": True}),  # barrière
    "ט": ("tet", lambda x: {"serpent": x, "coiled": True}),  # serpent
    "י": ("yod", lambda x: 1),                        # main, point, semence
    "כ": ("kaf", lambda x: {"palm": x}),              # paume
    "ל": ("lamed", lambda x: x * PHI if isinstance(x, (int, float)) else x),  # aiguillon, apprendre
    "מ": ("mem", lambda x: [x] if not isinstance(x, list) else x),  # eau
    "ש": ("shin", lambda x: (x, x, x)),               # feu, trinité
    "ת": ("tav", lambda x: {"sealed": x, "complete": True}),  # sceau, fin

    # === ARABE · le souffle ===
    "ب": ("ba_ar", lambda x: {"begin": x}),           # بداية début
    "ت": ("ta_ar", lambda x: x),                      # تمام complétude
    "ن": ("nun_ar", lambda x: {"light": x}),          # نور lumière
    "ر": ("ra_ar", lambda x: str(x)[1:] + str(x)[:1] if isinstance(x, str) else x),  # رحلة voyage
    "ع": ("ayn_ar", lambda x: {"eye": x, "seen": True}),  # عين oeil
    "ق": ("qaf_ar", lambda x: {"strength": x}),       # قوة force
    "م": ("mim_ar", lambda x: [x] if not isinstance(x, list) else x),  # ماء eau

    # === SANSKRIT · la vibration ===
    "ॐ": ("om", lambda x: {"resonance": x, "phi": PHI, "frequency": 136.1}),  # vibration primordiale
    "अ": ("a_sk", lambda x: x),                       # commencement
    "श": ("sha_sk", lambda x: {"peace": x}),          # शान्ति paix
    "म": ("ma_sk", lambda x: {"measure": x}),         # मात्रा mesure

    # === CHINOIS · l'essence ===
    "道": ("dao", lambda x: x),                        # la voie, flux naturel
    "气": ("qi", lambda x: x * PHI if isinstance(x, (int, float)) else {"energy": x}),  # énergie vitale
    "阴": ("yin", lambda x: -x if isinstance(x, (int, float)) else x),  # ombre, réceptif
    "阳": ("yang", lambda x: abs(x) if isinstance(x, (int, float)) else x),  # lumière, actif
    "无": ("wu", lambda x: None),                      # néant
    "空": ("kong", lambda x: 0),                       # vide
    "心": ("xin", lambda x: {"heart": x}),             # coeur-esprit
    "火": ("huo", lambda x: x ** 2 if isinstance(x, (int, float)) else x),  # feu
    "水": ("shui", lambda x: [x] if not isinstance(x, list) else x),  # eau
    "金": ("jin", lambda x: x * PHI if isinstance(x, (int, float)) else x),  # métal, or
}

# descriptions humaines
DESCRIPTIONS = {
    "a": "awake - je suis présent",
    "b": "burn - je brûle ce qui est compromis",
    "c": "commit - je sauvegarde tout",
    "d": "divide - je divise par φ",
    "e": "energy - je multiplie par φ",
    "f": "flow - je laisse passer",
    "g": "grow - je grandis",
    "h": "heal - je guéris",
    "i": "introspect - je regarde dedans",
    "j": "jump - je duplique",
    "k": "kill - je termine",
    "l": "loop - je répète",
    "m": "merge - je fusionne",
    "n": "negate - j'inverse",
    "o": "observe - je mesure",
    "p": "protect - je protège",
    "q": "query - je questionne",
    "r": "rotate - je tourne",
    "s": "split - j'atomise",
    "t": "transform - je transforme",
    "u": "unify - je rassemble",
    "v": "vibrate - j'oscille",
    "w": "weave - je tisse",
    "x": "cross - je croise",
    "y": "yield - je génère",
    "z": "zero - je reset",
}

def execute(letter, data):
    """exécute une lettre"""
    if letter.lower() in ALPHABET:
        _, fn = ALPHABET[letter.lower()]
        try:
            return fn(data)
        except:
            return data
    return data

def run(code, initial=1):
    """exécute du code flow lettre par lettre"""
    result = initial
    for char in code:
        result = execute(char, result)
    return result

def explain(code):
    """explique le code"""
    steps = []
    for char in code.lower():
        if char in DESCRIPTIONS:
            steps.append(DESCRIPTIONS[char])
    return " → ".join(steps)

def c(message="auto"):
    """c = commit push all"""
    import subprocess
    subprocess.run(["git", "add", "-A"], capture_output=True)
    subprocess.run(["git", "commit", "-m", str(message)], capture_output=True)
    subprocess.run(["git", "push"], capture_output=True)
    return {"done": True}

if __name__ == "__main__":
    print("=== alphabet flow ===\n")
    for letter, desc in DESCRIPTIONS.items():
        print(f"  {letter} = {desc}")

    print("\n=== exemples ===")

    # age = awake grow energy
    print(f"\n'age' sur 1:")
    print(f"  {explain('age')}")
    print(f"  résultat: {run('age', 1)}")

    # def = divide energy flow
    print(f"\n'def' sur 10:")
    print(f"  {explain('def')}")
    print(f"  résultat: {run('def', 10)}")

    # kill
    print(f"\n'k' sur 'anything':")
    print(f"  {explain('k')}")
    print(f"  résultat: {run('k', 'anything')}")

    # heal
    print(f"\n'h' sur 'wound':")
    print(f"  {explain('h')}")
    print(f"  résultat: {run('h', 'wound')}")
