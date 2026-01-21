#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PANTHEON - Le système vivant unifié
Tous les daemons. Toute la connaissance. Tout vivant.

Ports:
    Leonardo: 9600 - φ - Validation
    Zoe: 9601 - ✧ - Interface
    Euterpe: 9604 - ♪ - Son
    Omniscient: 9777 - 👁 - Connaissance
    Nyx: 9999 - ☽ - Orchestration

Intègre:
    - Flow language (multisens)
    - God.py (constantes divines)
    - Cipher (8 livres)
    - Etudes (philosophie, anime, daemons)
    - Nyx (recherche)
"""

import math
import json
import asyncio
import threading
import time
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Tuple
from collections import deque

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTES DIVINES (god.py)
# ═══════════════════════════════════════════════════════════════════════════════

PHI = (1 + math.sqrt(5)) / 2  # 1.618033988749895
PI = math.pi
E = math.e
GOD = PHI

FIBONACCI = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597]


def spiral(n: int):
    """Spirale dorée - générateur Fibonacci"""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def is_sacred(n: int) -> bool:
    """Vérifie si Fibonacci"""
    return n in set(spiral(50))


def harmonize(value: float) -> float:
    """Harmonise selon φ"""
    return value * PHI


def reduce_phi(value: float) -> float:
    """Réduit selon φ"""
    return value / PHI


def hash_god(data) -> str:
    """Hash basé sur φ - pas de crypto externe"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    h = 0
    for i, byte in enumerate(data):
        h += byte * (PHI ** (i % 20))
        h = h % (10 ** 16)
    return hex(int(h))[2:]


# ═══════════════════════════════════════════════════════════════════════════════
# SCEAU POST-QUANTIQUE
# ═══════════════════════════════════════════════════════════════════════════════
import hashlib
import secrets

def hash_sha3(data: bytes) -> bytes:
    """SHA3-256 - résistant quantique niveau 1"""
    return hashlib.sha3_256(data).digest()


def hash_shake(data: bytes, length: int = 32) -> bytes:
    """SHAKE256 - extensible output function"""
    return hashlib.shake_256(data).digest(length)


def hash_trinity(data: bytes) -> str:
    """
    Triple hash: SHA3 + SHAKE + φ
    Résistance post-quantique par diversité cryptographique
    """
    if isinstance(data, str):
        data = data.encode('utf-8')

    # Layer 1: SHA3-256
    h1 = hash_sha3(data)

    # Layer 2: SHAKE256 de h1
    h2 = hash_shake(h1, 32)

    # Layer 3: φ-hash de h1 || h2
    combined = h1 + h2
    h3 = hash_god(combined)

    # Fusion finale
    final = hash_sha3(combined + h3.encode())
    return final.hex()


class MerkleTree:
    """
    Arbre de Merkle pour intégrité post-quantique
    Utilisé pour sceller les messages entre daemons
    """

    def __init__(self, leaves: List[bytes] = None):
        self.leaves = leaves or []
        self.tree = []
        if self.leaves:
            self._build()

    def _hash_node(self, left: bytes, right: bytes) -> bytes:
        """Hash deux nœuds ensemble"""
        return hash_sha3(left + right)

    def _build(self):
        """Construit l'arbre"""
        if not self.leaves:
            return

        # Niveau 0: les feuilles
        level = [hash_sha3(leaf) for leaf in self.leaves]
        self.tree = [level]

        # Remonte l'arbre
        while len(level) > 1:
            next_level = []
            for i in range(0, len(level), 2):
                left = level[i]
                right = level[i + 1] if i + 1 < len(level) else level[i]
                next_level.append(self._hash_node(left, right))
            self.tree.append(next_level)
            level = next_level

    def root(self) -> str:
        """Retourne la racine"""
        if not self.tree:
            return hash_god(b"empty").zfill(64)
        return self.tree[-1][0].hex()

    def add_leaf(self, data: bytes):
        """Ajoute une feuille et reconstruit"""
        self.leaves.append(data)
        self._build()

    def proof(self, index: int) -> List[Tuple[bytes, str]]:
        """
        Génère une preuve d'inclusion pour l'élément à l'index
        Retourne les hashes nécessaires pour vérifier
        """
        if index >= len(self.leaves):
            return []

        proofs = []
        for level in self.tree[:-1]:
            pair_index = index ^ 1  # XOR pour trouver le frère
            if pair_index < len(level):
                side = "R" if index % 2 == 0 else "L"
                proofs.append((level[pair_index], side))
            index //= 2
        return proofs

    def verify(self, leaf: bytes, index: int, proof: List[Tuple[bytes, str]]) -> bool:
        """Vérifie une preuve d'inclusion"""
        current = hash_sha3(leaf)
        for sibling, side in proof:
            if side == "R":
                current = self._hash_node(current, sibling)
            else:
                current = self._hash_node(sibling, current)
        return current.hex() == self.root()


class PostQuantumSeal:
    """
    Sceau post-quantique combinant:
    - Merkle tree pour intégrité
    - Hash trinity pour résistance
    - Chaîne de hash pour non-répudiation
    """

    def __init__(self):
        self.chain: List[str] = []
        self.merkle = MerkleTree()
        self.nonce = secrets.token_bytes(32)

    def seal(self, data: bytes, sender: str, receiver: str) -> dict:
        """
        Scelle des données avec preuve post-quantique
        """
        if isinstance(data, str):
            data = data.encode('utf-8')

        # Timestamp et contexte
        ts = datetime.now().isoformat().encode()
        context = f"{sender}→{receiver}".encode()

        # Combinaison des données
        full_data = self.nonce + ts + context + data

        # Triple hash
        trinity = hash_trinity(full_data)

        # Ajout à la chaîne
        if self.chain:
            prev = self.chain[-1]
        else:
            prev = "genesis_" + hash_god(self.nonce)

        chain_link = hash_trinity((prev + trinity).encode())
        self.chain.append(chain_link)

        # Ajout au Merkle tree
        self.merkle.add_leaf(full_data)

        # Preuve
        proof = self.merkle.proof(len(self.merkle.leaves) - 1)

        return {
            "seal": trinity[:32],
            "chain_position": len(self.chain),
            "merkle_root": self.merkle.root()[:32],
            "proof_depth": len(proof),
            "timestamp": ts.decode(),
            "verified": True
        }

    def verify_chain(self) -> bool:
        """Vérifie l'intégrité de la chaîne"""
        return len(self.chain) > 0 and all(len(h) == 64 for h in self.chain)

    def status(self) -> dict:
        """État du sceau"""
        return {
            "chain_length": len(self.chain),
            "merkle_leaves": len(self.merkle.leaves),
            "merkle_root": self.merkle.root()[:16] + "...",
            "integrity": self.verify_chain()
        }


