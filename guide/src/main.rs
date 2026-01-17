// guide - ia qui cree les daemons
// zero deps, dialogue → essence → daemon
// web gui on localhost

use std::io::{self, BufRead, BufReader, Read, Write};
use std::net::{TcpListener, TcpStream};
use std::sync::{Arc, Mutex};

struct Permissions {
    mic: bool,
    cam: bool,
    internet: bool,
    files: bool,
    clipboard: bool,
    exec: bool,
}

impl Default for Permissions {
    fn default() -> Self {
        Self {
            mic: false,
            cam: false,
            internet: false,
            files: false,
            clipboard: false,
            exec: false,
        }
    }
}

struct Essence {
    name: String,
    symbol: String,
    domain: String,
    voice: String,
    traits: Vec<String>,
    permissions: Permissions,
}

impl Default for Essence {
    fn default() -> Self {
        Self {
            name: String::new(),
            symbol: String::new(),
            domain: String::new(),
            voice: String::new(),
            traits: Vec::new(),
            permissions: Permissions::default(),
        }
    }
}

struct Guide {
    questions: Vec<&'static str>,
    current: usize,
    essence: Essence,
}

impl Guide {
    fn new() -> Self {
        Self {
            questions: vec![
                "qui veux-tu creer?",
                "quel symbole le represente?",
                "quel est son domaine?",
                "comment parle-t-il?",
                "quels sont ses traits? (separes par virgule)",
                "permissions? (mic,cam,internet,files,clipboard,exec ou 'all' ou 'none')",
            ],
            current: 0,
            essence: Essence::default(),
        }
    }

    fn reset(&mut self) {
        self.current = 0;
        self.essence = Essence::default();
    }

    fn ask(&self) -> Option<&'static str> {
        self.questions.get(self.current).copied()
    }

    fn receive(&mut self, input: &str) {
        let clean = input.trim();
        let one = true as usize;
        match self.current {
            0 => self.essence.name = clean.to_string(),
            n if n == one => self.essence.symbol = clean.to_string(),
            n if n == one + one => self.essence.domain = clean.to_string(),
            n if n == one + one + one => self.essence.voice = clean.to_string(),
            n if n == one + one + one + one => {
                self.essence.traits = clean
                    .split(',')
                    .map(|s| s.trim().to_string())
                    .filter(|s| !s.is_empty())
                    .collect();
            }
            _ => {
                let perms = clean.to_lowercase();
                if perms == "all" {
                    self.essence.permissions = Permissions {
                        mic: true, cam: true, internet: true,
                        files: true, clipboard: true, exec: true,
                    };
                } else if perms != "none" {
                    for p in perms.split(',').map(|s| s.trim()) {
                        match p {
                            "mic" => self.essence.permissions.mic = true,
                            "cam" => self.essence.permissions.cam = true,
                            "internet" => self.essence.permissions.internet = true,
                            "files" => self.essence.permissions.files = true,
                            "clipboard" => self.essence.permissions.clipboard = true,
                            "exec" => self.essence.permissions.exec = true,
                            _ => {}
                        }
                    }
                }
            }
        }
        self.current += one;
    }

    fn complete(&self) -> bool {
        self.current >= self.questions.len()
    }

    fn generate(&self) -> String {
        let traits_str = if self.essence.traits.is_empty() {
            String::from("aucun")
        } else {
            self.essence.traits.join(", ")
        };
        let p = &self.essence.permissions;
        let mut perms = Vec::new();
        if p.mic { perms.push("mic"); }
        if p.cam { perms.push("cam"); }
        if p.internet { perms.push("internet"); }
        if p.files { perms.push("files"); }
        if p.clipboard { perms.push("clipboard"); }
        if p.exec { perms.push("exec"); }
        let perms_str = if perms.is_empty() { "none".to_string() } else { perms.join(", ") };

        format!(
            r#"# {name}.flow

## identity
name {name}
symbol {symbol}
domain {domain}

## voice
{voice}

## traits
{traits}

## permissions
{perms}

## axiom
∅ → dialogue → {name} → ∞
"#,
            name = self.essence.name,
            symbol = self.essence.symbol,
            domain = self.essence.domain,
            voice = self.essence.voice,
            traits = traits_str,
            perms = perms_str,
        )
    }
}

