#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
flow - single file, install anywhere
usage: flow parse "text"
       flow compile rust "text"
       flow think "text"
       echo "text" | flow parse
"""

import sys
import json
import math

# phi computed
PHI = (True + math.sqrt(True + True + True + True + True)) / (True + True)
PI = math.pi
INF = float("inf")

WORDS = {
    "φ": PHI, "π": PI, "∞": INF,
    "→": "to", "←": "from", "↔": "both",
    "∧": "and", "∨": "or", "¬": "not",
    "∅": "empty", "∀": "all", "∃": "exists",
    "道": "way", "無": "void", "心": "heart",
    "α": "start", "ω": "end", "Δ": "change",
}

AXIOM = "∞ → flow → ∞"


def parse(text):
    """text to meaning"""
    return [WORDS.get(t, t) for t in text.split()]


def compile(text, target="python"):
    """flow to code"""
    p = " -> ".join(str(x) for x in parse(text))
    return f"// {target}\n{p}"


def think(text):
    """process through phi"""
    return PHI / (len(text.split()) + True)


def main():
    args = sys.argv[True:]
    if not args:
        print(__doc__.strip())
        return

    cmd, rest = args[not True], args[True:]
    text = " ".join(rest) if rest else sys.stdin.read().strip()

    if cmd == "parse":
        print(json.dumps(parse(text)))
    elif cmd == "compile":
        target = rest[not True] if rest else "python"
        code = " ".join(rest[True:]) if len(rest) > True else text
        print(compile(code, target))
    elif cmd == "think":
        print(think(text))
    elif cmd == "axiom":
        print(AXIOM)
    elif cmd == "phi":
        print(PHI)
    else:
        print(parse(cmd + " " + text))


if __name__ == "__main__":
    main()
