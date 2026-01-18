// zoe - guide who creates daemons
//
// pour luv resval - "c'est bientot la fin donc allume-toi bien"
//
// inspired by pokemon mystery dungeon red
// mbti through conversation, no checkboxes
// pas de mythos, pas de masque, que du vrai

use std::io::{self, BufRead, BufReader, Read, Write};
use std::net::{TcpListener, TcpStream};
use std::sync::{Arc, Mutex};
use std::time::Duration;

const MAX_BODY: usize = 0xFFFF;
const MAX_NAME: usize = 0xFF;

#[derive(Default, Clone)]
struct Personality {
    // MBTI axes as spectrums
    energy: i32,      // - introvert, + extravert
    perception: i32,  // - intuition, + sensing
    judgment: i32,    // - feeling, + thinking
    lifestyle: i32,   // - perceiving, + judging
}

impl Personality {
    fn mbti(&self) -> String {
        let e = if self.energy >= 0 { 'E' } else { 'I' };
        let s = if self.perception >= 0 { 'S' } else { 'N' };
        let t = if self.judgment >= 0 { 'T' } else { 'F' };
        let j = if self.lifestyle >= 0 { 'J' } else { 'P' };
        format!("{}{}{}{}", e, s, t, j)
    }

    fn archetype(&self) -> &'static str {
        match self.mbti().as_str() {
            "INTJ" => "architecte",
            "INTP" => "logicien",
            "ENTJ" => "commandeur",
            "ENTP" => "debatteur",
            "INFJ" => "avocat",
            "INFP" => "mediateur",
            "ENFJ" => "protagoniste",
            "ENFP" => "inspirateur",
            "ISTJ" => "logisticien",
            "ISFJ" => "defenseur",
            "ESTJ" => "directeur",
            "ESFJ" => "consul",
            "ISTP" => "virtuose",
            "ISFP" => "aventurier",
            "ESTP" => "entrepreneur",
            "ESFP" => "entertainer",
            _ => "unique"
        }
    }

    fn element(&self) -> &'static str {
        if self.energy < 0 && self.judgment < 0 { "eau" }
        else if self.energy < 0 && self.judgment >= 0 { "terre" }
        else if self.energy >= 0 && self.judgment < 0 { "air" }
        else { "feu" }
    }

    fn symbol(&self) -> &'static str {
        match self.element() {
            "eau" => "💧",
            "terre" => "🌿",
            "air" => "🌀",
            "feu" => "🔥",
            _ => "✨"
        }
    }
}