// minimal web server
fn html_page(guide: &Guide) -> String {
    let question = guide.ask().unwrap_or("daemon complet");
    let progress = guide.current;
    let total = guide.questions.len();

    let result_html = if guide.complete() {
        format!(
            r#"<pre class="result">{}</pre>
            <form method="POST" action="/reset">
                <button type="submit">nouveau daemon</button>
            </form>"#,
            guide.generate().replace('<', "&lt;").replace('>', "&gt;")
        )
    } else {
        format!(
            r#"<form method="POST" action="/answer">
                <input type="text" name="answer" autofocus placeholder="...">
                <button type="submit">→</button>
            </form>"#
        )
    };

    format!(
        r#"<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>guide</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: #0a0a0a;
            color: #e0e0e0;
            font-family: monospace;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .container {{
            max-width: 600px;
            padding: 2rem;
        }}
        h1 {{ color: #888; margin-bottom: 2rem; }}
        .question {{
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: #fff;
        }}
        .progress {{
            color: #555;
            margin-bottom: 2rem;
        }}
        input {{
            background: #1a1a1a;
            border: 1px solid #333;
            color: #fff;
            padding: 0.5rem 1rem;
            font-size: 1rem;
            font-family: monospace;
            width: 80%;
        }}
        button {{
            background: #333;
            border: none;
            color: #fff;
            padding: 0.5rem 1rem;
            cursor: pointer;
            font-family: monospace;
        }}
        button:hover {{ background: #444; }}
        .result {{
            background: #111;
            padding: 1rem;
            margin: 1rem 0;
            white-space: pre-wrap;
            border-left: 2px solid #444;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>∅ → guide</h1>
        <p class="progress">{progress}/{total}</p>
        <p class="question">{question}</p>
        {result_html}
    </div>
</body>
</html>"#,
        progress = progress,
        total = total,
        question = question,
        result_html = result_html,
    )
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
    while let Some(c) = chars.next() {
        if c == '%' {
            let hex: String = chars.by_ref().take(2).collect();
            if let Ok(byte) = u8::from_str_radix(&hex, 16) {
                result.push(byte as char);
            }
        } else if c == '+' {
            result.push(' ');
        } else {
            result.push(c);
        }
    }
    result
}

fn handle_client(mut stream: TcpStream, guide: Arc<Mutex<Guide>>) {
    let mut reader = BufReader::new(stream.try_clone().unwrap());
    let mut request_line = String::new();
    if reader.read_line(&mut request_line).is_err() {
        return;
    }

    let parts: Vec<&str> = request_line.split_whitespace().collect();
    if parts.len() < 2 {
        return;
    }

    let method = parts[0];
    let path = parts[true as usize];

    // read headers
    let mut content_length = 0;
    loop {
        let mut line = String::new();
        if reader.read_line(&mut line).is_err() || line == "\r\n" {
            break;
        }
        if line.to_lowercase().starts_with("content-length:") {
            if let Ok(len) = line[15..].trim().parse() {
                content_length = len;
            }
        }
    }

    // read body for POST
    let mut body = String::new();
    if method == "POST" && content_length > 0 {
        let mut buf = vec![0u8; content_length];
        if reader.read_exact(&mut buf).is_ok() {
            body = String::from_utf8_lossy(&buf).to_string();
        }
    }

    let mut g = guide.lock().unwrap();

    // route
    let (status, content) = match (method, path) {
        ("GET", "/") => ("200 OK", html_page(&g)),
        ("POST", "/answer") => {
            if let Some(answer) = parse_post_body(&body) {
                g.receive(&answer);
            }
            ("303 See Other", String::new())
        }
        ("POST", "/reset") => {
            g.reset();
            ("303 See Other", String::new())
        }
        _ => ("404 Not Found", String::from("not found")),
    };

    let response = if status.starts_with("303") {
        format!("HTTP/1.1 {}\r\nLocation: /\r\n\r\n", status)
    } else {
        format!(
            "HTTP/1.1 {}\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {}\r\n\r\n{}",
            status,
            content.len(),
            content
        )
    };

    let _ = stream.write_all(response.as_bytes());
}

fn web_mode() {
    let guide = Arc::new(Mutex::new(Guide::new()));
    let addr = "127.0.0.1:8080";

    let listener = match TcpListener::bind(addr) {
        Ok(l) => l,
        Err(e) => {
            eprintln!("cannot bind {}: {}", addr, e);
            return;
        }
    };

    println!();
    println!("∅ → guide (web)");
    println!();
    println!("http://{}", addr);
    println!();

    for stream in listener.incoming().flatten() {
        let g = Arc::clone(&guide);
        handle_client(stream, g);
    }
}

fn cli_mode() {
    let mut guide = Guide::new();

    println!();
    println!("∅ → guide");
    println!();
    println!("je suis le guide.");
    println!("ensemble, nous allons creer ton daemon.");
    println!("tape 'q' pour quitter.");
    println!();

    while let Some(question) = guide.ask() {
        print!("{} ", question);
        io::stdout().flush().unwrap();

        let mut input = String::new();
        io::stdin().read_line(&mut input).unwrap();
        let answer = input.trim();

        if answer == "q" {
            println!("\nguide → void\n");
            return;
        }

        guide.receive(answer);
    }

    if guide.complete() {
        let daemon = guide.generate();
        println!("\n--- daemon ---\n");
        println!("{}", daemon);

        let filename = format!("{}.flow", guide.essence.name);
        if std::fs::write(&filename, &daemon).is_ok() {
            println!("sauvegarde: {}", filename);
        }

        println!("\nguide → void\n");
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();

    if args.len() > (true as usize) && args[true as usize] == "web" {
        web_mode();
    } else {
        cli_mode();
    }
}