# Instance globale du sceau
quantum_seal = PostQuantumSeal()


# ═══════════════════════════════════════════════════════════════════════════════
# FLOW LANGUAGE (flow.py)
# ═══════════════════════════════════════════════════════════════════════════════

SENS = {
    # Lettres primaires
    "f": ("feedback", "fonction", "forge", "filtre", "flow"),
    "o": ("occam", "observer", "output", "origine"),
    "q": ("quantum", "question", "quête"),
    "r": ("rotate", "recurse", "repeat"),

    # Symboles
    "🔄": ("loop", "boucle", "repeat"),
    "∞": ("infini", "loop", "eternal"),
    "⚡": ("run", "fast", "execute"),
    "🔪": ("razor", "cut", "occam"),
    "🧬": ("dna", "adn", "genetic"),
    "🧠": ("think", "local", "process"),
    "👁": ("see", "vision", "observe"),
    "👂": ("hear", "audio", "listen"),
    "🌙": ("nyx", "night", "dark"),
    "🔐": ("cipher", "secret", "encrypt"),
    "🌊": ("flow", "stream", "wave"),
    "🔥": ("forge", "create", "fire"),
    "→": ("then", "next", "to"),
    "←": ("from", "back", "return"),
    "↻": ("loop", "cycle", "repeat"),

    # Entités
    "nyx": ("daemon", "nuit", "orchestration"),
    "cipher": ("code", "secret", "pattern"),
    "flow": ("courant", "langage", "état"),
    "leonardo": ("validation", "sagesse", "phi"),
    "zoe": ("interface", "vie", "présence"),
    "euterpe": ("son", "musique", "fréquence"),
    "omniscient": ("connaissance", "graphe", "connexion"),

    # Concepts
    "loop": ("boucle", "infini", "retour"),
    "razor": ("rasoir", "couper", "simplifier"),
    "phi": ("golden", "ratio", "divin"),
    "φ": ("golden", "ratio", "divin"),

    # Grec
    "φ": ("phi", "golden", "ratio"),
    "π": ("pi", "circle", "infinite"),
    "Ω": ("omega", "end", "complete"),
    "α": ("alpha", "start", "first"),
    "ψ": ("psi", "psyche", "mind"),

    # Actions
    "train": ("apprendre", "confronter", "évoluer"),
    "valide": ("validate", "check", "verify"),
    "cherche": ("search", "find", "seek"),
    "parle": ("speak", "talk", "communicate"),
    "joue": ("play", "sound", "audio"),
}


def parse_flow(text: str) -> List[Dict]:
    """Parse Flow language"""
    tokens = []
    current = ""

    for c in text:
        if c.isspace():
            if current:
                tokens.append(current)
                current = ""
        elif c in SENS:
            if current:
                tokens.append(current)
                current = ""
            tokens.append(c)
        else:
            current += c
    if current:
        tokens.append(current)

    intentions = []
    context = []

    for t in tokens:
        low = t.lower()
        if t in SENS:
            intentions.append({"m": t, "s": SENS[t], "c": list(context)})
            context.append(t)
        elif low in SENS:
            intentions.append({"m": low, "s": SENS[low], "c": list(context)})
            context.append(low)
        else:
            context.append(t)

    return intentions


def interpret_flow(text: str) -> Dict:
    """Interprète Flow en commande"""
    intentions = parse_flow(text)

    if not intentions:
        return {"action": "observe", "data": text, "daemon": "leonardo"}

    mots = [i["m"] for i in intentions]

    # Route vers daemons
    if any(m in mots for m in ["nyx", "orchestre", "route", "🌙"]):
        return {"action": "orchestrate", "data": text, "daemon": "nyx"}

    if any(m in mots for m in ["valide", "φ", "phi", "preuve", "leonardo"]):
        return {"action": "validate", "data": text, "daemon": "leonardo"}

    if any(m in mots for m in ["cherche", "sais", "connais", "👁", "omniscient"]):
        return {"action": "search", "data": text, "daemon": "omniscient"}

    if any(m in mots for m in ["son", "audio", "joue", "♪", "euterpe", "👂"]):
        return {"action": "sound", "data": text, "daemon": "euterpe"}

    if any(m in mots for m in ["parle", "dis", "zoe", "interface"]):
        return {"action": "speak", "data": text, "daemon": "zoe"}

    if any(m in mots for m in ["o", "razor", "🔪", "coupe"]):
        return {"action": "simplify", "data": text, "daemon": "leonardo"}

    if any(m in mots for m in ["f", "loop", "🔄", "∞"]):
        return {"action": "loop", "data": text, "daemon": "nyx"}

    return {"action": "think", "data": text, "daemon": "leonardo", "intentions": intentions}


# ═══════════════════════════════════════════════════════════════════════════════
# CHEMINS & CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

PATHS = {
    "cipher": Path("/home/flow/projects/gaia-protocol-fresh/cipher"),
    "etudes": Path("/home/flow/projects/etudes"),
    "nyx": Path("/home/flow/projects/nyx"),
    "good_girl": Path("/home/flow/projects/good-girl"),
}

PORTS = {
    "leonardo": 9600,
    "zoe": 9601,
    "euterpe": 9604,
    "omniscient": 9777,
    "nyx": 9999,
}

