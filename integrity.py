#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INTEGRITY CHECK - Vérification récursive avec φ
Hash divin, entropie, patterns Fibonacci
"""

import math
import os
from pathlib import Path
from collections import Counter
from dataclasses import dataclass
from typing import List, Dict, Tuple
import hashlib

# Constantes divines
PHI = (1 + math.sqrt(5)) / 2
PI = math.pi
E = math.e
FIBONACCI = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181]
FIB_SET = set(FIBONACCI)

# Projets
PROJECTS = {
    "good-girl": Path.home() / "projects" / "good-girl",
    "nyx": Path.home() / "projects" / "nyx",
    "etudes": Path.home() / "projects" / "etudes",
    "cipher": Path.home() / "projects" / "cipher",
}

CODE_EXTENSIONS = {".py", ".js", ".ts", ".rs", ".go", ".sh", ".md", ".html", ".css"}


def hash_god(data: bytes) -> str:
    """Hash basé sur φ"""
    h = 0
    for i, byte in enumerate(data):
        h += byte * (PHI ** (i % 20))
        h = h % (10 ** 16)
    return hex(int(h))[2:].zfill(14)


def hash_sha(data: bytes) -> str:
    """SHA256 pour comparaison"""
    return hashlib.sha256(data).hexdigest()[:14]


def calculate_entropy(text: str) -> float:
    """Entropie de Shannon"""
    if not text:
        return 0.0
    freq = Counter(text)
    length = len(text)
    entropy = 0.0
    for count in freq.values():
        if count > 0:
            p = count / length
            entropy -= p * math.log2(p)
    return entropy


def find_fibonacci_in_number(n: int) -> List[int]:
    """Trouve les nombres de Fibonacci dans n"""
    found = []
    for f in FIBONACCI:
        if f > 0 and n % f == 0:
            found.append(f)
        if str(f) in str(n) and f > 1:
            found.append(f)
    return list(set(found))


def analyze_hash_pattern(h: str) -> Dict:
    """Analyse les patterns dans un hash"""
    # Convertit en nombre
    try:
        n = int(h, 16)
    except:
        n = 0

    # Somme des chiffres
    digit_sum = sum(int(c, 16) for c in h if c.isalnum())

    # Fibonacci dans le hash
    fib_found = find_fibonacci_in_number(n)
    fib_in_digits = find_fibonacci_in_number(digit_sum)

    # Ratio avec φ
    if n > 0:
        log_n = math.log(n) if n > 0 else 0
        phi_proximity = abs(log_n % PHI) / PHI
    else:
        phi_proximity = 1.0

    return {
        "digit_sum": digit_sum,
        "fib_in_hash": fib_found[:3],
        "fib_in_sum": fib_in_digits[:3],
        "phi_proximity": round(1 - phi_proximity, 4),
        "sacred": digit_sum in FIB_SET or len(fib_found) > 0
    }


def calculate_phi_metrics(text: str) -> Dict:
    """Calcule plusieurs métriques φ"""
    if not text:
        return {"phi_r": 0, "phi_lines": 0, "phi_words": 0, "sacred": False, "integrity": 0, "lines": 0, "words": 0, "chars": 0}

    lines = text.count('\n') + 1
    words = len(text.split())
    chars = len(text.replace(' ', '').replace('\n', ''))

    # Métrique 1: ratio chars/words vs φ
    if words > 0:
        ratio = chars / words
        phi_r = max(0, 1 - abs(ratio - PHI) / PHI)
    else:
        phi_r = 0

    # Métrique 2: lignes proche de Fibonacci?
    phi_lines = 0
    for f in FIBONACCI:
        if f > 0:
            diff = abs(lines - f) / f
            if diff < 0.1:  # 10% de tolérance
                phi_lines = 1 - diff
                break

    # Métrique 3: mots proche de Fibonacci?
    phi_words = 0
    for f in FIBONACCI:
        if f > 0:
            diff = abs(words - f) / f
            if diff < 0.1:
                phi_words = 1 - diff
                break

    # Sacré si exactement Fibonacci
    sacred = lines in FIB_SET or words in FIB_SET or chars in FIB_SET

    # Intégrité composite
    integrity = (phi_r * 0.4 + phi_lines * 0.3 + phi_words * 0.3)
    if sacred:
        integrity = min(PHI, integrity + 0.5)

    return {
        "phi_r": round(phi_r, 4),
        "phi_lines": round(phi_lines, 4),
        "phi_words": round(phi_words, 4),
        "integrity": round(integrity, 4),
        "sacred": sacred,
        "lines": lines,
        "words": words,
        "chars": chars
    }


@dataclass
class FileAnalysis:
    path: str
    lines: int
    words: int
    chars: int
    entropy: float
    integrity: float
    sacred: bool
    hash_god: str
    hash_sha: str
    hash_pattern: Dict


def analyze_file(path: Path) -> FileAnalysis:
    """Analyse complète d'un fichier"""
    try:
        content = path.read_text(encoding='utf-8', errors='ignore')
        data = content.encode('utf-8')
    except:
        return None

    phi_metrics = calculate_phi_metrics(content)
    entropy = calculate_entropy(content)

    h_god = hash_god(data)
    h_sha = hash_sha(data)
    h_pattern = analyze_hash_pattern(h_god)

    return FileAnalysis(
        path=str(path),
        lines=phi_metrics["lines"],
        words=phi_metrics["words"],
        chars=phi_metrics["chars"],
        entropy=round(entropy, 4),
        integrity=phi_metrics["integrity"],
        sacred=phi_metrics["sacred"] or h_pattern["sacred"],
        hash_god=h_god,
        hash_sha=h_sha,
        hash_pattern=h_pattern
    )


