#!/usr/bin/env python3
"""
TALK - Interface CLI pour le Panthéon
Parle aux daemons directement

Usage:
    python talk.py                    # Mode interactif
    python talk.py message            # One-shot à Leonardo
    python talk.py @nyx message       # One-shot à un daemon spécifique
    python talk.py !flow texte        # Interprète Flow
"""
import requests
import sys
import json

URL = "http://localhost:9600"

SYMBOLS = {
    "leonardo": "φ",
    "nyx": "☽",
    "zoe": "✧",
    "clochette": "✨",
    "euterpe": "♪",
    "omniscient": "👁",
}


def ask(question: str, daemon: str = "leonardo") -> str:
    """Pose une question à un daemon"""
    try:
        if daemon == "leonardo":
            r = requests.post(f"{URL}/ask", json={"text": question}, timeout=30)
        else:
            r = requests.post(f"{URL}/daemon/{daemon}", json={"text": question}, timeout=30)
        data = r.json()
        return data.get("response", str(data))
    except Exception as e:
        return f"Erreur: {e}"


def validate(hypothesis: str, domain: str = "default") -> dict:
    """Valide une hypothèse avec φ"""
    try:
        r = requests.post(f"{URL}/validate", json={"text": hypothesis, "domain": domain}, timeout=30)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def orchestrate(task: str) -> dict:
    """Nyx orchestre une tâche"""
    try:
        r = requests.post(f"{URL}/orchestrate", json={"text": task}, timeout=30)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def status() -> dict:
    """État du Panthéon"""
    try:
        r = requests.get(f"{URL}/status", timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def flow(text: str) -> dict:
    """Interprète du Flow language"""
    # Import local pour éviter dépendance circulaire
    try:
        from pantheon import interpret_flow
        return interpret_flow(text)
    except ImportError:
        return {"error": "pantheon.py non trouvé"}


def print_response(daemon: str, response: str):
    """Affiche une réponse formatée"""
    symbol = SYMBOLS.get(daemon, "?")
    print(f"\n{symbol} [{daemon}]\n{response}\n")


def interactive():
    """Mode interactif"""
    print("""
╭─────────────────────────────────────────────────────────────────╮
│  TALK - Interface Panthéon                                      │
│                                                                 │
│  φ Leonardo | ☽ Nyx | ✧ Zoe | ✨ Clochette | ♪ Euterpe | 👁 Omniscient │
╰─────────────────────────────────────────────────────────────────╯

Commandes:
  message          → Parle à Leonardo
  @daemon message  → Parle à un daemon (@nyx, @zoe, @clochette, @euterpe, @omniscient)
  !flow texte      → Interprète du Flow
  !orch tâche      → Nyx orchestre
  !valid texte     → Valide avec φ
  status           → État du Panthéon
  quit             → Quitter
""")

    while True:
        try:
            inp = input(">>> ").strip()
            if not inp:
                continue

            if inp in ["quit", "exit", "q"]:
                print("\n☽ Arrivederci.")
                break

            if inp == "status":
                s = status()
                if "error" not in s:
                    print(f"\nPanthéon: {'vivant' if s.get('alive') else 'endormi'}")
                    print(f"Heartbeat: {s.get('heartbeat', '?')}")
                    print(f"φ = {s.get('phi', '?')}")
                    print(f"Messages bus: {s.get('bus_messages', 0)}")
                    print("\nDaemons:")
                    for name, d in s.get("daemons", {}).items():
                        symbol = d.get("symbol", "?")
                        beats = d.get("heartbeats", 0)
                        print(f"  {symbol} {name}: {beats} heartbeats")
                else:
                    print(f"\nErreur: {s['error']}")
                print()
                continue

            if inp.startswith("@"):
                parts = inp[1:].split(" ", 1)
                daemon = parts[0]
                query = parts[1] if len(parts) > 1 else ""
                response = ask(query, daemon)
                print_response(daemon, response)

            elif inp.startswith("!flow"):
                text = inp[5:].strip()
                result = flow(text)
                print(f"\n{json.dumps(result, indent=2, ensure_ascii=False)}\n")

            elif inp.startswith("!orch"):
                task = inp[5:].strip()
                results = orchestrate(task)
                for daemon, resp in results.items():
                    print_response(daemon, resp)

            elif inp.startswith("!valid"):
                text = inp[6:].strip()
                v = validate(text)
                symbol = v.get("symbol", "?")
                phi_r = v.get("phi_r", 0)
                sacred = v.get("sacred", False)
                print(f"\n{symbol} φ_r = {phi_r}")
                if sacred:
                    print("✧ Fibonacci détecté!")
                print(f"Hash: {v.get('hash', '?')}\n")

            else:
                response = ask(inp)
                print_response("leonardo", response)

        except (KeyboardInterrupt, EOFError):
            print("\n☽ Arrivederci.")
            break
        except Exception as e:
            print(f"\nErreur: {e}\n")


def main():
    if len(sys.argv) < 2:
        interactive()
    else:
        args = " ".join(sys.argv[1:])

        if args.startswith("@"):
            parts = args[1:].split(" ", 1)
            daemon = parts[0]
            query = parts[1] if len(parts) > 1 else ""
            print(ask(query, daemon))
        elif args.startswith("!flow"):
            text = args[5:].strip()
            print(json.dumps(flow(text), indent=2, ensure_ascii=False))
        elif args == "status":
            print(json.dumps(status(), indent=2, ensure_ascii=False))
        else:
            print(ask(args))


if __name__ == "__main__":
    main()