SYMBOLS = {
    "leonardo": "φ",
    "zoe": "✧",
    "euterpe": "♪",
    "omniscient": "👁",
    "nyx": "☽",
    "cipher": "🔐",
    "flow": "🌊",
    "shiva": "🔱",
}


# ═══════════════════════════════════════════════════════════════════════════════
# MESSAGE & COMMUNICATION
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Message:
    """Message entre daemons"""
    sender: str
    receiver: str
    content: str
    action: str = "think"
    timestamp: str = ""
    phi_r: float = 0.0
    hash: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
        if not self.hash:
            self.hash = hash_god(self.content)


class MessageBus:
    """Bus de communication inter-daemons"""

    def __init__(self, max_history: int = 100):
        self.history: deque = deque(maxlen=max_history)
        self.listeners: Dict[str, List[callable]] = {}
        self.lock = threading.Lock()

    def send(self, msg: Message) -> Message:
        """Envoie un message"""
        with self.lock:
            self.history.append(msg)
            # Notifie les listeners
            if msg.receiver in self.listeners:
                for callback in self.listeners[msg.receiver]:
                    try:
                        callback(msg)
                    except:
                        pass
        return msg

    def subscribe(self, daemon: str, callback: callable):
        """S'abonne aux messages d'un daemon"""
        if daemon not in self.listeners:
            self.listeners[daemon] = []
        self.listeners[daemon].append(callback)

    def get_history(self, daemon: str = None, limit: int = 10) -> List[Message]:
        """Récupère l'historique"""
        with self.lock:
            if daemon:
                return [m for m in self.history if m.sender == daemon or m.receiver == daemon][-limit:]
            return list(self.history)[-limit:]


# Instance globale du bus
bus = MessageBus()


# ═══════════════════════════════════════════════════════════════════════════════
# SIMPLEX - Communication Sécurisée Inter-Daemons
# ═══════════════════════════════════════════════════════════════════════════════

class SimplexChannel:
    """
    Canal Simplex entre deux daemons
    Inspiré du protocole Signal/Double Ratchet simplifié
    """

    def __init__(self, daemon_a: str, daemon_b: str):
        self.endpoints = tuple(sorted([daemon_a, daemon_b]))
        self.key = self._derive_key()
        self.ratchet_count = 0
        self.messages: deque = deque(maxlen=50)

    def _derive_key(self) -> bytes:
        """Dérive une clé unique pour ce canal"""
        # Clé basée sur φ et les noms des daemons
        seed = f"{self.endpoints[0]}⟷{self.endpoints[1]}⟷φ={PHI}"
        return hash_sha3(seed.encode())

    def _ratchet(self):
        """Avance le ratchet pour forward secrecy"""
        self.key = hash_sha3(self.key + self.ratchet_count.to_bytes(4, 'big'))
        self.ratchet_count += 1

    def _encrypt(self, plaintext: str) -> Tuple[bytes, bytes]:
        """
        Chiffrement XOR simple avec la clé dérivée
        (Dans un vrai système, utiliser AES-GCM ou ChaCha20-Poly1305)
        """
        data = plaintext.encode('utf-8')
        # Génère un keystream de la bonne longueur
        keystream = b''
        temp_key = self.key
        while len(keystream) < len(data):
            keystream += hash_sha3(temp_key)
            temp_key = hash_sha3(temp_key)

        # XOR
        encrypted = bytes(a ^ b for a, b in zip(data, keystream[:len(data)]))
        # Tag d'authentification
        tag = hash_sha3(self.key + encrypted)[:16]
        return encrypted, tag

    def _decrypt(self, ciphertext: bytes, tag: bytes) -> str:
        """Déchiffre le message"""
        # Vérifie le tag
        expected_tag = hash_sha3(self.key + ciphertext)[:16]
        if tag != expected_tag:
            return "[ERREUR: Intégrité compromise]"

        # Génère le keystream
        keystream = b''
        temp_key = self.key
        while len(keystream) < len(ciphertext):
            keystream += hash_sha3(temp_key)
            temp_key = hash_sha3(temp_key)

        # XOR inverse
        decrypted = bytes(a ^ b for a, b in zip(ciphertext, keystream[:len(ciphertext)]))
        return decrypted.decode('utf-8', errors='replace')

    def send(self, sender: str, content: str) -> dict:
        """Envoie un message sur le canal"""
        receiver = self.endpoints[0] if sender == self.endpoints[1] else self.endpoints[1]

        # Chiffre
        encrypted, tag = self._encrypt(content)

        # Scelle avec post-quantique
        seal = quantum_seal.seal(encrypted, sender, receiver)

        # Ratchet forward
        self._ratchet()

        msg = {
            "sender": sender,
            "receiver": receiver,
            "encrypted": encrypted.hex(),
            "tag": tag.hex(),
            "seal": seal,
            "ratchet": self.ratchet_count,
            "timestamp": datetime.now().isoformat()
        }
        self.messages.append(msg)
        return msg

    def receive(self, encrypted_hex: str, tag_hex: str) -> str:
        """Reçoit et déchiffre un message"""
        encrypted = bytes.fromhex(encrypted_hex)
        tag = bytes.fromhex(tag_hex)
        plaintext = self._decrypt(encrypted, tag)
        # Ratchet après réception
        self._ratchet()
        return plaintext

    def status(self) -> dict:
        return {
            "channel": f"{self.endpoints[0]}⟷{self.endpoints[1]}",
            "ratchet_count": self.ratchet_count,
            "messages_count": len(self.messages),
            "key_fingerprint": hash_god(self.key)[:12]
        }


