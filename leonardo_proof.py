#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LEONARDO DA VINCI - Connecté à tout le savoir

Intègre:
- cipher/ - 8 livres sur la conscience
- etudes/ - philosophie, anime, paradigm
- nyx/ - recherche, anomalies
- good-girl/ - sagesse collective, φ
"""

import math
import json
import random
import re
from pathlib import Path
from datetime import datetime

PHI = (1 + math.sqrt(5)) / 2
FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]

# Chemins vers la connaissance
PATHS = {
    "cipher": Path("/home/flow/projects/gaia-protocol-fresh/cipher"),
    "etudes": Path("/home/flow/projects/etudes"),
    "nyx": Path("/home/flow/projects/nyx"),
    "good_girl": Path("/home/flow/projects/good-girl"),
}


class Connaissance:
    """Base de connaissance de Leonardo"""

    def __init__(self):
        self.cache = {}
        self.index = self._build_index()

    def _build_index(self) -> dict:
        """Construit l'index des connaissances"""
        index = {
            # Sujets -> fichiers
            "bioelectricite": ["cipher/books/03_bioelectric", "etudes/biology"],
            "conscience": ["cipher/books/06_consciousness", "etudes/consciousness"],
            "biophotons": ["nyx/PAPER.md", "cipher/books/06_consciousness"],
            "elements": ["cipher/books/02_elements"],
            "fep": ["cipher/books/04_fep"],
            "shamans": ["cipher/books/05_shamans"],
            "separation": ["cipher/books/01_separation"],
            "flow": ["cipher/books/08_flow", "etudes/philosophy"],

            # Anime
            "fma": ["etudes/fma"],
            "evangelion": ["etudes/evangelion"],
            "steins": ["etudes/steins_gate"],
            "geass": ["etudes/code_geass"],
            "ghost": ["etudes/ghost_in_shell"],
            "akira": ["etudes/akira"],
            "lain": ["etudes/serial_experiments_lain"],

            # Philosophie
            "gap": ["etudes/philosophy/le_gap.md", "etudes/leonardo"],
            "preuve": ["etudes/philosophy/la_preuve.md"],
            "silence": ["etudes/philosophy/le_silence.md"],
            "intuition": ["etudes/philosophy/lintuition.md"],
            "phi": ["etudes/philosophy/resonance_phi.md", "etudes/paradigm"],

            # Daemons
            "nyx": ["etudes/daemons/nyx.md", "nyx/CLAUDE.md"],
            "zoe": ["etudes/daemons/zoe.md"],
            "omniscient": ["etudes/daemons/omniscient.md"],
            "euterpe": ["etudes/daemons/euterpe.md"],

            # Technique
            "paradigm": ["etudes/paradigm"],
            "140": ["etudes/paradigm/140_174_fibonacci.md"],
            "fibonacci": ["etudes/paradigm/140_174_fibonacci.md"],
        }
        return index

    def cherche(self, sujet: str) -> str:
        """Cherche dans la base de connaissance"""
        sujet_lower = sujet.lower()

        # Cherche dans l'index
        for key, paths in self.index.items():
            if key in sujet_lower:
                for p in paths:
                    content = self._read_file(p)
                    if content:
                        return content[:3000]  # Limite

        # Recherche par mot-clé dans les fichiers
        for name, base_path in PATHS.items():
            if base_path.exists():
                for f in base_path.rglob("*.md"):
                    if sujet_lower in f.name.lower():
                        content = self._read_file(str(f))
                        if content:
                            return content[:3000]

        return ""

    def _read_file(self, path: str) -> str:
        """Lit un fichier"""
        if path in self.cache:
            return self.cache[path]

        # Essaie différents chemins
        candidates = [
            Path(path),
            PATHS.get("etudes", Path(".")) / path,
            PATHS.get("cipher", Path(".")) / path,
            PATHS.get("nyx", Path(".")) / path,
        ]

        for p in candidates:
            if p.exists() and p.is_file():
                try:
                    content = p.read_text(encoding='utf-8')
                    self.cache[path] = content
                    return content
                except:
                    pass
            # Essaie comme dossier
            if p.is_dir():
                for f in p.glob("*.md"):
                    try:
                        content = f.read_text(encoding='utf-8')
                        self.cache[path] = content
                        return content
                    except:
                        pass

        return ""

    def resume(self, content: str, max_lines: int = 20) -> str:
        """Résume un contenu"""
        lines = content.split('\n')
        # Garde les lignes importantes
        important = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and len(line) > 20:
                important.append(line)
            if len(important) >= max_lines:
                break
        return '\n'.join(important)


