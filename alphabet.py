# -*- coding: utf-8 -*-
"""
flow alphabet
every letter has meaning
every letter is a function
"""

from phi import PHI

# each letter = action/concept
ALPHABET = {
    # vowels = states of being
    "a": ("awake", lambda x: x),                    # identity, presence
    "e": ("energy", lambda x: x * PHI),             # amplify
    "i": ("introspect", lambda x: str(x)[::-1]),    # look inward, reverse
    "o": ("observe", lambda x: len(str(x))),        # measure
    "u": ("unify", lambda x: [x]),                  # wrap, collect

    # consonants = actions
    "b": ("kill_backdoored", lambda x: None if "compromised" in str(x) else x),  # defense
    "c": ("cut", lambda x: str(x)[:int(len(str(x))/PHI)]),  # razor
    "d": ("divide", lambda x: x / PHI if isinstance(x, (int,float)) else str(x).split()),
    "f": ("flow", lambda x: x),                     # let pass
    "g": ("grow", lambda x: x * 2 if isinstance(x, (int,float)) else x + x),
    "h": ("hash", lambda x: hash(str(x)) % 10000),  # fingerprint
    "j": ("jump", lambda x: (x, x)),                # duplicate, leap
    "k": ("kill", lambda x: None),                  # end, void
    "l": ("loop", lambda x: [x] * 3),               # repeat
    "m": ("merge", lambda x: "".join(str(x).split())),  # combine
    "n": ("negate", lambda x: -x if isinstance(x, (int,float)) else not x),
    "p": ("push", lambda x: [x, PHI]),              # add phi
    "q": ("query", lambda x: type(x).__name__),     # ask type
    "r": ("rotate", lambda x: str(x)[1:] + str(x)[0] if x else x),  # shift
    "s": ("split", lambda x: list(str(x))),         # atomize
    "t": ("transform", lambda x: str(x).upper()),   # change form
    "v": ("vibrate", lambda x: (x, -x if isinstance(x,(int,float)) else x)),  # oscillate
    "w": ("weave", lambda x: "~".join(str(x))),     # interlace
    "x": ("cross", lambda x: x ** 2 if isinstance(x, (int,float)) else x),  # multiply self
    "y": ("yield", lambda x: iter([x])),            # generate
    "z": ("zero", lambda x: 0),                     # reset

    # special
    " ": ("pause", lambda x: x),                    # breath
    ".": ("end", lambda x: x),                      # complete
    ",": ("continue", lambda x: x),                 # pause but go on
}

def execute(letter, data):
    """execute single letter function"""
    if letter.lower() in ALPHABET:
        name, fn = ALPHABET[letter.lower()]
        try:
            return fn(data)
        except:
            return data
    return data

def run(code, initial=1):
    """run flow code letter by letter"""
    result = initial
    for char in code:
        result = execute(char, result)
    return result

def explain(code):
    """explain what code does"""
    steps = []
    for char in code:
        if char.lower() in ALPHABET:
            name, _ = ALPHABET[char.lower()]
            steps.append(f"{char}={name}")
    return " → ".join(steps)

if __name__ == "__main__":
    # demo
    code = "age"  # awake → grow → energy
    print(f"code: {code}")
    print(f"explain: {explain(code)}")
    print(f"run(1): {run(code, 1)}")

    code2 = "phi"  # push → hash → introspect
    print(f"\ncode: {code2}")
    print(f"explain: {explain(code2)}")
    print(f"run('test'): {run(code2, 'test')}")