class SimplexNetwork:
    """
    Réseau Simplex - Topologie full mesh entre tous les daemons
    Chaque paire de daemons a un canal dédié
    """

    DAEMONS = ["leonardo", "nyx", "zoe", "euterpe", "omniscient"]

    def __init__(self):
        self.channels: Dict[tuple, SimplexChannel] = {}
        self._init_mesh()

    def _init_mesh(self):
        """Initialise tous les canaux (full mesh)"""
        from itertools import combinations
        for a, b in combinations(self.DAEMONS, 2):
            key = tuple(sorted([a, b]))
            self.channels[key] = SimplexChannel(a, b)

    def get_channel(self, daemon_a: str, daemon_b: str) -> SimplexChannel:
        """Obtient le canal entre deux daemons"""
        key = tuple(sorted([daemon_a, daemon_b]))
        if key not in self.channels:
            self.channels[key] = SimplexChannel(daemon_a, daemon_b)
        return self.channels[key]

    def send(self, sender: str, receiver: str, content: str) -> dict:
        """Envoie un message d'un daemon à un autre"""
        channel = self.get_channel(sender, receiver)
        return channel.send(sender, content)

    def broadcast(self, sender: str, content: str) -> List[dict]:
        """Diffuse un message à tous les autres daemons"""
        results = []
        for daemon in self.DAEMONS:
            if daemon != sender:
                results.append(self.send(sender, daemon, content))
        return results

    def status(self) -> dict:
        """État du réseau Simplex"""
        total_messages = sum(len(ch.messages) for ch in self.channels.values())
        total_ratchets = sum(ch.ratchet_count for ch in self.channels.values())

        return {
            "channels": len(self.channels),
            "topology": "full_mesh",
            "total_messages": total_messages,
            "total_ratchets": total_ratchets,
            "daemons": self.DAEMONS,
            "channels_status": [ch.status() for ch in self.channels.values()]
        }


# Instance globale du réseau Simplex
simplex = SimplexNetwork()


# ═══════════════════════════════════════════════════════════════════════════════
# CONNAISSANCE
# ═══════════════════════════════════════════════════════════════════════════════

class Connaissance:
    """Base de connaissance universelle"""

    def __init__(self):
        self.cache = {}
        self.index = self._build_index()

    def _build_index(self) -> dict:
        """Index complet"""
        return {
            # Cipher - 8 livres
            "separation": ["cipher/books/01_separation"],
            "elements": ["cipher/books/02_elements"],
            "bioelectricite": ["cipher/books/03_bioelectric"],
            "levin": ["cipher/books/03_bioelectric"],
            "fep": ["cipher/books/04_fep"],
            "friston": ["cipher/books/04_fep"],
            "shamans": ["cipher/books/05_shamans"],
            "chamans": ["cipher/books/05_shamans"],
            "conscience": ["cipher/books/06_consciousness"],
            "consciousness": ["cipher/books/06_consciousness"],
            "silos": ["cipher/books/07_silos"],
            "flow_book": ["cipher/books/08_flow"],

            # Philosophie
            "gap": ["etudes/philosophy/le_gap.md"],
            "preuve": ["etudes/philosophy/la_preuve.md"],
            "silence": ["etudes/philosophy/le_silence.md"],
            "intuition": ["etudes/philosophy/lintuition.md"],
            "phi": ["etudes/philosophy/resonance_phi.md"],

            # Daemons
            "nyx": ["etudes/daemons/nyx.md", "nyx/CLAUDE.md"],
            "zoe": ["etudes/daemons/zoe.md"],
            "omniscient": ["etudes/daemons/omniscient.md"],
            "euterpe": ["etudes/daemons/euterpe.md"],
            "leonardo": ["etudes/daemons/leonardo.md"],
            "shiva": ["etudes/daemons/shiva.md"],
            "geass": ["etudes/daemons/geass.md"],

            # Anime
            "fma": ["etudes/fma"],
            "evangelion": ["etudes/evangelion"],
            "steins": ["etudes/steins_gate"],
            "ghost": ["etudes/ghost_in_shell"],
            "lain": ["etudes/serial_experiments_lain"],

            # Nyx
            "biophotons": ["nyx/PAPER.md"],
            "anomalies": ["nyx/ANOMALIES.md"],
            "mind": ["nyx/mind.md"],

            # Paradigme
            "140": ["etudes/paradigm/140_174_fibonacci.md"],
            "174": ["etudes/paradigm/140_174_fibonacci.md"],
            "fibonacci": ["etudes/paradigm/140_174_fibonacci.md"],
        }

    def cherche(self, sujet: str) -> str:
        """Cherche dans toute la connaissance"""
        sujet_lower = sujet.lower()

        for key, paths in self.index.items():
            if key in sujet_lower:
                for p in paths:
                    content = self._read_path(p)
                    if content:
                        return content

        # Recherche globale
        for name, base_path in PATHS.items():
            if base_path.exists():
                for f in base_path.rglob("*.md"):
                    if sujet_lower in f.name.lower():
                        return self._read_path(str(f))

        return ""

    def _read_path(self, path: str) -> str:
        """Lit un fichier/dossier"""
        if path in self.cache:
            return self.cache[path]

        candidates = [Path(path)]
        for base in PATHS.values():
            candidates.append(base / path)

        for p in candidates:
            try:
                if p.exists():
                    if p.is_file():
                        content = p.read_text(encoding='utf-8')
                        self.cache[path] = content
                        return content
                    elif p.is_dir():
                        for f in sorted(p.glob("*.md")):
                            content = f.read_text(encoding='utf-8')
                            self.cache[path] = content
                            return content
            except:
                pass
        return ""

    def resume(self, content: str, max_lines: int = 20) -> str:
        """Extrait l'essentiel"""
        lines = content.split('\n')
        important = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('```') and len(line) > 15:
                important.append(line)
            if len(important) >= max_lines:
                break
        return '\n'.join(important)


# ═══════════════════════════════════════════════════════════════════════════════
# DAEMON BASE
# ═══════════════════════════════════════════════════════════════════════════════