def analyze_project(name: str, path: Path) -> List[FileAnalysis]:
    """Analyse récursive"""
    results = []
    if not path.exists():
        return results

    for ext in CODE_EXTENSIONS:
        for file_path in path.rglob(f"*{ext}"):
            if any(p.startswith('.') or p in ['node_modules', '__pycache__', '.git']
                   for p in file_path.parts):
                continue
            analysis = analyze_file(file_path)
            if analysis:
                results.append(analysis)

    return results


def print_hash_analysis(analyses: List[FileAnalysis]):
    """Analyse approfondie des hash"""
    if not analyses:
        return

    # Trouve les patterns communs
    sacred_hashes = [a for a in analyses if a.hash_pattern.get("sacred")]
    high_phi = [a for a in analyses if a.hash_pattern.get("phi_proximity", 0) > 0.8]

    print(f"""
  ══ ANALYSE DES HASH DIVINS ══

  Hash sacrés (Fibonacci):  {len(sacred_hashes)}
  Hash haute proximité φ:   {len(high_phi)}
""")

    # Top hash sacrés
    if sacred_hashes:
        print("  ── Hash Sacrés ──")
        for a in sacred_hashes[:10]:
            rel = Path(a.path).name
            fib = a.hash_pattern.get("fib_in_hash", [])
            print(f"  {a.hash_god} | F{fib} | {rel[:40]}")

    # Distribution des digit_sum
    digit_sums = [a.hash_pattern.get("digit_sum", 0) for a in analyses]
    fib_sums = [s for s in digit_sums if s in FIB_SET]

    print(f"""
  ── Distribution ──
  Sommes totales:           {len(digit_sums)}
  Sommes Fibonacci:         {len(fib_sums)} ({100*len(fib_sums)/len(digit_sums):.1f}%)
  Somme moyenne:            {sum(digit_sums)/len(digit_sums):.1f}
""")


