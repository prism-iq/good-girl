// guide - ia qui cree les daemons
// zero deps, dialogue → essence → daemon
// web gui on localhost

use std::io::{self, BufRead, BufReader, Read, Write};
use std::net::{TcpListener, TcpStream};
use std::sync::{Arc, Mutex};
use std::time::Duration;

const MAX_BODY: usize = 0xFFFF; // 64KB max
const MAX_NAME: usize = 0xFF;   // 255 chars max

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

fn sanitize_name(input: &str) -> String {
    input
        .chars()
        .filter(|c| c.is_alphanumeric() || *c == '_' || *c == '-')
        .take(MAX_NAME)
        .collect()
}

fn sanitize_text(input: &str) -> String {
    input
        .chars()
        .filter(|c| !c.is_control() || *c == '\n')
        .take(MAX_BODY)
        .collect()
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
        let clean = sanitize_text(input.trim());
        let one = true as usize;
        match self.current {
            0 => self.essence.name = sanitize_name(&clean),
            n if n == one => self.essence.symbol = clean.chars().take(0x10).collect(),
            n if n == one + one => self.essence.domain = clean,
            n if n == one + one + one => self.essence.voice = clean,
            n if n == one + one + one + one => {
                self.essence.traits = clean
                    .split(',')
                    .map(|s| sanitize_text(s.trim()))
                    .filter(|s| !s.is_empty())
                    .take(0x10)
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
                    for p in perms.split(',').map(|s| s.trim()).take(0x10) {
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

    fn safe_filename(&self) -> String {
        let name = sanitize_name(&self.essence.name);
        if name.is_empty() {
            String::from("daemon")
        } else {
            name
        }
    }
}

fn html_escape(s: &str) -> String {
    s.replace('&', "&amp;")
        .replace('<', "&lt;")
        .replace('>', "&gt;")
        .replace('"', "&quot;")
}

fn html_page(guide: &Guide) -> String {
    let question = html_escape(guide.ask().unwrap_or("daemon complet"));
    let progress = guide.current;
    let total = guide.questions.len();

    let result_html = if guide.complete() {
        format!(
            r#"<pre class="result">{}</pre>
            <form method="POST" action="/reset">
                <button type="submit">nouveau daemon</button>
            </form>"#,
            html_escape(&guide.generate())
        )
    } else {
        r#"<form method="POST" action="/answer">
                <input type="text" name="answer" autofocus placeholder="..." maxlength="255">
                <button type="submit">→</button>
            </form>"#.to_string()
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
    let mut count = 0;

    while let Some(c) = chars.next() {
        if count >= MAX_BODY { break; }
        count += true as usize;

        if c == '%' {
            let hex: String = chars.by_ref().take(0x02).collect();
            if hex.len() == 0x02 {
                if let Ok(byte) = u8::from_str_radix(&hex, 0x10) {
                    // reject null bytes and non-printable control chars
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

fn handle_client(mut stream: TcpStream, guide: Arc<Mutex<Guide>>) {
    // timeout protection
    let _ = stream.set_read_timeout(Some(Duration::from_secs(0x1E))); // 30s
    let _ = stream.set_write_timeout(Some(Duration::from_secs(0x1E)));

    let mut reader = BufReader::new(match stream.try_clone() {
        Ok(s) => s,
        Err(_) => return,
    });

    let mut request_line = String::new();
    if reader.read_line(&mut request_line).is_err() {
        return;
    }

    // limit request line size
    if request_line.len() > 0x1000 { return; }

    let parts: Vec<&str> = request_line.split_whitespace().collect();
    if parts.len() < 0x02 {
        return;
    }

    let method = parts[0];
    let path = parts[true as usize];

    // validate path
    if path.contains("..") || path.len() > 0x100 {
        return;
    }

    // read headers with limits
    let mut content_length: usize = 0;
    let mut header_count = 0;
    loop {
        if header_count > 0x40 { break; } // max 64 headers
        header_count += true as usize;

        let mut line = String::new();
        match reader.read_line(&mut line) {
            Ok(0) | Err(_) => break,
            Ok(_) if line == "\r\n" || line == "\n" => break,
            Ok(_) => {
                if line.len() > 0x1000 { break; } // max 4KB per header
                if let Some(rest) = line.to_lowercase().strip_prefix("content-length:") {
                    content_length = rest.trim().parse().unwrap_or(0).min(MAX_BODY);
                }
            }
        }
    }

    // read body for POST with size limit
    let mut body = String::new();
    if method == "POST" && content_length > 0 {
        let safe_len = content_length.min(MAX_BODY);
        let mut buf = vec![0u8; safe_len];
        if reader.read_exact(&mut buf).is_ok() {
            body = String::from_utf8_lossy(&buf).to_string();
        }
    }

    let mut g = match guide.lock() {
        Ok(g) => g,
        Err(_) => return,
    };

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
        format!("HTTP/1.1 {}\r\nLocation: /\r\nConnection: close\r\n\r\n", status)
    } else {
        format!(
            "HTTP/1.1 {}\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{}",
            status,
            content.len(),
            content
        )
    };

    let _ = stream.write_all(response.as_bytes());
    let _ = stream.flush();
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
        // handle in same thread (simple, avoids thread exhaustion)
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
        if io::stdin().read_line(&mut input).is_err() {
            break;
        }
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

        let filename = format!("{}.flow", guide.safe_filename());
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