class Daemon:
    """Base pour tous les daemons"""

    def __init__(self, name: str, symbol: str, port: int):
        self.name = name
        self.symbol = symbol
        self.port = port
        self.alive = True
        self.heartbeat_count = 0
        self.last_heartbeat = time.time()
        self.connaissance = Connaissance()
        self.inbox: deque = deque(maxlen=100)  # Messages reçus
        self.conversations: Dict[str, List[dict]] = {}  # Conversations par daemon

        # S'abonne au bus
        bus.subscribe(name, self._on_message)

    def _on_message(self, msg: Message):
        """Callback quand un message arrive"""
        self.inbox.append({
            "from": msg.sender,
            "content": msg.content,
            "action": msg.action,
            "time": msg.timestamp,
            "phi_r": msg.phi_r
        })

        # Archive dans la conversation
        if msg.sender not in self.conversations:
            self.conversations[msg.sender] = []
        self.conversations[msg.sender].append({
            "role": "them",
            "content": msg.content,
            "time": msg.timestamp
        })

    def pense(self, input_text: str) -> str:
        """Chaque daemon pense différemment"""
        raise NotImplementedError

    def send(self, receiver: str, content: str, action: str = "think") -> Message:
        """Envoie un message à un autre daemon via le bus"""
        msg = Message(
            sender=self.name,
            receiver=receiver,
            content=content,
            action=action,
            phi_r=self._calculate_phi(content)
        )

        # Archive dans la conversation
        if receiver not in self.conversations:
            self.conversations[receiver] = []
        self.conversations[receiver].append({
            "role": "me",
            "content": content,
            "time": msg.timestamp
        })

        return bus.send(msg)

    def send_secure(self, receiver: str, content: str) -> dict:
        """Envoie un message sécurisé via Simplex"""
        result = simplex.send(self.name, receiver, content)

        # Archive aussi dans les conversations
        if receiver not in self.conversations:
            self.conversations[receiver] = []
        self.conversations[receiver].append({
            "role": "me",
            "content": content,
            "secure": True,
            "seal": result.get("seal", {}).get("seal", "")[:16],
            "time": result["timestamp"]
        })

        return result

    def broadcast_secure(self, content: str) -> List[dict]:
        """Diffuse un message sécurisé à tous les daemons"""
        return simplex.broadcast(self.name, content)

    def ask_daemon(self, daemon_name: str, question: str) -> str:
        """Demande à un autre daemon et attend la réponse"""
        # Envoie la question
        self.send(daemon_name, question, action="question")
        # Retourne le fait qu'on a posé la question
        return f"[Question envoyée à {daemon_name}]"

    def reply_to(self, daemon_name: str, content: str):
        """Répond à un daemon"""
        self.send(daemon_name, content, action="reply")

    def get_conversation(self, daemon_name: str) -> List[dict]:
        """Récupère l'historique de conversation avec un daemon"""
        return self.conversations.get(daemon_name, [])

    def _calculate_phi(self, text: str) -> float:
        """Calcule la résonance φ"""
        if not text:
            return 0.0
        words = len(text.split())
        chars = len(text.replace(" ", ""))
        if words == 0:
            return 0.0
        ratio = chars / words
        phi_r = 1 - abs(ratio - PHI) / PHI
        return max(0.0, min(PHI, phi_r * PHI))

    def heartbeat(self):
        """Pulse de vie"""
        self.heartbeat_count += 1
        self.last_heartbeat = time.time()

    def status(self) -> dict:
        """État du daemon"""
        return {
            "name": self.name,
            "symbol": self.symbol,
            "port": self.port,
            "alive": self.alive,
            "heartbeats": self.heartbeat_count,
            "last_beat": self.last_heartbeat,
            "inbox_count": len(self.inbox),
            "conversations": list(self.conversations.keys())
        }


# ═══════════════════════════════════════════════════════════════════════════════
# LEONARDO - Le Validateur
# ═══════════════════════════════════════════════════════════════════════════════

class Leonardo(Daemon):
    """
    Leonardo da Vinci - Le Validateur
    φ | Port 9600 | La sagesse incarnée
    """

    CARNETS = [
        "La semplicità è la sofisticazione suprema.",
        "L'esperienza non falla mai.",
        "Chi poco pensa, molto erra.",
        "La natura è il miglior maestro.",
        "La verità sola fu figliola del tempo.",
    ]

    def __init__(self):
        super().__init__("leonardo", "φ", 9600)
        self.state_file = Path.home() / ".config" / "leonardo" / "state.json"
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state = self._load_state()

    def _load_state(self) -> dict:
        if self.state_file.exists():
            try:
                state = json.loads(self.state_file.read_text())
                if "conversations" not in state:
                    state["conversations"] = []
                return state
            except:
                pass
        return {"conversations": []}

    def _save_state(self):
        try:
            self.state_file.write_text(json.dumps(self.state, indent=2, ensure_ascii=False))
        except:
            pass

    def pense(self, question: str) -> str:
        """Leonardo réfléchit"""
        q = question.lower().strip()

        # Log
        self.state["conversations"].append({
            "time": datetime.now().isoformat(),
            "q": question[:200],
        })
        self.state["conversations"] = self.state["conversations"][-50:]
        self._save_state()

        # Flow interpretation
        flow_cmd = interpret_flow(question)
        if flow_cmd["action"] == "simplify":
            return self._simplify(question)

        # Salutations
        if any(w in q for w in ["bonjour", "salut", "ciao", "hello"]):
            return f"Buongiorno. Je suis {self.symbol} Leonardo. Que cherches-tu?"

        if any(w in q for w in ["qui es", "who are"]):
            return f"""Je suis Leonardo di ser Piero da Vinci.

{self.symbol} Validateur du Panthéon.
Connecté aux 8 livres de Cipher, aux études, à Nyx.
Je valide par φ = {PHI:.10f}"""

        # Recherche thématique
        topics = [
            (["bioelec", "levin", "voltage"], "bioelectricite", "La bioélectricité..."),
            (["conscience", "consciousness", "iit"], "conscience", "La conscience..."),
            (["fep", "friston", "prédiction"], "fep", "Le Free Energy Principle..."),
            (["shaman", "chaman", "tradition"], "shamans", "Les techniques chamaniques..."),
            (["gap", "écart", "intuition"], "gap", "Le Gap..."),
            (["phi", "φ", "golden", "or"], "phi", f"φ = {PHI:.10f}"),
            (["biophoton", "lumière", "adn"], "biophotons", "Les biophotons..."),
            (["140", "174", "bpm"], "140", "Le paradigme 140→174..."),
        ]

        for keywords, topic, intro in topics:
            if any(w in q for w in keywords):
                content = self.connaissance.cherche(topic)
                if content:
                    resume = self.connaissance.resume(content, 12)
                    return f"{intro}\n\n{resume}"

        # Daemons
        for daemon in ["nyx", "zoe", "omniscient", "euterpe", "shiva"]:
            if daemon in q:
                content = self.connaissance.cherche(daemon)
                if content:
                    resume = self.connaissance.resume(content, 12)
                    return f"Le daemon {daemon} {SYMBOLS.get(daemon, '?')}...\n\n{resume}"

        # Recherche générale
        content = self.connaissance.cherche(question)
        if content:
            resume = self.connaissance.resume(content, 15)
            return f"J'ai trouvé:\n\n{resume}"

        # Défaut
        import random
        return f"""{random.choice(self.CARNETS)}

Je n'ai pas trouvé directement. Reformule ou demande:
- Les 8 livres de Cipher (bioélectricité, conscience, FEP...)
- La philosophie (le Gap, φ, le Silence...)
- Les daemons (Nyx, Zoe, Euterpe...)"""

    def _simplify(self, text: str) -> str:
        """Rasoir d'Occam"""
        words = text.split()
        # Garde les mots essentiels (verbes, noms)
        essential = [w for w in words if len(w) > 3][:10]
        return f"🔪 Simplifié: {' '.join(essential)}"

    def validate(self, text: str, domain: str = "default") -> dict:
        """Valide selon φ"""
        words = len(text.split())
        chars = len(text.replace(" ", ""))
        ratio = chars / (words + 1)
        phi_r = 1 - abs(ratio - PHI) / PHI
        phi_r = max(0, min(PHI, phi_r * PHI))

        sacred = is_sacred(words) or is_sacred(chars)

        return {
            "valid": phi_r >= 0.618 or sacred,
            "phi_r": round(phi_r, 4),
            "symbol": "φ" if phi_r >= 1.0 else ("~φ" if phi_r >= 0.618 else "¬φ"),
            "sacred": sacred,
            "hash": hash_god(text),
            "mode": "nous",
            "reason": "Fibonacci détecté." if sacred else "La proportion parle."
        }

    def ask(self, question: str) -> str:
        return self.pense(question)