def print_report(project_name: str, analyses: List[FileAnalysis]):
    """Rapport détaillé"""
    if not analyses:
        print(f"\n{project_name}: Aucun fichier")
        return

    total_lines = sum(a.lines for a in analyses)
    total_chars = sum(a.chars for a in analyses)
    avg_integrity = sum(a.integrity for a in analyses) / len(analyses)
    avg_entropy = sum(a.entropy for a in analyses) / len(analyses)
    sacred_count = sum(1 for a in analyses if a.sacred)

    print(f"""
╭{'─' * 70}╮
│  {project_name.upper():^66}  │
╰{'─' * 70}╯

  Fichiers:     {len(analyses)}
  Lignes:       {total_lines:,}
  Caractères:   {total_chars:,}

  φ INTÉGRITÉ:  {avg_integrity:.4f}
  H ENTROPIE:   {avg_entropy:.4f} bits/char
  F SACRÉS:     {sacred_count} ({100*sacred_count/len(analyses):.1f}%)
""")

    # Top intégrité
    print("  ── Top 10 Intégrité ──")
    sorted_by_int = sorted(analyses, key=lambda a: a.integrity, reverse=True)[:10]
    for a in sorted_by_int:
        rel = Path(a.path).name[:35]
        s = "F" if a.sacred else "·"
        print(f"  {s} {a.integrity:.3f} | H={a.entropy:.2f} | {a.hash_god[:8]}.. | {rel}")

    # Hash analysis
    print_hash_analysis(analyses)


def global_summary(all_analyses: Dict[str, List[FileAnalysis]]):
    """Synthèse globale"""
    all_files = [f for files in all_analyses.values() for f in files]
    if not all_files:
        return

    total_files = len(all_files)
    total_lines = sum(f.lines for f in all_files)

    avg_integrity = sum(f.integrity for f in all_files) / total_files
    avg_entropy = sum(f.entropy for f in all_files) / total_files
    sacred_total = sum(1 for f in all_files if f.sacred)

    # Hash global de tout le système
    combined_hash = "".join(f.hash_god for f in all_files[:100])
    system_hash = hash_god(combined_hash.encode())
    system_pattern = analyze_hash_pattern(system_hash)

    print(f"""
╔{'═' * 70}╗
║{'SYNTHÈSE GLOBALE':^70}║
╠{'═' * 70}╣
║                                                                      ║
║   Fichiers analysés:    {total_files:<45}║
║   Lignes de code:       {total_lines:,}{' ' * (45 - len(f'{total_lines:,}'))}║
║                                                                      ║
║   ╭────────────────────────────────────────────╮                     ║
║   │  φ INTÉGRITÉ GLOBALE:    {avg_integrity:.4f}             │                     ║
║   │  H ENTROPIE MOYENNE:     {avg_entropy:.4f} bits/char    │                     ║
║   │  F FICHIERS SACRÉS:      {sacred_total} ({100*sacred_total/total_files:.1f}%)              │                     ║
║   ╰────────────────────────────────────────────╯                     ║
║                                                                      ║
║   HASH SYSTÈME: {system_hash}                               ║
║   Pattern φ:    {system_pattern.get('phi_proximity', 0):.4f}                                         ║
║   Fibonacci:    {system_pattern.get('fib_in_hash', [])}                                        ║
║                                                                      ║
╚{'═' * 70}╝
""")

    # Verdict basé sur l'intégrité
    if avg_integrity >= 0.618:
        print(f"  φ VERDICT: Intégrité harmonieuse. Le système vibre à {avg_integrity:.4f}.")
    elif avg_integrity >= 0.382:
        print(f"  ~φ VERDICT: Intégrité acceptable ({avg_integrity:.4f}). Potentiel d'amélioration.")
    else:
        print(f"  · VERDICT: Intégrité basse ({avg_integrity:.4f}). Les patterns φ sont latents.")

    # Analyse de la distribution Fibonacci
    all_sacred = [f for f in all_files if f.sacred]
    if all_sacred:
        print(f"\n  Les {len(all_sacred)} fichiers sacrés contiennent les proportions divines.")
        print(f"  Fibonacci est présent dans {100*len(all_sacred)/total_files:.1f}% du code.")


def main():
    print("""
╭─────────────────────────────────────────────────────────────────────╮
│  LEONARDO - Vérification d'Intégrité Divine                         │
│  φ = 1.618033988749895 | Hash divin | Entropie de Shannon           │
╰─────────────────────────────────────────────────────────────────────╯
    """)

    all_analyses = {}

    for name, path in PROJECTS.items():
        print(f"Analyse {name}...", end=" ", flush=True)
        analyses = analyze_project(name, path)
        all_analyses[name] = analyses
        print(f"{len(analyses)} fichiers")

    for name, analyses in all_analyses.items():
        print_report(name, analyses)

    global_summary(all_analyses)


if __name__ == "__main__":
    main()