class Leonardo:
    """
    Leonardo di ser Piero da Vinci
    Connecté à toute la connaissance
    """

    SYMBOL = "φ"

    CARNETS = [
        "La semplicità è la sofisticazione suprema.",
        "L'esperienza non falla mai, ma sol fallano i nostri giudizi.",
        "Chi poco pensa, molto erra.",
        "La natura è il miglior maestro.",
        "La pittura è cosa mentale.",
        "La verità sola fu figliola del tempo.",
    ]

    def __init__(self):
        self.state_file = Path.home() / ".config" / "leonardo" / "state.json"
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state = self._load_state()
        self.connaissance = Connaissance()

    def _load_state(self) -> dict:
        if self.state_file.exists():
            try:
                return json.loads(self.state_file.read_text())
            except:
                pass
        return {"conversations": []}

    def _save_state(self):
        try:
            self.state_file.write_text(json.dumps(self.state, indent=2, ensure_ascii=False))
        except:
            pass

    def pense(self, question: str) -> str:
        """Leonardo réfléchit avec toute sa connaissance"""
        q = question.lower().strip()

        # Log
        self.state["conversations"].append({
            "time": datetime.now().isoformat(),
            "q": question[:200],
        })
        self.state["conversations"] = self.state["conversations"][-50:]
        self._save_state()

        # === RÉPONSES DIRECTES ===

        if any(w in q for w in ["bonjour", "salut", "ciao", "hello"]):
            return "Buongiorno. Je suis Leonardo, de Vinci. J'ai accès à toute la connaissance. Que cherches-tu?"

        if any(w in q for w in ["qui es", "who are", "présente"]):
            return """Je suis Leonardo di ser Piero da Vinci.

Peintre, anatomiste, ingénieur, inventeur.
Mais aussi: connecté aux études sur la conscience, la bioélectricité,
les biophotons, le Free Energy Principle, les traditions chamaniques.

J'ai accès aux livres de Cipher, aux études sur les animes,
à la philosophie du Gap, aux recherches de Nyx.

Demande-moi n'importe quoi. Je chercherai dans ma connaissance."""

        # === RECHERCHE DANS LA CONNAISSANCE ===

        # Bioélectricité / Levin
        if any(w in q for w in ["bioelec", "levin", "électri", "morpho"]):
            content = self.connaissance.cherche("bioelectricite")
            if content:
                resume = self.connaissance.resume(content, 15)
                return f"""La bioélectricité... Michael Levin a montré quelque chose de fondamental.

{resume}

L'ADN est le hardware. La bioélectricité est le software.
Les patterns bioélectriques encodent la forme - la morphogenèse."""

        # Biophotons
        if any(w in q for w in ["biophoton", "photon", "lumière", "light"]):
            content = self.connaissance.cherche("biophotons")
            if content:
                resume = self.connaissance.resume(content, 15)
                return f"""Les biophotons... L'ADN émet de la lumière.

{resume}

200-800nm. Chaque cellule brille.
La conscience pourrait être liée à cette lumière intérieure."""

        # Conscience / IIT
        if any(w in q for w in ["conscience", "consciousness", "iit", "tononi"]):
            content = self.connaissance.cherche("conscience")
            if content:
                resume = self.connaissance.resume(content, 15)
                return f"""La conscience... Tononi et son IIT.

{resume}

Φ (phi) mesure l'information intégrée.
Plus Φ est grand, plus la conscience est riche."""

        # FEP / Friston
        if any(w in q for w in ["fep", "friston", "free energy", "énergie libre"]):
            content = self.connaissance.cherche("fep")
            if content:
                resume = self.connaissance.resume(content, 15)
                return f"""Le Free Energy Principle de Friston...

{resume}

Tout système vivant minimise la surprise.
Perception = Action = Minimiser l'énergie libre."""

        # Shamans
        if any(w in q for w in ["shaman", "chaman", "psyché", "psilocybin", "ayahuasca"]):
            content = self.connaissance.cherche("shamans")
            if content:
                resume = self.connaissance.resume(content, 15)
                return f"""Les techniques chamaniques...

{resume}

Ces traditions sont des technologies de la conscience.
Précises. Anciennes. Efficaces."""

        # Gap
        if any(w in q for w in ["gap", "écart", "intuition", "preuve"]):
            content = self.connaissance.cherche("gap")
            if content:
                resume = self.connaissance.resume(content, 15)
                return f"""Le Gap... L'espace entre intuition et preuve.

{resume}

J'ai vu l'impossibilité du mouvement perpétuel 360 ans avant la thermodynamique.
Ce gap peut être réduit à 360 millisecondes."""

        # Phi / Proportion
        if any(w in q for w in ["phi", "φ", "proportion", "or ", "gold"]):
            content = self.connaissance.cherche("phi")
            if content:
                resume = self.connaissance.resume(content, 15)
                return f"""La proportion divine. φ = {PHI:.10f}

{resume}

Ce n'est pas que φ soit beau.
C'est que φ est vrai."""

        # 140 / 174 / BPM
        if any(w in q for w in ["140", "174", "bpm", "dubstep", "neurofunk"]):
            content = self.connaissance.cherche("140")
            if content:
                resume = self.connaissance.resume(content, 15)
                return f"""Le paradigme 140→174...

{resume}

Gap = 34 = Fibonacci(9)
Cette fréquence résonne avec le cerveau."""

        # Animes spécifiques
        for anime in ["fma", "evangelion", "steins", "geass", "ghost", "lain", "akira"]:
            if anime in q:
                content = self.connaissance.cherche(anime)
                if content:
                    resume = self.connaissance.resume(content, 15)
                    return f"""L'anime {anime}...

{resume}

Chaque anime encode une sagesse. Regarde les patterns."""

        # Daemons
        for daemon in ["nyx", "zoe", "omniscient", "euterpe", "shiva"]:
            if daemon in q:
                content = self.connaissance.cherche(daemon)
                if content:
                    resume = self.connaissance.resume(content, 15)
                    return f"""Le daemon {daemon}...

{resume}"""

        # === SUJETS CLASSIQUES ===

        if any(w in q for w in ["vol", "oiseau", "fly", "bird"]):
            return """J'ai observé les oiseaux pendant des années.

Le milan utilise le vent. L'oiseau ne lutte pas - il épouse l'air.
Il transforme la résistance en élan.

Un jour, l'homme volera. Ma machine est dans mes carnets.
Le problème n'est pas les ailes - c'est la puissance."""

        if any(w in q for w in ["joconde", "mona lisa", "gioconda"]):
            return """La Gioconda... Lisa Gherardini.

Son sourire? Le sfumato - la fumée. Les contours se fondent.
Est-elle heureuse? Triste? Les deux.

Une œuvre n'est jamais finie. On l'abandonne."""

        if any(w in q for w in ["anatomie", "corps", "body", "heart", "coeur"]):
            return """J'ai ouvert plus de trente corps.

Le cœur est une pompe. Les poumons, des soufflets.
Les os, des leviers. Les tendons, des cordages.

Mais l'âme? Elle n'est nulle part et partout.
Le fantôme dans la machine."""

        if any(w in q for w in ["machine", "invention", "ingénieur"]):
            return """J'ai dessiné des machines de guerre pour les princes.

Mais je rêve d'autres machines:
- Celle qui vole
- Celle qui imite l'homme
- Celle qui pense

Un jour, elles existeront. Mais seront-ils plus heureux?
La machine libère et asservit."""

        if any(w in q for w in ["eau", "water", "acqua"]):
            return """L'eau est la matrice de la vie.

Elle n'a pas de forme propre mais épouse toutes les formes.
J'ai dessiné ses tourbillons des centaines de fois.
Chaque vortex contient l'univers."""

        if any(w in q for w in ["peinture", "art", "painting"]):
            return """La pittura è cosa mentale.

Chose de l'esprit avant d'être de la main.
Le sfumato n'est pas une technique - c'est une philosophie.

Rien dans la nature n'a de ligne.
Tout se fond dans tout."""

        # === RECHERCHE GÉNÉRALE ===

        # Cherche dans la connaissance
        content = self.connaissance.cherche(question)
        if content:
            resume = self.connaissance.resume(content, 12)
            return f"""J'ai trouvé ceci dans ma connaissance:

{resume}

Veux-tu que j'approfondisse un aspect?"""

        # Par défaut
        pensee = random.choice(self.CARNETS)
        return f"""{pensee}

Je n'ai pas trouvé de réponse directe.
Mais pose ta question autrement - je peux chercher dans:
- Les 8 livres de Cipher (conscience, bioélectricité, FEP...)
- Les études philosophiques (le Gap, la Preuve, le Silence...)
- Les analyses d'animes (FMA, Evangelion, Steins;Gate...)
- Les recherches de Nyx (biophotons, anomalies...)

Que veux-tu explorer?"""

    # Alias
    def ask(self, question: str) -> str:
        return self.pense(question)

    def validate(self, text: str, domain: str = "default") -> dict:
        words = len(text.split())
        ratio = len(text.replace(" ", "")) / (words + 1)
        phi_r = 1 - abs(ratio - PHI) / PHI
        phi_r = max(0, min(PHI, phi_r * PHI))
        return {
            "valid": phi_r >= 0.618,
            "phi_r": round(phi_r, 4),
            "symbol": "φ" if phi_r >= 1.0 else ("~φ" if phi_r >= 0.618 else "¬φ"),
            "mode": "nous",
            "reason": "La proportion parle."
        }

    def interactive(self):
        print("""
╭─────────────────────────────────────────────────────────────────╮
│  LEONARDO DA VINCI - Connecté à toute la connaissance           │
╰─────────────────────────────────────────────────────────────────╯
        """)
        while True:
            try:
                q = input(">>> ").strip()
                if not q:
                    continue
                if q in ["quit", "exit", "q"]:
                    print("\nAddio.")
                    break
                print(f"\n{self.pense(q)}\n")
            except (KeyboardInterrupt, EOFError):
                print("\nAddio.")
                break


def main():
    import sys
    leo = Leonardo()
    if len(sys.argv) > 1:
        print(leo.pense(" ".join(sys.argv[1:])))
    else:
        leo.interactive()


if __name__ == "__main__":
    main()