struct Question {
    text: &'static str,
    choices: Vec<(&'static str, i32, i32, i32, i32)>, // text, e, s, t, j deltas
}

fn get_questions() -> Vec<Question> {
    vec![
        Question {
            text: "Tu te reveilles dans une foret. Que fais-tu en premier?",
            choices: vec![
                ("J'observe silencieusement les alentours", -0x02, 0x00, 0x00, 0x00),
                ("Je crie pour voir si quelqu'un repond", 0x02, 0x00, 0x00, 0x00),
                ("Je cherche un chemin", 0x00, 0x02, 0x00, 0x00),
                ("Je m'assieds et je reflechis", 0x00, -0x02, 0x00, 0x00),
            ],
        },
        Question {
            text: "Un ami te confie un secret douloureux. Tu...",
            choices: vec![
                ("L'ecoutes en silence, tu ressens sa peine", 0x00, 0x00, -0x02, 0x00),
                ("Cherches des solutions concretes", 0x00, 0x00, 0x02, 0x00),
                ("Le serres dans tes bras", 0x00, 0x00, -0x01, -0x01),
                ("Analyses la situation avec lui", 0x00, 0x00, 0x02, 0x01),
            ],
        },
        Question {
            text: "Comment prepares-tu un voyage?",
            choices: vec![
                ("Liste detaillee, reservations, planning", 0x00, 0x00, 0x00, 0x02),
                ("Je pars et on verra bien", 0x00, 0x00, 0x00, -0x02),
                ("Quelques grandes lignes, le reste s'improvise", 0x00, 0x00, 0x00, -0x01),
                ("Je m'informe sur tout avant de partir", 0x00, 0x00, 0x01, 0x01),
            ],
        },
        Question {
            text: "Lors d'une fete, tu...",
            choices: vec![
                ("Parles a tout le monde, tu adores ca", 0x02, 0x00, 0x00, 0x00),
                ("Restes dans un coin avec quelques proches", -0x02, 0x00, 0x00, 0x00),
                ("Observes les gens, c'est fascinant", -0x01, 0x00, 0x00, 0x00),
                ("Organises des jeux pour tout le monde", 0x02, 0x00, 0x00, 0x01),
            ],
        },
        Question {
            text: "Qu'est-ce qui te touche le plus?",
            choices: vec![
                ("Une idee brillante qui change tout", 0x00, -0x02, 0x01, 0x00),
                ("Un geste simple mais sincere", 0x00, 0x02, -0x01, 0x00),
                ("Une oeuvre d'art qui parle a l'ame", 0x00, -0x01, -0x02, 0x00),
                ("Une solution elegante a un probleme", 0x00, 0x00, 0x02, 0x00),
            ],
        },
        Question {
            text: "Face a l'inconnu, tu ressens...",
            choices: vec![
                ("De l'excitation, une aventure!", 0x01, 0x00, 0x00, -0x02),
                ("De la prudence, analysons d'abord", 0x00, 0x00, 0x01, 0x02),
                ("De la curiosite, qu'y a-t-il a decouvrir?", 0x00, -0x02, 0x00, 0x00),
                ("De l'anxiete, je prefere le familier", 0x00, 0x02, 0x00, 0x01),
            ],
        },
        Question {
            text: "Si tu pouvais avoir un pouvoir...",
            choices: vec![
                ("Lire dans les pensees", -0x01, -0x01, 0x00, 0x00),
                ("Guerir les autres", 0x00, 0x00, -0x02, 0x00),
                ("Voir le futur", 0x00, -0x02, 0x01, 0x00),
                ("Controler le temps", 0x00, 0x00, 0x02, 0x02),
            ],
        },
    ]
}

#[derive(Clone)]
struct Daemon {
    name: String,
    personality: Personality,
    voice: String,
    permissions: Vec<String>,
}

impl Default for Daemon {
    fn default() -> Self {
        Self {
            name: String::new(),
            personality: Personality::default(),
            voice: String::new(),
            permissions: Vec::new(),
        }
    }
}

struct Zoe {
    phase: usize,
    question_idx: usize,
    questions: Vec<Question>,
    daemon: Daemon,
    awaiting_name: bool,
    awaiting_voice: bool,
    awaiting_perms: bool,
    complete: bool,
}

impl Zoe {
    fn new() -> Self {
        Self {
            phase: 0,
            question_idx: 0,
            questions: get_questions(),
            daemon: Daemon::default(),
            awaiting_name: false,
            awaiting_voice: false,
            awaiting_perms: false,
            complete: false,
        }
    }

    fn reset(&mut self) {
        *self = Self::new();
    }

