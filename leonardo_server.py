#!/usr/bin/env python3
"""
PANTHEON SERVER - API du système vivant unifié
Port 9600 (φ × 5932.67...)

Endpoints:
    /              - Interface web
    /status        - État du Panthéon
    /ask           - Demande à Leonardo (défaut)
    /validate      - Validation φ
    /prove         - Chemin de preuve
    /orchestrate   - Nyx orchestre
    /daemon/<name> - Demande à un daemon spécifique
    /dialogue      - Fait dialoguer deux daemons
    /council       - Réunit tous les daemons
    /teach         - Un daemon enseigne à un autre
    /simplex       - État du réseau Simplex
    /seal          - État du sceau post-quantique
"""
import json
import http.server
import socketserver
from pathlib import Path
from pantheon import pantheon, Leonardo, PHI, simplex, quantum_seal

PORT = 9600
leo = Leonardo()


class PantheonHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            html_path = Path(__file__).parent / 'leonardo_chat.html'
            if html_path.exists():
                with open(html_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b"<html><body><h1>Pantheon</h1></body></html>")

        elif self.path == '/status':
            self.send_json(pantheon.status())

        elif self.path == '/simplex':
            self.send_json(simplex.status())

        elif self.path == '/seal':
            self.send_json(quantum_seal.status())

        elif self.path.startswith('/daemon/'):
            daemon_name = self.path.split('/')[2]
            self.send_json({
                "daemon": daemon_name,
                "info": pantheon.status()["daemons"].get(daemon_name, {"error": "unknown"})
            })

        else:
            self.send_error(404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        try:
            data = json.loads(post_data)
        except:
            data = {"text": post_data}

        path = self.path

        if path == '/ask':
            text = data.get('text', '')
            response = leo.pense(text)
            self.send_json({"response": response})

        elif path == '/validate':
            text = data.get('text', '')
            domain = data.get('domain', 'default')
            v = leo.validate(text, domain)
            self.send_json(v)

        elif path == '/prove':
            text = data.get('text', '')
            response = leo.pense(f"Comment prouver: {text}")
            self.send_json({
                "hypothesis": text,
                "response": response,
                "phi_r": PHI
            })

        elif path == '/orchestrate':
            task = data.get('text', data.get('task', ''))
            results = pantheon.orchestrate(task)
            self.send_json(results)

        elif path.startswith('/daemon/'):
            daemon_name = path.split('/')[2]
            text = data.get('text', '')
            response = pantheon.ask(daemon_name, text)
            self.send_json({
                "daemon": daemon_name,
                "response": response
            })

        elif path == '/dialogue':
            daemon_a = data.get('daemon_a', data.get('d1', 'leonardo'))
            daemon_b = data.get('daemon_b', data.get('d2', 'nyx'))
            topic = data.get('topic', data.get('text', ''))
            turns = data.get('turns', 3)
            conversation = pantheon.dialogue(daemon_a, daemon_b, topic, turns)
            self.send_json({
                "participants": [daemon_a, daemon_b],
                "topic": topic,
                "conversation": conversation
            })

        elif path == '/council':
            question = data.get('question', data.get('text', ''))
            results = pantheon.council(question)
            self.send_json(results)

        elif path == '/teach':
            teacher = data.get('teacher', 'leonardo')
            student = data.get('student', 'zoe')
            topic = data.get('topic', data.get('text', ''))
            result = pantheon.teach(teacher, student, topic)
            self.send_json(result)

        else:
            self.send_error(404)

    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        pass  # Silent


if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), PantheonHandler) as httpd:
        print(f"φ Pantheon server on http://localhost:{PORT}")
        print(f"  Daemons: φ Leonardo | ☽ Nyx | ✧ Zoe | ✨ Clochette | ♪ Euterpe | 👁 Omniscient")
        print(f"  Simplex: {len(simplex.channels)} canaux sécurisés")
        print(f"  Post-Quantique: SHA3 + SHAKE256 + φ-hash + Merkle")
        httpd.serve_forever()