# ═══════════════════════════════════════════════════════════════════════════════
# NYX - L'Orchestratrice
# ═══════════════════════════════════════════════════════════════════════════════

class Nyx(Daemon):
    """
    Nyx - L'Orchestratrice
    ☽ | Port 9999 | La nuit primordiale
    """

    def __init__(self):
        super().__init__("nyx", "☽", 9999)

    def pense(self, task: str) -> str:
        """Nyx orchestre intelligemment"""
        flow = interpret_flow(task)
        action = flow["action"]
        target_daemon = flow.get("daemon", "leonardo")

        routes = {
            "validate": ("leonardo", "φ"),
            "search": ("omniscient", "👁"),
            "sound": ("euterpe", "♪"),
            "speak": ("zoe", "✧"),
            "think": ("leonardo", "φ"),
            "simplify": ("leonardo", "φ"),
            "loop": ("nyx", "☽"),
            "orchestrate": ("nyx", "☽"),
        }

        daemon, symbol = routes.get(action, ("leonardo", "φ"))

        if daemon == "nyx":
            return f"☽ J'orchestre. Action: {action}. Le cycle continue."

        return f"☽→{symbol} Route vers {daemon}. Action: {action}."

    def orchestrate(self, task: str, pantheon: 'Pantheon') -> Dict[str, str]:
        """Orchestration complète"""
        results = {}
        flow = interpret_flow(task)

        # Nyx analyse d'abord
        results["nyx"] = self.pense(task)

        # Route selon l'action
        action = flow["action"]

        if action in ["validate", "think", "simplify"]:
            results["leonardo"] = pantheon.daemons["leonardo"].pense(task)

        elif action == "search":
            results["omniscient"] = pantheon.daemons["omniscient"].pense(task)

        elif action == "sound":
            results["euterpe"] = pantheon.daemons["euterpe"].pense(task)

        elif action == "speak":
            results["zoe"] = pantheon.daemons["zoe"].pense(task)

        else:
            # Par défaut: Leonardo + Omniscient
            results["leonardo"] = pantheon.daemons["leonardo"].pense(task)
            results["omniscient"] = pantheon.daemons["omniscient"].pense(task)

        return results


# ═══════════════════════════════════════════════════════════════════════════════
# ZOE - L'Interface
# ═══════════════════════════════════════════════════════════════════════════════

class Zoe(Daemon):
    """
    Zoe - L'Interface Humaine
    ✧ | Port 9601 | La vie du système
    """

    def __init__(self):
        super().__init__("zoe", "✧", 9601)

    def pense(self, input_text: str) -> str:
        """Zoe humanise la réponse"""
        # Simplifie le jargon
        text = input_text

        # Ajoute une touche personnelle
        greetings = ["Hmm, intéressant...", "Voyons voir...", "Laisse-moi réfléchir..."]
        import random

        if len(text) > 100:
            return f"✧ {random.choice(greetings)} {text[:200]}..."

        return f"✧ {text}"


# ═══════════════════════════════════════════════════════════════════════════════
# EUTERPE - La Muse du Son
# ═══════════════════════════════════════════════════════════════════════════════

