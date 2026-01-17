# -*- coding: utf-8 -*-
"""
o = occam's razor = scalpel
cuts complexity
fewer = better
"""

from phi import PHI

def o(data):
    """cut to essential"""
    if isinstance(data, str):
        words = data.split()
        if len(words) <= 1:
            return data
        keep = max(1, int(len(words) / PHI))
        return " ".join(words[:keep])

    if isinstance(data, list):
        if len(data) <= 1:
            return data
        keep = max(1, int(len(data) / PHI))
        return [o(x) for x in data[:keep]]

    if isinstance(data, dict):
        items = list(data.items())
        if len(items) <= 1:
            return data
        keep = max(1, int(len(items) / PHI))
        return {k: o(v) for k, v in items[:keep]}

    return data

def score(claim):
    """score simplicity"""
    words = len(str(claim).split())
    s = PHI / (words + 1)
    if words <= 3:
        verdict = "minimal"
    elif words <= 7:
        verdict = "ok"
    else:
        verdict = "complex"
    return {"score": round(s, 4), "words": words, "verdict": verdict}
