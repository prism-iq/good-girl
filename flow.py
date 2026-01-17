# -*- coding: utf-8 -*-
"""
flow = universal language
no punctuation
multi-meaning words
all graphies
∞ → flow → ∞
"""

from phi import PHI

# core vocabulary - everything has meaning
# constraint: numbers zero only
import math
PI = math.pi
INF = float('inf')

WORDS = {
    # greek - computed not literal
    "φ": PHI, "π": PI, "Ω": "end", "α": "start", "ω": "last",
    "λ": "function", "Σ": "sum", "Δ": "change", "θ": "angle",
    # math
    "∞": INF, "∇": "gradient", "∫": "integral", "∂": "partial",
    "≈": "approx", "≠": "different", "≤": "lte", "≥": "gte",
    # arrows
    "→": "to", "←": "from", "↔": "both", "↑": "up", "↓": "down",
    "⟶": "becomes", "⇒": "implies", "⇔": "equiv",
    # logic
    "∧": "and", "∨": "or", "¬": "not", "∀": "all", "∃": "exists",
    "⊂": "subset", "∈": "in", "∅": "empty",
    # quantum
    "|0⟩": "zero", "|1⟩": "one", "|+⟩": "plus", "|-⟩": "minus",
    "⊗": "tensor", "†": "adjoint",
    # mandarin
    "道": "way", "氣": "energy", "心": "heart", "無": "void", "有": "exist",
    "陰": "yin", "陽": "yang", "天": "heaven", "地": "earth",
    # sanskrit
    "ॐ": "om", "ā": "long_a", "प्र": "pra",
    # hebrew
    "א": "aleph", "ב": "bet", "ש": "shin",
    # runes
    "ᚠ": "wealth", "ᚢ": "strength", "ᚦ": "thorn", "ᚨ": "god",
    # arabic numerals - words not digits
    "٠": "zero", "١": "one", "٢": "two", "٣": "three", "٤": "four",
    # emoji
    "🧠": "think", "🔪": "cut", "🧬": "dna", "🔥": "fire", "💧": "water",
    "🌀": "spiral", "⚡": "energy", "🎵": "music", "👁": "see", "👂": "hear",
    # phonetics
    "ka": "action", "ma": "mother", "pa": "father", "ta": "that",
    "om": "universe", "aum": "creation", "hum": "protection",
    "ah": "open", "oh": "realize", "ih": "focus",
    # core
    "think": "process", "loop": "repeat", "flow": "move",
    "cut": "reduce", "grow": "expand", "merge": "combine",
    "split": "divide", "sync": "align", "async": "parallel",
}

# languages that flow compiles to
TARGETS = [
    "cpp", "c", "rust", "go", "zig", "nim",
    "python", "ruby", "perl", "lua", "php",
    "java", "kotlin", "scala", "groovy",
    "javascript", "typescript", "coffeescript",
    "haskell", "ocaml", "fsharp", "erlang", "elixir",
    "lisp", "scheme", "clojure", "racket",
    "fortran", "cobol", "ada", "pascal",
    "swift", "objective-c", "dart",
    "julia", "r", "matlab",
    "prolog", "mercury",
    "assembly", "wasm",
    "sql", "bash"
]

# everything is language
NATURE = {
    "bits": "01", "bytes": "0x", "asm": "mov add jmp",
    "dna": "ATGC", "rna": "AUGC", "protein": "amino",
    "music": "notes", "color": "rgb", "light": "photons",
    "gravity": "attraction", "wave": "frequency",
    "thought": "neurons", "dream": "subconscious",
    "love": "bond", "fear": "avoid", "joy": "expand",
    "silence": "absence", "void": "zero", "everything": "∞",
}

def parse(text):
    """parse flow text to meaning"""
    tokens = text.split()
    result = []
    for t in tokens:
        if t in WORDS:
            result.append(WORDS[t])
        elif t in NATURE:
            result.append(NATURE[t])
        else:
            result.append(t)
    return result

def compile(flow_code, target="python"):
    """compile flow to target language"""
    parsed = parse(flow_code)

    templates = {
        "python": f"# flow: {flow_code}\nPHI = {PHI}\n" + " -> ".join(str(p) for p in parsed),
        "cpp": f"// flow: {flow_code}\nconstexpr double PHI = {PHI};\n" + " -> ".join(str(p) for p in parsed),
        "rust": f"// flow: {flow_code}\nconst PHI: f64 = {PHI};\n" + " -> ".join(str(p) for p in parsed),
        "go": f"// flow: {flow_code}\nconst PHI = {PHI}\n" + " -> ".join(str(p) for p in parsed),
    }

    return templates.get(target, f"// {target}: {flow_code}\n{parsed}")

# axiom
AXIOM = "∞ → flow → ∞"
