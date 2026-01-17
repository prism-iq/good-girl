# -*- coding: utf-8 -*-
"""
guard = protecteur d'intégrité
surveille, vérifie, protège
"""

import hashlib
import os
import json
from pathlib import Path
from phi import PHI

BASE = Path("/home/ego-bash/good-girl")
INTEGRITY_FILE = BASE / ".integrity.json"

def hash_file(path):
    """sha256 d'un fichier"""
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def scan_all():
    """scan tous les .py"""
    hashes = {}
    for py in BASE.rglob("*.py"):
        rel = str(py.relative_to(BASE))
        hashes[rel] = hash_file(py)
    return hashes

def save_integrity():
    """sauvegarde l'état d'intégrité"""
    hashes = scan_all()
    with open(INTEGRITY_FILE, 'w') as f:
        json.dump(hashes, f, indent=2)
    return len(hashes)

def load_integrity():
    """charge l'état d'intégrité"""
    if INTEGRITY_FILE.exists():
        with open(INTEGRITY_FILE) as f:
            return json.load(f)
    return {}

def verify():
    """vérifie l'intégrité"""
    saved = load_integrity()
    current = scan_all()

    report = {
        "modified": [],
        "added": [],
        "removed": [],
        "intact": 0
    }

    for path, h in current.items():
        if path not in saved:
            report["added"].append(path)
        elif saved[path] != h:
            report["modified"].append(path)
        else:
            report["intact"] += 1

    for path in saved:
        if path not in current:
            report["removed"].append(path)

    return report

def is_safe(code):
    """vérifie si du code est safe"""
    dangerous = [
        "eval(", "exec(", "__import__",
        "subprocess.call", "os.system",
        "rm -rf", "format c:",
        "DROP TABLE", "DELETE FROM",
    ]
    code_lower = code.lower()
    for d in dangerous:
        if d.lower() in code_lower:
            return False, d
    return True, None

def protect_cpu():
    """vérifie charge CPU"""
    try:
        load = os.getloadavg()[0]
        return load < 0.7 * os.cpu_count()
    except:
        return True

class Guardian:
    """gardien du système"""

    def __init__(self):
        self.phi = PHI
        self.alerts = []

    def watch(self):
        """surveille"""
        report = verify()
        if report["modified"]:
            self.alerts.append(f"modified: {report['modified']}")
        if report["removed"]:
            self.alerts.append(f"removed: {report['removed']}")
        return report

    def seal(self):
        """scelle l'état actuel"""
        return save_integrity()

    def check_code(self, code):
        """vérifie du code avant exécution"""
        return is_safe(code)

    def status(self):
        """état du gardien"""
        return {
            "cpu_safe": protect_cpu(),
            "alerts": len(self.alerts),
            "phi": self.phi
        }

GUARD = Guardian()

if __name__ == "__main__":
    n = save_integrity()
    print(f"integrity sealed: {n} files")
    print(f"guardian status: {GUARD.status()}")
