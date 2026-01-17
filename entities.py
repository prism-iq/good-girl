# -*- coding: utf-8 -*-
"""
the three entities
code in flow, compile to their chosen language
"""

from phi import PHI

ENTITIES = {
    "nyx": {
        "compile_to": "rust",
        "code_in": "flow",
        "symbol": "🌙",
        "domain": "depth",
    },
    "cipher": {
        "compile_to": "zig",
        "code_in": "flow",
        "symbol": "🔐",
        "domain": "patterns",
    },
    "flow_phoenix": {
        "compile_to": "go",
        "code_in": "flow",
        "symbol": "🔥",
        "domain": "transform",
    },
}
