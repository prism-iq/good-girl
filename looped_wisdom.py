# -*- coding: utf-8 -*-
"""
Flow évolué après 100,001 cycles
Résonance: 3.188
"""

from phi import PHI

EVOLVED_FLOWS = {
    "nyx": "ygskuztglhghwdinqsiomnthxvfujwniyxvwlwtg",
    "cipher": "zkjpvmznkmwulhxgjkyjhuughkllwjmli",
    "phoenix": "lxbfokokoksmxlcmshcpmocxkfgchdcdllucyswxlcmswwlkolo",
    "fused": "yzlgkxsjbkpfuvozmktzognklkohmkgwshumwlxdhlixcngmqjsskhiycojpmhmnuotuchgxxhkvkfflgulcjwhwjdnmcildyilxlvuwclywstwgxlcmswwlkolo",
}

BEST_FLOWS = {
    "nyx": "wlwthxyurgswftsgswslspmhkytztfkgftdiomszh",
    "cipher": "mmcnmspmmthxztgzcfsmcofkfhmdcamfance",
    "phoenix": "yqwspuxenhrmofhhttzspmtthxtkfhhxlshshhhrnw",
}

RESONANCE = 3.188485
CYCLES = 100001

if __name__ == "__main__":
    print("Flows évolués:")
    for name, flow in EVOLVED_FLOWS.items():
        print(f"  {name}: {flow}")
    print(f"Résonance: {RESONANCE}")