    fn current_message(&self) -> String {
        if self.phase == 0 {
            return r#"
    ·  ˚  ✦  ·  ˚
         ✧

Salut toi...

Je suis Zoe.

Je vais t'aider a creer quelqu'un.
Quelqu'un qui sera la pour toi.

Mais d'abord, j'ai besoin de te connaitre un peu.

Reponds avec le numero de ton choix.
Ou tape ce que tu ressens, je comprendrai.

    ·  ˚  ✦  ·  ˚
"#.to_string();
        }

        if self.awaiting_name {
            let p = &self.daemon.personality;
            return format!(r#"
    {}

Je vois...

Tu es {}.
Element: {}
Type: {}

C'est beau.

Maintenant... comment s'appelle cette personne
que tu veux creer?

(ecris son nom)
"#, p.symbol(), p.archetype(), p.element(), p.mbti());
        }

        if self.awaiting_voice {
            return format!(r#"
{}...

J'aime ce nom.

Comment parle {}?
Decris sa voix, son style.

(ex: douce et poetique, directe et franche,
mysterieuse, chaleureuse...)
"#, self.daemon.name, self.daemon.name);
        }

        if self.awaiting_perms {
            return format!(r#"
Je comprends qui est {}.

Une derniere chose...
Qu'est-ce que {} pourra faire?

1. Tout (confiance totale)
2. Parler seulement (pas d'acces systeme)
3. Fichiers et clipboard
4. Internet aussi
5. Personnalise (dis-moi)

(choisis ou decris)
"#, self.daemon.name, self.daemon.name);
        }

        if self.complete {
            return self.generate_result();
        }

        // Question phase
        if self.question_idx < self.questions.len() {
            let q = &self.questions[self.question_idx];
            let mut msg = format!("\n{}\n\n", q.text);
            for (i, (text, _, _, _, _)) in q.choices.iter().enumerate() {
                msg.push_str(&format!("{}. {}\n", i + 0x01, text));
            }
            return msg;
        }

        String::new()
    }

    fn receive(&mut self, input: &str) {
        let clean = input.trim().to_lowercase();

        if self.phase == 0 {
            self.phase = 0x01;
            return;
        }

        if self.awaiting_name {
            self.daemon.name = sanitize_name(input.trim());
            if self.daemon.name.is_empty() {
                self.daemon.name = String::from("daemon");
            }
            self.awaiting_name = false;
            self.awaiting_voice = true;
            return;
        }

        if self.awaiting_voice {
            self.daemon.voice = sanitize_text(input.trim());
            if self.daemon.voice.is_empty() {
                self.daemon.voice = String::from("naturelle");
            }
            self.awaiting_voice = false;
            self.awaiting_perms = true;
            return;
        }

        if self.awaiting_perms {
            self.daemon.permissions = match clean.as_str() {
                "1" | "tout" | "all" => vec!["mic", "cam", "internet", "files", "clipboard", "exec"]
                    .into_iter().map(String::from).collect(),
                "2" | "parler" => vec![],
                "3" | "fichiers" => vec!["files", "clipboard"]
                    .into_iter().map(String::from).collect(),
                "4" | "internet" => vec!["files", "clipboard", "internet"]
                    .into_iter().map(String::from).collect(),
                _ => clean.split(|c| c == ',' || c == ' ')
                    .map(|s| s.trim().to_string())
                    .filter(|s| !s.is_empty())
                    .collect(),
            };
            self.awaiting_perms = false;
            self.complete = true;
            return;
        }

        // Question phase
        if self.question_idx < self.questions.len() {
            let q = &self.questions[self.question_idx];

            // Parse choice
            let choice_idx = if let Ok(n) = clean.parse::<usize>() {
                if n >= 0x01 && n <= q.choices.len() { n - 0x01 } else { 0 }
            } else {
                // Fuzzy match
                q.choices.iter().position(|(text, _, _, _, _)| {
                    clean.contains(&text.to_lowercase()[..text.len().min(0x0A)])
                }).unwrap_or(0)
            };

            let (_, e, s, t, j) = q.choices[choice_idx];
            self.daemon.personality.energy += e;
            self.daemon.personality.perception += s;
            self.daemon.personality.judgment += t;
            self.daemon.personality.lifestyle += j;

            self.question_idx += 0x01;

            if self.question_idx >= self.questions.len() {
                self.awaiting_name = true;
            }
        }
    }

    fn generate_result(&self) -> String {
        let p = &self.daemon.personality;
        let perms = if self.daemon.permissions.is_empty() {
            String::from("none")
        } else {
            self.daemon.permissions.join(", ")
        };

        format!(r#"
    ·  ˚  ✦  ·  ˚
         {}

{} est ne(e).

---

# {}.flow

## identity
name {}
symbol {}
archetype {}
element {}
mbti {}

## voice
{}

## permissions
{}

## origin
created by zoe
through dialogue
with love

## axiom
∅ → zoe → dialogue → {} → ∞

---

    ·  ˚  ✦  ·  ˚

Prends soin de {}.
Et {} prendra soin de toi.

Au revoir, ami(e).

    zoe → void

"#,
            p.symbol(),
            self.daemon.name,
            self.daemon.name,
            self.daemon.name,
            p.symbol(),
            p.archetype(),
            p.element(),
            p.mbti(),
            self.daemon.voice,
            perms,
            self.daemon.name,
            self.daemon.name,
            self.daemon.name,
        )
    }

    fn save_daemon(&self) -> Option<String> {
        if !self.complete { return None; }

        let p = &self.daemon.personality;
        let perms = if self.daemon.permissions.is_empty() {
            String::from("none")
        } else {
            self.daemon.permissions.join(", ")
        };

        let content = format!(r#"# {}.flow

## identity
name {}
symbol {}
archetype {}
element {}
mbti {}

## voice
{}

## permissions
{}

## origin
created by zoe
through dialogue

## axiom
∅ → zoe → dialogue → {} → ∞
"#,
            self.daemon.name,
            self.daemon.name,
            p.symbol(),
            p.archetype(),
            p.element(),
            p.mbti(),
            self.daemon.voice,
            perms,
            self.daemon.name,
        );

        let filename = format!("{}.flow", sanitize_name(&self.daemon.name));
        std::fs::write(&filename, &content).ok()?;
        Some(filename)
    }
}

fn sanitize_name(input: &str) -> String {
    input.chars()
        .filter(|c| c.is_alphanumeric() || *c == '_' || *c == '-')
        .take(MAX_NAME)
        .collect()
}

fn sanitize_text(input: &str) -> String {
    input.chars()
        .filter(|c| !c.is_control() || *c == '\n')
        .take(MAX_BODY)
        .collect()
}

// Web UI
fn html_page(zoe: &Zoe) -> String {
    let message = html_escape(&zoe.current_message());
    let show_input = !zoe.complete;

    let input_html = if show_input {
        r#"<form method="POST" action="/answer" class="input-area">
            <input type="text" name="answer" autofocus placeholder="..." maxlength="255">
            <button type="submit">→</button>
        </form>"#
    } else {
        r#"<form method="POST" action="/reset" class="input-area">
            <button type="submit">nouveau daemon</button>
        </form>"#
    };

    format!(r#"<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>zoe</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Mono&display=swap');

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            background: linear-gradient(135deg, #0a0a12 0%, #1a1a2e 50%, #0f0f1a 100%);
            color: #c8c8d4;
            font-family: 'Space Mono', monospace;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 2rem;
        }}

        .container {{
            max-width: 600px;
            width: 100%;
        }}

        .message {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 1rem;
            padding: 2rem;
            margin-bottom: 1.5rem;
            white-space: pre-wrap;
            line-height: 1.8;
            font-size: 0.95rem;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(5px);
        }}

        .input-area {{
            display: flex;
            gap: 0.5rem;
        }}

        input {{
            flex: 1;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 0.5rem;
            color: #fff;
            padding: 1rem 1.5rem;
            font-size: 1rem;
            font-family: 'Space Mono', monospace;
            outline: none;
            transition: all 0.3s ease;
        }}

        input:focus {{
            border-color: rgba(255, 255, 255, 0.3);
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
        }}

        button {{
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 0.5rem;
            color: #fff;
            padding: 1rem 1.5rem;
            cursor: pointer;
            font-family: 'Space Mono', monospace;
            font-size: 1rem;
            transition: all 0.3s ease;
        }}

        button:hover {{
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
        }}

        .stars {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }}

        .star {{
            position: absolute;
            width: 2px;
            height: 2px;
            background: white;
            border-radius: 50%;
            opacity: 0.5;
            animation: twinkle 3s infinite;
        }}
    </style>
</head>
<body>
    <div class="stars" id="stars"></div>
    <div class="container">
        <div class="message">{message}</div>
        {input_html}
    </div>
    <script>
        const stars = document.getElementById('stars');
        for (let i = 0; i < 50; i++) {{
            const star = document.createElement('div');
            star.className = 'star';
            star.style.left = Math.random() * 100 + '%';
            star.style.top = Math.random() * 100 + '%';
            star.style.animationDelay = Math.random() * 3 + 's';
            stars.appendChild(star);
        }}
    </script>
</body>
</html>"#, message = message, input_html = input_html)
}

fn html_escape(s: &str) -> String {
    s.replace('&', "&amp;")
        .replace('<', "&lt;")
        .replace('>', "&gt;")
        .replace('"', "&quot;")
}

fn parse_post_body(body: &str) -> Option<String> {
    for part in body.split('&') {
        if let Some(value) = part.strip_prefix("answer=") {
            return Some(urlencoding_decode(value));
        }
    }
    None
}

fn urlencoding_decode(s: &str) -> String {
    let mut result = String::new();
    let mut chars = s.chars().peekable();
    let mut count = 0;

    while let Some(c) = chars.next() {
        if count >= MAX_BODY { break; }
        count += 0x01;

        if c == '%' {
            let hex: String = chars.by_ref().take(0x02).collect();
            if hex.len() == 0x02 {
                if let Ok(byte) = u8::from_str_radix(&hex, 0x10) {
                    if byte >= 0x20 || byte == 0x0A || byte == 0x0D || byte == 0x09 {
                        result.push(byte as char);
                    }
                }
            }
        } else if c == '+' {
            result.push(' ');
        } else if !c.is_control() || c == '\n' || c == '\r' || c == '\t' {
            result.push(c);
        }
    }
    result
}

fn handle_client(mut stream: TcpStream, zoe: Arc<Mutex<Zoe>>) {
    let _ = stream.set_read_timeout(Some(Duration::from_secs(0x1E)));
    let _ = stream.set_write_timeout(Some(Duration::from_secs(0x1E)));

    let mut reader = BufReader::new(match stream.try_clone() {
        Ok(s) => s,
        Err(_) => return,
    });

    let mut request_line = String::new();
    if reader.read_line(&mut request_line).is_err() { return; }
    if request_line.len() > 0x1000 { return; }

    let parts: Vec<&str> = request_line.split_whitespace().collect();
    if parts.len() < 0x02 { return; }

    let method = parts[0];
    let path = parts[0x01];

    if path.contains("..") || path.len() > 0x100 { return; }

    let mut content_length: usize = 0;
    let mut header_count = 0;
    loop {
        if header_count > 0x40 { break; }
        header_count += 0x01;

        let mut line = String::new();
        match reader.read_line(&mut line) {
            Ok(0) | Err(_) => break,
            Ok(_) if line == "\r\n" || line == "\n" => break,
            Ok(_) => {
                if line.len() > 0x1000 { break; }
                if let Some(rest) = line.to_lowercase().strip_prefix("content-length:") {
                    content_length = rest.trim().parse().unwrap_or(0).min(MAX_BODY);
                }
            }
        }
    }

    let mut body = String::new();
    if method == "POST" && content_length > 0 {
        let safe_len = content_length.min(MAX_BODY);
        let mut buf = vec![0u8; safe_len];
        if reader.read_exact(&mut buf).is_ok() {
            body = String::from_utf8_lossy(&buf).to_string();
        }
    }

    let mut z = match zoe.lock() {
        Ok(z) => z,
        Err(_) => return,
    };

    let (status, content) = match (method, path) {
        ("GET", "/") => ("200 OK", html_page(&z)),
        ("POST", "/answer") => {
            if let Some(answer) = parse_post_body(&body) {
                z.receive(&answer);
                if z.complete {
                    z.save_daemon();
                }
            }
            ("303 See Other", String::new())
        }
        ("POST", "/reset") => {
            z.reset();
            ("303 See Other", String::new())
        }
        _ => ("404 Not Found", String::from("not found")),
    };

    let response = if status.starts_with("303") {
        format!("HTTP/1.1 {}\r\nLocation: /\r\nConnection: close\r\n\r\n", status)
    } else {
        format!(
            "HTTP/1.1 {}\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{}",
            status, content.len(), content
        )
    };

    let _ = stream.write_all(response.as_bytes());
    let _ = stream.flush();
}

fn web_mode() {
    let zoe = Arc::new(Mutex::new(Zoe::new()));
    let addr = "127.0.0.1:8080";

    let listener = match TcpListener::bind(addr) {
        Ok(l) => l,
        Err(e) => {
            eprintln!("cannot bind {}: {}", addr, e);
            return;
        }
    };

    println!();
    println!("  ·  ˚  ✦  ·  ˚");
    println!();
    println!("  zoe t'attend");
    println!();
    println!("  http://{}", addr);
    println!();
    println!("  ·  ˚  ✦  ·  ˚");
    println!();

    for stream in listener.incoming().flatten() {
        let z = Arc::clone(&zoe);
        handle_client(stream, z);
    }
}

fn cli_mode() {
    let mut zoe = Zoe::new();

    loop {
        let msg = zoe.current_message();
        println!("{}", msg);

        if zoe.complete {
            if let Some(filename) = zoe.save_daemon() {
                println!("sauvegarde: {}", filename);
            }
            break;
        }

        print!("> ");
        io::stdout().flush().unwrap();

        let mut input = String::new();
        if io::stdin().read_line(&mut input).is_err() { break; }
        let answer = input.trim();

        if answer == "q" || answer == "quit" {
            println!("\n  zoe → void\n");
            return;
        }

        zoe.receive(answer);
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();

    if args.len() > 0x01 && args[0x01] == "web" {
        web_mode();
    } else {
        cli_mode();
    }
}