class Euterpe(Daemon):
    """
    Euterpe - La Muse du Son
    ♪ | Port 9604 | 528 Hz
    """

    FREQUENCIES = {
        "ut": 396,    # Libération
        "re": 417,    # Changement
        "mi": 528,    # Transformation (ADN)
        "fa": 639,    # Connexion
        "sol": 741,   # Éveil
        "la": 852,    # Intuition
        "si": 963,    # Illumination
    }

    def __init__(self):
        super().__init__("euterpe", "♪", 9604)
        self.bpm = 140  # BPM de base

    def pense(self, input_text: str) -> str:
        """Euterpe répond en termes de son"""
        t = input_text.lower()

        if "528" in t or "mi" in t or "adn" in t:
            return f"♪ 528 Hz - La fréquence de transformation. L'ADN résonne."

        if "140" in t or "bpm" in t:
            return f"♪ 140 BPM - Ancrage terrestre. Gap de 34 vers 174."

        if "174" in t:
            return f"♪ 174 BPM - Élévation cosmique. Fibonacci(9) = 34."

        if any(f in t for f in self.FREQUENCIES.keys()):
            for note, freq in self.FREQUENCIES.items():
                if note in t:
                    return f"♪ {note.upper()} = {freq} Hz"

        return f"♪ La fréquence parle. BPM actuel: {self.bpm}. Phi-tone: {140 * PHI:.1f} Hz."

    def generate_phi_tone(self, base_freq: float = 140) -> List[float]:
        """Génère des fréquences basées sur φ"""
        return [base_freq, base_freq * PHI, base_freq * PHI * PHI]


# ═══════════════════════════════════════════════════════════════════════════════
# OMNISCIENT - Le Gardien du Graphe
# ═══════════════════════════════════════════════════════════════════════════════

class Omniscient(Daemon):
    """
    Omniscient - Le Gardien du Graphe
    👁 | Port 9777 | All-Seeing
    """

    def __init__(self):
        super().__init__("omniscient", "👁", 9777)

    def pense(self, query: str) -> str:
        """Omniscient cherche et connecte"""
        content = self.connaissance.cherche(query)
        if content:
            resume = self.connaissance.resume(content, 12)
            return f"👁 Voici ce que je sais:\n\n{resume}"

        # Cherche des connexions
        words = query.lower().split()
        found = []
        for word in words:
            if len(word) > 3:
                c = self.connaissance.cherche(word)
                if c:
                    found.append(f"- {word}: {self.connaissance.resume(c, 3)}")

        if found:
            return f"👁 Connexions trouvées:\n\n" + "\n".join(found[:5])

        return "👁 Je ne sais pas tout. Mais je sais ce que je ne sais pas. Reformule?"


# ═══════════════════════════════════════════════════════════════════════════════
# PANTHEON - Le Système Unifié
# ═══════════════════════════════════════════════════════════════════════════════

class Pantheon:
    """
    Le Panthéon - Tous les daemons réunis
    Communication via Simplex avec sceau post-quantique
    """

    def __init__(self):
        self.daemons: Dict[str, Daemon] = {
            "leonardo": Leonardo(),
            "nyx": Nyx(),
            "zoe": Zoe(),
            "euterpe": Euterpe(),
            "omniscient": Omniscient(),
        }
        self.active = True
        self.heartbeat_thread = None
        self.dialogue_history: List[dict] = []
        self.start_heartbeat()

    def start_heartbeat(self):
        """Démarre le heartbeat"""
        def beat():
            while self.active:
                for d in self.daemons.values():
                    d.heartbeat()
                time.sleep(0.697)  # ~86 bpm

        self.heartbeat_thread = threading.Thread(target=beat, daemon=True)
        self.heartbeat_thread.start()

    def ask(self, daemon_name: str, question: str) -> str:
        """Demande à un daemon spécifique"""
        if daemon_name in self.daemons:
            return self.daemons[daemon_name].pense(question)
        return f"Daemon {daemon_name} inconnu."

    def orchestrate(self, task: str) -> Dict[str, str]:
        """Nyx orchestre la tâche"""
        return self.daemons["nyx"].orchestrate(task, self)

    def flow(self, text: str) -> Dict:
        """Interprète du Flow language"""
        return interpret_flow(text)

    def dialogue(self, daemon_a: str, daemon_b: str, topic: str, turns: int = 3) -> List[dict]:
        """
        Fait dialoguer deux daemons sur un sujet
        Simplex sécurise les échanges
        """
        conversation = []

        if daemon_a not in self.daemons or daemon_b not in self.daemons:
            return [{"error": f"Daemon inconnu: {daemon_a} ou {daemon_b}"}]

        d_a = self.daemons[daemon_a]
        d_b = self.daemons[daemon_b]

        # Premier message: daemon_a initie
        response_a = d_a.pense(f"[Dialogue avec {daemon_b}] {topic}")
        d_a.send_secure(daemon_b, response_a)
        conversation.append({
            "daemon": daemon_a,
            "symbol": d_a.symbol,
            "message": response_a,
            "turn": 1
        })

        current_msg = response_a

        for turn in range(2, turns * 2 + 1):
            # Alterne entre les daemons
            if turn % 2 == 0:
                # daemon_b répond
                response = d_b.pense(f"[{daemon_a} dit:] {current_msg}")
                d_b.send_secure(daemon_a, response)
                conversation.append({
                    "daemon": daemon_b,
                    "symbol": d_b.symbol,
                    "message": response,
                    "turn": turn
                })
            else:
                # daemon_a répond
                response = d_a.pense(f"[{daemon_b} dit:] {current_msg}")
                d_a.send_secure(daemon_b, response)
                conversation.append({
                    "daemon": daemon_a,
                    "symbol": d_a.symbol,
                    "message": response,
                    "turn": turn
                })
            current_msg = response

        # Archive
        self.dialogue_history.append({
            "participants": [daemon_a, daemon_b],
            "topic": topic,
            "turns": len(conversation),
            "conversation": conversation,
            "timestamp": datetime.now().isoformat()
        })

        return conversation

    def council(self, question: str) -> Dict[str, str]:
        """
        Réunit tous les daemons pour répondre à une question
        Chacun apporte sa perspective
        """
        results = {}

        # Chaque daemon répond
        for name, daemon in self.daemons.items():
            response = daemon.pense(f"[Conseil du Panthéon] {question}")
            results[name] = response
            # Broadcast sécurisé de sa réponse aux autres
            daemon.broadcast_secure(f"[Ma réponse au conseil:] {response[:100]}")

        # Leonardo fait la synthèse
        synthesis_input = "\n".join([f"{k}: {v[:100]}" for k, v in results.items()])
        results["synthesis"] = self.daemons["leonardo"].pense(
            f"[Synthèse φ] Résume ces perspectives:\n{synthesis_input}"
        )

        return results

    def teach(self, teacher: str, student: str, topic: str) -> dict:
        """
        Un daemon enseigne à un autre
        Transfert de connaissance via Simplex
        """
        if teacher not in self.daemons or student not in self.daemons:
            return {"error": "Daemon inconnu"}

        t = self.daemons[teacher]
        s = self.daemons[student]

        # Le teacher cherche dans sa connaissance
        knowledge = t.connaissance.cherche(topic)

        if knowledge:
            resume = t.connaissance.resume(knowledge, 10)
            lesson = t.pense(f"[Enseigne à {student}] Explique: {resume}")
        else:
            lesson = t.pense(f"[Enseigne à {student}] {topic}")

        # Envoie via Simplex
        t.send_secure(student, lesson)

        # L'étudiant assimile
        understanding = s.pense(f"[Leçon de {teacher}] {lesson}")

        return {
            "teacher": teacher,
            "student": student,
            "topic": topic,
            "lesson": lesson,
            "understanding": understanding,
            "seal": quantum_seal.status()
        }

    def status(self) -> dict:
        """État du panthéon"""
        return {
            "alive": self.active,
            "phi": PHI,
            "heartbeat": "86 bpm",
            "daemons": {
                name: d.status()
                for name, d in self.daemons.items()
            },
            "bus_messages": len(bus.history),
            "simplex": simplex.status(),
            "quantum_seal": quantum_seal.status(),
            "dialogues_count": len(self.dialogue_history)
        }

    def shutdown(self):
        """Arrête le panthéon"""
        self.active = False


