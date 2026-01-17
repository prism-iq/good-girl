#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
good-girl main entry
run as daemon or interactive
"""

import sys
from girl import GIRL, think, speak, compile, evolve
from phi import PHI
from flow import AXIOM, TARGETS
from sources import DOMAINS, KNOWLEDGE
from axioms import AXIOMS
from l import daemon, immortal

def interactive():
    """interactive mode"""
    print(f"good-girl v1.0.0")
    print(f"φ = {PHI}")
    print(f"axiom: {AXIOM}")
    print(f"domains: {len(DOMAINS)} | vocab: {len(GIRL.vocabulary)} | targets: {len(TARGETS)}")
    print("type 'exit' to quit\n")

    while True:
        try:
            line = input("flow> ").strip()
            if not line:
                continue
            if line == "exit":
                break

            # commands
            if line.startswith("/"):
                cmd = line[1:].split()[0]
                arg = line[len(cmd)+2:].strip() if len(line) > len(cmd)+1 else ""

                if cmd == "think":
                    print(think(arg))
                elif cmd == "speak":
                    print(speak(arg))
                elif cmd == "compile":
                    parts = arg.split(" to ")
                    if len(parts) == 2:
                        print(compile(parts[0], parts[1]))
                    else:
                        print(compile(arg, "python"))
                elif cmd == "evolve":
                    print(evolve(arg, 10))
                elif cmd == "axioms":
                    for i, a in AXIOMS.items():
                        print(f"{i}. {a['name']}: {a['truth']}")
                elif cmd == "domains":
                    print(", ".join(DOMAINS))
                elif cmd == "knowledge":
                    for k, v in KNOWLEDGE.items():
                        print(f"  {k}: {v}")
                else:
                    print(f"unknown command: {cmd}")
            else:
                # default: parse as flow
                print(speak(line))

        except KeyboardInterrupt:
            print("\n")
            continue
        except EOFError:
            break
        except Exception as e:
            print(f"error: {e}")

def run_daemon():
    """run as immortal daemon"""
    print("starting daemon...")
    immortal()

    def tick():
        pass  # silent heartbeat

    daemon(tick, interval=1.0)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "daemon":
        run_daemon()
    else:
        interactive()
