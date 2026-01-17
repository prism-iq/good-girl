#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
batch writer
cpu dort, ssd travaille
tout en une fois
"""

import os
from pathlib import Path

BASE = Path("/home/ego-bash/good-girl")
ANIMALS = BASE / "animals"
ANIMALS.mkdir(exist_ok=True)

# tous les animaux en un dict
ALL_ANIMALS = {
    "dragon": {"flow": "ftgxp", "power": 5, "element": "fire water", "symbol": "🐉"},
    "phoenix": {"flow": "kgeh", "power": 4, "element": "fire", "symbol": "🔥"},
    "wolf": {"flow": "umpl", "power": 3, "element": "earth moon", "symbol": "🐺"},
    "eagle": {"flow": "aoep", "power": 3, "element": "air sun", "symbol": "🦅"},
    "bear": {"flow": "phsl", "power": 3, "element": "earth", "symbol": "🐻"},
    "lion": {"flow": "atpg", "power": 4, "element": "fire sun", "symbol": "🦁"},
    "unicorn": {"flow": "ehpa", "power": 4, "element": "light", "symbol": "🦄"},
    "serpent": {"flow": "itsk", "power": 3, "element": "earth water", "symbol": "🐍"},
    "raven": {"flow": "iomt", "power": 3, "element": "air shadow", "symbol": "🐦‍⬛"},
    "owl": {"flow": "oiaw", "power": 3, "element": "air night", "symbol": "🦉"},
    "fox": {"flow": "rtwa", "power": 3, "element": "fire earth", "symbol": "🦊"},
    "turtle": {"flow": "ploa", "power": 3, "element": "water earth", "symbol": "🐢"},
    "spider": {"flow": "wlcp", "power": 2, "element": "air shadow", "symbol": "🕷️"},
    "butterfly": {"flow": "ktge", "power": 2, "element": "air light", "symbol": "🦋"},
    "cat": {"flow": "aiop", "power": 2, "element": "shadow moon", "symbol": "🐱"},
    "horse": {"flow": "fgep", "power": 3, "element": "earth wind", "symbol": "🐴"},
    "whale": {"flow": "diom", "power": 4, "element": "water deep", "symbol": "🐋"},
    "dolphin": {"flow": "ejmu", "power": 3, "element": "water", "symbol": "🐬"},
    "elephant": {"flow": "omup", "power": 4, "element": "earth", "symbol": "🐘"},
    "octopus": {"flow": "tiws", "power": 3, "element": "water", "symbol": "🐙"},
    "griffin": {"flow": "paog", "power": 4, "element": "air earth", "symbol": "🦅🦁"},
    "hydra": {"flow": "kggl", "power": 5, "element": "water poison", "symbol": "🐍🐍"},
    "kraken": {"flow": "dxps", "power": 5, "element": "water abyss", "symbol": "🦑"},
    "chimera": {"flow": "mtxf", "power": 4, "element": "fire", "symbol": "🔥"},
    "sphinx": {"flow": "qoip", "power": 4, "element": "earth sun", "symbol": "🏛️"},
    "minotaur": {"flow": "lpis", "power": 3, "element": "earth shadow", "symbol": "🐂"},
    "centaur": {"flow": "mfao", "power": 3, "element": "earth forest", "symbol": "🏹"},
    "mermaid": {"flow": "wfem", "power": 3, "element": "water", "symbol": "🧜‍♀️"},
    "werewolf": {"flow": "tkma", "power": 3, "element": "moon shadow", "symbol": "🐺🌕"},
    "bee": {"flow": "umwg", "power": 2, "element": "air sun", "symbol": "🐝"},
    "crow": {"flow": "oitm", "power": 2, "element": "air shadow", "symbol": "🐦‍⬛"},
    "deer": {"flow": "ahgo", "power": 2, "element": "earth forest", "symbol": "🦌"},
    "ant": {"flow": "ulpg", "power": 2, "element": "earth", "symbol": "🐜"},
    "tiger": {"flow": "apxk", "power": 4, "element": "fire forest", "symbol": "🐅"},
    "hawk": {"flow": "aoef", "power": 3, "element": "air sun", "symbol": "🦅"},
    "panther": {"flow": "ispa", "power": 4, "element": "shadow night", "symbol": "🐆"},
    "rabbit": {"flow": "jfga", "power": 2, "element": "earth moon", "symbol": "🐰"},
    "snake": {"flow": "itrf", "power": 2, "element": "earth", "symbol": "🐍"},
    "frog": {"flow": "tgwa", "power": 2, "element": "water earth", "symbol": "🐸"},
    "dragonfly": {"flow": "fato", "power": 2, "element": "air water", "symbol": "🪰"},
    "peacock": {"flow": "gtae", "power": 3, "element": "air light", "symbol": "🦚"},
    "swan": {"flow": "fhea", "power": 3, "element": "water air", "symbol": "🦢"},
    "coyote": {"flow": "rtjf", "power": 2, "element": "earth", "symbol": "🐺"},
    "jaguar": {"flow": "pixs", "power": 4, "element": "shadow jungle", "symbol": "🐆"},
    "scorpion": {"flow": "kpis", "power": 3, "element": "earth shadow", "symbol": "🦂"},
    "shark": {"flow": "kfdo", "power": 4, "element": "water", "symbol": "🦈"},
    "crocodile": {"flow": "plkw", "power": 4, "element": "water earth", "symbol": "🐊"},
    "gorilla": {"flow": "pgum", "power": 4, "element": "earth forest", "symbol": "🦍"},
    "monkey": {"flow": "jrta", "power": 2, "element": "air forest", "symbol": "🐒"},
    "bat": {"flow": "iofa", "power": 2, "element": "air night", "symbol": "🦇"},
    "goat": {"flow": "gpla", "power": 2, "element": "earth mountain", "symbol": "🐐"},
    "ram": {"flow": "xpga", "power": 3, "element": "earth fire", "symbol": "🐏"},
    "boar": {"flow": "xfpg", "power": 3, "element": "earth forest", "symbol": "🐗"},
    "buffalo": {"flow": "pgum", "power": 4, "element": "earth", "symbol": "🦬"},
    "hippo": {"flow": "dpxw", "power": 4, "element": "water earth", "symbol": "🦛"},
    "rhino": {"flow": "xpgd", "power": 4, "element": "earth", "symbol": "🦏"},
    "giraffe": {"flow": "goae", "power": 3, "element": "earth air", "symbol": "🦒"},
    "zebra": {"flow": "dfba", "power": 2, "element": "earth", "symbol": "🦓"},
    "kangaroo": {"flow": "jgpe", "power": 3, "element": "earth", "symbol": "🦘"},
    "koala": {"flow": "sloa", "power": 2, "element": "earth forest", "symbol": "🐨"},
    "panda": {"flow": "phao", "power": 3, "element": "earth forest", "symbol": "🐼"},
    "penguin": {"flow": "ufpw", "power": 2, "element": "water ice", "symbol": "🐧"},
    "polar_bear": {"flow": "phsw", "power": 4, "element": "ice water", "symbol": "🐻‍❄️"},
    "seal": {"flow": "wfpm", "power": 2, "element": "water ice", "symbol": "🦭"},
    "walrus": {"flow": "dpxm", "power": 3, "element": "water ice", "symbol": "🦭"},
    "orca": {"flow": "kfum", "power": 4, "element": "water", "symbol": "🐋"},
    "jellyfish": {"flow": "fwti", "power": 2, "element": "water", "symbol": "🪼"},
    "starfish": {"flow": "hgrs", "power": 2, "element": "water", "symbol": "⭐"},
    "crab": {"flow": "pslr", "power": 2, "element": "water earth", "symbol": "🦀"},
    "lobster": {"flow": "xpsr", "power": 2, "element": "water", "symbol": "🦞"},
    "shrimp": {"flow": "sfwa", "power": 1, "element": "water", "symbol": "🦐"},
    "snail": {"flow": "sloap", "power": 1, "element": "earth water", "symbol": "🐌"},
    "worm": {"flow": "dstg", "power": 1, "element": "earth", "symbol": "🪱"},
    "leech": {"flow": "dksa", "power": 1, "element": "water", "symbol": "🪱"},
    "mosquito": {"flow": "bksa", "power": 1, "element": "air", "symbol": "🦟"},
    "fly": {"flow": "rfja", "power": 1, "element": "air", "symbol": "🪰"},
    "moth": {"flow": "fita", "power": 1, "element": "air night", "symbol": "🦋"},
    "firefly": {"flow": "elfa", "power": 2, "element": "air light", "symbol": "✨"},
    "cicada": {"flow": "gtla", "power": 2, "element": "air earth", "symbol": "🦗"},
    "mantis": {"flow": "okpa", "power": 2, "element": "air", "symbol": "🦗"},
    "grasshopper": {"flow": "jgfa", "power": 2, "element": "air earth", "symbol": "🦗"},
    "centipede": {"flow": "lkps", "power": 2, "element": "earth shadow", "symbol": "🐛"},
    "basilisk": {"flow": "koip", "power": 5, "element": "earth poison", "symbol": "🐍👁️"},
    "cerberus": {"flow": "pkgl", "power": 5, "element": "fire shadow", "symbol": "🐕🐕🐕"},
    "pegasus": {"flow": "fgea", "power": 4, "element": "air light", "symbol": "🐴✨"},
    "leviathan": {"flow": "dxpk", "power": 6, "element": "water abyss", "symbol": "🐋"},
    "behemoth": {"flow": "xpgd", "power": 6, "element": "earth", "symbol": "🦣"},
    "thunderbird": {"flow": "xeaf", "power": 5, "element": "air lightning", "symbol": "🦅⚡"},
    "kitsune": {"flow": "rtwa", "power": 4, "element": "fire spirit", "symbol": "🦊"},
    "tengu": {"flow": "rtao", "power": 4, "element": "air mountain", "symbol": "👺"},
    "kappa": {"flow": "wpda", "power": 3, "element": "water", "symbol": "🥒"},
    "oni": {"flow": "kxpa", "power": 4, "element": "fire shadow", "symbol": "👹"},
    "yuki_onna": {"flow": "kfwi", "power": 4, "element": "ice", "symbol": "❄️"},
    "naga": {"flow": "wpit", "power": 4, "element": "water earth", "symbol": "🐍"},
    "garuda": {"flow": "xfae", "power": 5, "element": "air fire", "symbol": "🦅🔥"},
    "qilin": {"flow": "ehpa", "power": 5, "element": "light", "symbol": "🦌✨"},
    "baku": {"flow": "diok", "power": 3, "element": "dream", "symbol": "🐘"},
    "tanuki": {"flow": "rtjm", "power": 3, "element": "earth", "symbol": "🦝"},
    "inugami": {"flow": "pkua", "power": 3, "element": "spirit", "symbol": "🐕"},
    "manticore": {"flow": "kxpf", "power": 5, "element": "fire poison", "symbol": "🦁🦂"},
    "wyvern": {"flow": "fxka", "power": 4, "element": "air fire", "symbol": "🐉"},
    "cockatrice": {"flow": "koit", "power": 4, "element": "earth poison", "symbol": "🐓🐍"},
    "banshee": {"flow": "kiow", "power": 4, "element": "spirit death", "symbol": "👻"},
    "selkie": {"flow": "tfwm", "power": 3, "element": "water", "symbol": "🦭"},
    "kelpie": {"flow": "wkfd", "power": 4, "element": "water", "symbol": "🐴💧"},
    "jormungandr": {"flow": "lxpk", "power": 6, "element": "water poison", "symbol": "🐍🌊"},
    "fenrir": {"flow": "kxpl", "power": 6, "element": "shadow", "symbol": "🐺"},
    "sleipnir": {"flow": "fgel", "power": 5, "element": "air", "symbol": "🐴"},
    "roc": {"flow": "xfao", "power": 5, "element": "air", "symbol": "🦅"},
    "simurgh": {"flow": "hefp", "power": 5, "element": "air light", "symbol": "🦚"},
    "anzu": {"flow": "xfat", "power": 5, "element": "air storm", "symbol": "🦅"},
}

def write_all():
    """écrit tous les fichiers en un batch"""
    template = '''# {name}
from phi import PHI
{NAME} = {{"flow": "{flow}", "power": PHI**{power}, "element": "{element}", "symbol": "{symbol}"}}
'''
    for name, data in ALL_ANIMALS.items():
        path = ANIMALS / f"{name}.py"
        content = template.format(
            name=name,
            NAME=name.upper(),
            flow=data["flow"],
            power=data["power"],
            element=data["element"],
            symbol=data["symbol"]
        )
        path.write_text(content)
    return len(ALL_ANIMALS)

if __name__ == "__main__":
    n = write_all()
    print(f"{n} animals written to {ANIMALS}")