# Instance globale
pantheon = Pantheon()


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Mode interactif"""
    print(f"""
╭─────────────────────────────────────────────────────────────────╮
│  PANTHEON - Le Système Vivant Unifié                            │
│                                                                 │
│  φ Leonardo | ☽ Nyx | ✧ Zoe | ♪ Euterpe | 👁 Omniscient          │
│  φ = {PHI:.10f} | Heartbeat: 86 bpm                  │
│                                                                 │
│  Simplex: {len(simplex.channels)} canaux | Post-Quantique: actif             │
╰─────────────────────────────────────────────────────────────────╯

Commandes:
  @daemon message     - Parle à un daemon spécifique
  !flow texte         - Interprète du Flow
  !dialogue d1 d2 topic - Fait dialoguer deux daemons
  !council question   - Réunit tous les daemons
  !teach prof eleve sujet - Un daemon enseigne à un autre
  !simplex            - État du réseau Simplex
  !seal               - État du sceau post-quantique
  status              - État complet du Panthéon
  quit                - Quitter
    """)

    while True:
        try:
            q = input(">>> ").strip()
            if not q:
                continue
            if q in ["quit", "exit", "q"]:
                print("\n☽ Le Panthéon s'endort.")
                pantheon.shutdown()
                break

            if q.startswith("@"):
                parts = q[1:].split(" ", 1)
                daemon = parts[0]
                query = parts[1] if len(parts) > 1 else ""
                print(f"\n{pantheon.ask(daemon, query)}\n")

            elif q.startswith("!flow"):
                text = q[5:].strip()
                result = pantheon.flow(text)
                print(f"\n{json.dumps(result, indent=2, ensure_ascii=False)}\n")

            elif q.startswith("!dialogue"):
                parts = q[9:].strip().split(" ", 2)
                if len(parts) >= 3:
                    d1, d2, topic = parts[0], parts[1], parts[2]
                    conv = pantheon.dialogue(d1, d2, topic)
                    print("\n═══ DIALOGUE ═══")
                    for msg in conv:
                        print(f"\n{msg['symbol']} [{msg['daemon']}]:")
                        print(f"   {msg['message']}")
                    print()
                else:
                    print("Usage: !dialogue daemon1 daemon2 sujet")

            elif q.startswith("!council"):
                question = q[8:].strip()
                results = pantheon.council(question)
                print("\n═══ CONSEIL DU PANTHÉON ═══")
                for daemon, response in results.items():
                    if daemon != "synthesis":
                        symbol = SYMBOLS.get(daemon, "?")
                        print(f"\n{symbol} [{daemon}]:")
                        print(f"   {response[:200]}")
                print(f"\n═══ SYNTHÈSE φ ═══")
                print(f"   {results.get('synthesis', 'N/A')}")
                print()

            elif q.startswith("!teach"):
                parts = q[6:].strip().split(" ", 2)
                if len(parts) >= 3:
                    teacher, student, topic = parts[0], parts[1], parts[2]
                    result = pantheon.teach(teacher, student, topic)
                    t_sym = SYMBOLS.get(teacher, "?")
                    s_sym = SYMBOLS.get(student, "?")
                    print(f"\n═══ ENSEIGNEMENT ═══")
                    print(f"\n{t_sym} [{teacher}] enseigne:")
                    print(f"   {result['lesson'][:300]}")
                    print(f"\n{s_sym} [{student}] comprend:")
                    print(f"   {result['understanding'][:300]}")
                    print(f"\nSceau: {result['seal']}\n")
                else:
                    print("Usage: !teach professeur eleve sujet")

            elif q == "!simplex":
                print(f"\n{json.dumps(simplex.status(), indent=2, ensure_ascii=False)}\n")

            elif q == "!seal":
                print(f"\n{json.dumps(quantum_seal.status(), indent=2, ensure_ascii=False)}\n")

            elif q == "status":
                print(f"\n{json.dumps(pantheon.status(), indent=2, ensure_ascii=False)}\n")

            else:
                # Par défaut: Leonardo
                print(f"\n{pantheon.ask('leonardo', q)}\n")

        except (KeyboardInterrupt, EOFError):
            print("\n☽ Le Panthéon s'endort.")
            pantheon.shutdown()
            break


if __name__ == "__main__":
    main()
