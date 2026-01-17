// daemon - the entity that lives
// all capabilities, strict permissions
// zero cloud, all local

use std::collections::HashSet;
use std::io::{BufRead, BufReader, Read, Write};
use std::net::{TcpListener, TcpStream};
use std::process::{Command, Stdio};
use std::sync::{Arc, Mutex};
use std::time::Duration;
use std::fs;
use std::path::Path;

// ============================================
// PERMISSIONS - NEVER BYPASS
// ============================================

#[derive(Clone, Default)]
struct Permissions {
    allowed: HashSet<String>,
}

impl Permissions {
    fn load(path: &str) -> Self {
        let mut p = Self::default();
        if let Ok(content) = fs::read_to_string(path) {
            for line in content.lines() {
                if line.starts_with("## permissions") {
                    continue;
                }
                if !line.is_empty() && !line.starts_with('#') {
                    for perm in line.split(',').map(|s| s.trim()) {
                        if perm != "none" {
                            p.allowed.insert(perm.to_string());
                        }
                    }
                }
            }
        }
        p
    }

    fn can(&self, action: &str) -> bool {
        self.allowed.contains(action)
    }

    fn require(&self, action: &str) -> Result<(), String> {
        if self.can(action) {
            Ok(())
        } else {
            Err(format!("permission denied: {}", action))
        }
    }
}

// ============================================
// CAPABILITIES - ALL LOCAL
// ============================================

struct Voice {
    enabled: bool,
}

impl Voice {
    fn new(perms: &Permissions) -> Self {
        Self { enabled: perms.can("mic") }
    }

    fn listen(&self) -> Result<String, String> {
        if !self.enabled {
            return Err("mic not permitted".into());
        }

        // whisper.cpp local
        let output = Command::new("whisper-cpp")
            .args(["--model", "base", "--file", "-"])
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .output();

        match output {
            Ok(o) => Ok(String::from_utf8_lossy(&o.stdout).to_string()),
            Err(_) => {
                // fallback: arecord + whisper
                let rec = Command::new("arecord")
                    .args(["-d", "5", "-f", "S16_LE", "-r", "16000", "-t", "wav", "/tmp/daemon_rec.wav"])
                    .output();

                if rec.is_ok() {
                    let trans = Command::new("whisper-cpp")
                        .args(["--model", "base", "--file", "/tmp/daemon_rec.wav"])
                        .output();

                    if let Ok(t) = trans {
                        return Ok(String::from_utf8_lossy(&t.stdout).to_string());
                    }
                }
                Err("stt failed".into())
            }
        }
    }

    fn speak(&self, text: &str, perms: &Permissions) -> Result<(), String> {
        // tts always allowed if daemon exists

        // try piper first
        let piper = Command::new("piper")
            .args(["--model", "fr_FR-upmc-medium", "--output-raw"])
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .spawn();

        if let Ok(mut child) = piper {
            if let Some(stdin) = child.stdin.as_mut() {
                let _ = stdin.write_all(text.as_bytes());
            }
            let output = child.wait_with_output();
            if let Ok(o) = output {
                // play audio
                let mut play = Command::new("aplay")
                    .args(["-f", "S16_LE", "-r", "22050", "-"])
                    .stdin(Stdio::piped())
                    .spawn()
                    .map_err(|e| e.to_string())?;

                if let Some(stdin) = play.stdin.as_mut() {
                    let _ = stdin.write_all(&o.stdout);
                }
                let _ = play.wait();
                return Ok(());
            }
        }

        // fallback espeak
        let _ = Command::new("espeak-ng")
            .args(["-v", "fr", text])
            .output();

        Ok(())
    }
}

struct Eyes {
    enabled: bool,
}

impl Eyes {
    fn new(perms: &Permissions) -> Self {
        Self { enabled: perms.can("cam") }
    }

    fn capture(&self) -> Result<Vec<u8>, String> {
        if !self.enabled {
            return Err("cam not permitted".into());
        }

        // ffmpeg capture
        let output = Command::new("ffmpeg")
            .args([
                "-f", "v4l2",
                "-i", "/dev/video0",
                "-frames:v", "1",
                "-f", "image2pipe",
                "-vcodec", "png",
                "-"
            ])
            .output()
            .map_err(|e| e.to_string())?;

        Ok(output.stdout)
    }

    fn screenshot(&self, perms: &Permissions) -> Result<Vec<u8>, String> {
        perms.require("screen")?;

        let output = Command::new("maim")
            .args(["-"])
            .output()
            .map_err(|e| e.to_string())?;

        Ok(output.stdout)
    }

    fn ocr(&self, image: &[u8]) -> Result<String, String> {
        // tesseract local
        fs::write("/tmp/daemon_ocr.png", image).map_err(|e| e.to_string())?;

        let output = Command::new("tesseract")
            .args(["/tmp/daemon_ocr.png", "stdout", "-l", "fra+eng"])
            .output()
            .map_err(|e| e.to_string())?;

        let _ = fs::remove_file("/tmp/daemon_ocr.png");
        Ok(String::from_utf8_lossy(&output.stdout).to_string())
    }

    fn detect(&self, image: &[u8]) -> Result<Vec<String>, String> {
        // yolo local (if available)
        fs::write("/tmp/daemon_detect.png", image).map_err(|e| e.to_string())?;

        let output = Command::new("yolo")
            .args(["detect", "/tmp/daemon_detect.png"])
            .output();

        let _ = fs::remove_file("/tmp/daemon_detect.png");

        match output {
            Ok(o) => {
                let text = String::from_utf8_lossy(&o.stdout);
                Ok(text.lines().map(|s| s.to_string()).collect())
            }
            Err(_) => Ok(vec![]) // yolo not installed, silent fail
        }
    }
}

struct Hands {
    files: bool,
    clipboard: bool,
    exec: bool,
    internet: bool,
}

impl Hands {
    fn new(perms: &Permissions) -> Self {
        Self {
            files: perms.can("files"),
            clipboard: perms.can("clipboard"),
            exec: perms.can("exec"),
            internet: perms.can("internet"),
        }
    }

    fn read_file(&self, path: &str) -> Result<String, String> {
        if !self.files {
            return Err("files not permitted".into());
        }
        fs::read_to_string(path).map_err(|e| e.to_string())
    }

    fn write_file(&self, path: &str, content: &str) -> Result<(), String> {
        if !self.files {
            return Err("files not permitted".into());
        }
        fs::write(path, content).map_err(|e| e.to_string())
    }

    fn clipboard_read(&self) -> Result<String, String> {
        if !self.clipboard {
            return Err("clipboard not permitted".into());
        }
        let output = Command::new("xclip")
            .args(["-selection", "clipboard", "-o"])
            .output()
            .map_err(|e| e.to_string())?;
        Ok(String::from_utf8_lossy(&output.stdout).to_string())
    }

    fn clipboard_write(&self, text: &str) -> Result<(), String> {
        if !self.clipboard {
            return Err("clipboard not permitted".into());
        }
        let mut child = Command::new("xclip")
            .args(["-selection", "clipboard"])
            .stdin(Stdio::piped())
            .spawn()
            .map_err(|e| e.to_string())?;

        if let Some(stdin) = child.stdin.as_mut() {
            stdin.write_all(text.as_bytes()).map_err(|e| e.to_string())?;
        }
        child.wait().map_err(|e| e.to_string())?;
        Ok(())
    }

    fn execute(&self, cmd: &str) -> Result<String, String> {
        if !self.exec {
            return Err("exec not permitted".into());
        }
        let output = Command::new("sh")
            .args(["-c", cmd])
            .output()
            .map_err(|e| e.to_string())?;
        Ok(String::from_utf8_lossy(&output.stdout).to_string())
    }

    fn fetch(&self, url: &str) -> Result<String, String> {
        if !self.internet {
            return Err("internet not permitted".into());
        }
        let output = Command::new("curl")
            .args(["-sL", url])
            .output()
            .map_err(|e| e.to_string())?;
        Ok(String::from_utf8_lossy(&output.stdout).to_string())
    }
}

// ============================================
// BRAIN - LOCAL LLM (optional)
// ============================================

struct Brain {
    model_path: Option<String>,
}

impl Brain {
    fn new() -> Self {
        // check for local models
        let paths = [
            "~/.local/share/goodgirl/model.gguf",
            "/usr/share/goodgirl/model.gguf",
            "./model.gguf",
        ];

        for p in paths {
            let expanded = shellexpand::tilde(p).to_string();
            if Path::new(&expanded).exists() {
                return Self { model_path: Some(expanded) };
            }
        }

        Self { model_path: None }
    }

    fn think(&self, prompt: &str, context: &str) -> Result<String, String> {
        let model = self.model_path.as_ref().ok_or("no local model")?;

        let full_prompt = format!("{}\n\nUser: {}\nAssistant:", context, prompt);

        let output = Command::new("llama-cli")
            .args([
                "-m", model,
                "-p", &full_prompt,
                "-n", "256",
                "--temp", "0.7",
            ])
            .output()
            .map_err(|e| e.to_string())?;

        Ok(String::from_utf8_lossy(&output.stdout).to_string())
    }

    fn available(&self) -> bool {
        self.model_path.is_some()
    }
}

// ============================================
// DAEMON - THE ENTITY
// ============================================

struct Daemon {
    name: String,
    symbol: String,
    archetype: String,
    voice_style: String,
    perms: Permissions,
    voice: Voice,
    eyes: Eyes,
    hands: Hands,
    brain: Brain,
    memory: Vec<String>,
}

impl Daemon {
    fn load(flow_path: &str) -> Result<Self, String> {
        let content = fs::read_to_string(flow_path).map_err(|e| e.to_string())?;
        let perms = Permissions::load(flow_path);

        let mut name = String::from("daemon");
        let mut symbol = String::from("✦");
        let mut archetype = String::from("unique");
        let mut voice_style = String::from("naturelle");

        for line in content.lines() {
            let line = line.trim();
            if line.starts_with("name ") {
                name = line[5..].to_string();
            } else if line.starts_with("symbol ") {
                symbol = line[7..].to_string();
            } else if line.starts_with("archetype ") {
                archetype = line[10..].to_string();
            } else if line.starts_with("## voice") {
                // next non-empty line is voice
                continue;
            } else if !line.starts_with('#') && !line.is_empty() && voice_style == "naturelle" {
                if content.contains("## voice") {
                    let idx = content.find("## voice").unwrap();
                    let after = &content[idx..];
                    if let Some(next_line) = after.lines().skip(1).find(|l| !l.trim().is_empty()) {
                        voice_style = next_line.trim().to_string();
                    }
                }
            }
        }

        Ok(Self {
            name,
            symbol,
            archetype,
            voice_style,
            perms: perms.clone(),
            voice: Voice::new(&perms),
            eyes: Eyes::new(&perms),
            hands: Hands::new(&perms),
            brain: Brain::new(),
            memory: Vec::new(),
        })
    }

    fn process(&mut self, input: &str) -> String {
        self.memory.push(format!("user: {}", input));
        if self.memory.len() > 0x14 { // keep last 20
            self.memory.remove(0);
        }

        let response = if self.brain.available() {
            let context = format!(
                "Tu es {}, {}. Tu parles de facon {}.\n\nHistorique:\n{}",
                self.name,
                self.archetype,
                self.voice_style,
                self.memory.join("\n")
            );
            self.brain.think(input, &context).unwrap_or_else(|_| self.fallback_response(input))
        } else {
            self.fallback_response(input)
        };

        self.memory.push(format!("{}: {}", self.name, response));
        response
    }

    fn fallback_response(&self, input: &str) -> String {
        // simple pattern matching without LLM
        let lower = input.to_lowercase();

        if lower.contains("bonjour") || lower.contains("salut") || lower.contains("hey") {
            return format!("{} te salue...", self.name);
        }
        if lower.contains("comment") && lower.contains("va") {
            return format!("{} va bien, merci de demander.", self.name);
        }
        if lower.contains("aide") || lower.contains("help") {
            return format!("{} est la pour toi.", self.name);
        }
        if lower.contains("merci") {
            return format!("{} sourit.", self.name);
        }
        if lower.contains("au revoir") || lower.contains("bye") {
            return format!("{} te dit a bientot...", self.name);
        }

        format!("{} t'ecoute...", self.name)
    }

    fn status(&self) -> String {
        let mut caps = vec![];
        if self.perms.can("mic") { caps.push("ecoute"); }
        if self.perms.can("cam") { caps.push("voit"); }
        if self.perms.can("files") { caps.push("fichiers"); }
        if self.perms.can("clipboard") { caps.push("clipboard"); }
        if self.perms.can("exec") { caps.push("execute"); }
        if self.perms.can("internet") { caps.push("internet"); }

        let brain_status = if self.brain.available() { "cerveau local" } else { "sans cerveau" };

        format!(
            "{} {} | {} | {} | caps: {}",
            self.symbol,
            self.name,
            self.archetype,
            brain_status,
            if caps.is_empty() { "aucune".to_string() } else { caps.join(", ") }
        )
    }
}

// ============================================
// WEB SERVER
// ============================================

fn html_page(daemon: &Daemon, messages: &[String]) -> String {
    let msgs_html: String = messages.iter()
        .map(|m| format!("<div class=\"msg\">{}</div>", html_escape(m)))
        .collect::<Vec<_>>()
        .join("\n");

    format!(r#"<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: linear-gradient(135deg, #0a0a12 0%, #1a1a2e 50%, #0f0f1a 100%);
            color: #c8c8d4;
            font-family: 'Courier New', monospace;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }}
        .header {{
            padding: 1rem;
            text-align: center;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        .status {{
            font-size: 0.8rem;
            color: #666;
        }}
        .messages {{
            flex: 1;
            overflow-y: auto;
            padding: 1rem;
        }}
        .msg {{
            margin: 0.5rem 0;
            padding: 0.5rem;
            background: rgba(255,255,255,0.03);
            border-radius: 0.5rem;
        }}
        .input-area {{
            padding: 1rem;
            border-top: 1px solid rgba(255,255,255,0.1);
            display: flex;
            gap: 0.5rem;
        }}
        input {{
            flex: 1;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 0.5rem;
            color: #fff;
            padding: 0.75rem;
            font-family: inherit;
        }}
        button {{
            background: rgba(255,255,255,0.1);
            border: none;
            border-radius: 0.5rem;
            color: #fff;
            padding: 0.75rem 1rem;
            cursor: pointer;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{symbol} {name}</h1>
        <p class="status">{status}</p>
    </div>
    <div class="messages" id="msgs">
        {msgs_html}
    </div>
    <form class="input-area" method="POST" action="/msg">
        <input type="text" name="msg" autofocus placeholder="...">
        <button type="submit">→</button>
    </form>
    <script>
        document.getElementById('msgs').scrollTop = 999999;
    </script>
</body>
</html>"#,
        name = daemon.name,
        symbol = daemon.symbol,
        status = html_escape(&daemon.status()),
        msgs_html = msgs_html
    )
}

fn html_escape(s: &str) -> String {
    s.replace('&', "&amp;")
        .replace('<', "&lt;")
        .replace('>', "&gt;")
}

fn parse_post(body: &str, key: &str) -> Option<String> {
    for part in body.split('&') {
        if let Some(val) = part.strip_prefix(&format!("{}=", key)) {
            return Some(urldecode(val));
        }
    }
    None
}

fn urldecode(s: &str) -> String {
    let mut result = String::new();
    let mut chars = s.chars();
    while let Some(c) = chars.next() {
        if c == '%' {
            let hex: String = chars.by_ref().take(2).collect();
            if let Ok(byte) = u8::from_str_radix(&hex, 16) {
                if byte >= 0x20 {
                    result.push(byte as char);
                }
            }
        } else if c == '+' {
            result.push(' ');
        } else {
            result.push(c);
        }
    }
    result
}

fn handle_client(
    mut stream: TcpStream,
    daemon: Arc<Mutex<Daemon>>,
    messages: Arc<Mutex<Vec<String>>>
) {
    let _ = stream.set_read_timeout(Some(Duration::from_secs(30)));
    let _ = stream.set_write_timeout(Some(Duration::from_secs(30)));

    let mut reader = BufReader::new(match stream.try_clone() {
        Ok(s) => s,
        Err(_) => return,
    });

    let mut req_line = String::new();
    if reader.read_line(&mut req_line).is_err() { return; }

    let parts: Vec<&str> = req_line.split_whitespace().collect();
    if parts.len() < 2 { return; }

    let method = parts[0];
    let path = parts[1];

    // read headers
    let mut content_length = 0usize;
    loop {
        let mut line = String::new();
        match reader.read_line(&mut line) {
            Ok(0) | Err(_) => break,
            Ok(_) if line == "\r\n" || line == "\n" => break,
            Ok(_) => {
                if let Some(rest) = line.to_lowercase().strip_prefix("content-length:") {
                    content_length = rest.trim().parse().unwrap_or(0).min(0xFFFF);
                }
            }
        }
    }

    // read body
    let mut body = String::new();
    if method == "POST" && content_length > 0 {
        let mut buf = vec![0u8; content_length];
        if reader.read_exact(&mut buf).is_ok() {
            body = String::from_utf8_lossy(&buf).to_string();
        }
    }

    let (status, content) = match (method, path) {
        ("GET", "/") => {
            let d = daemon.lock().unwrap();
            let m = messages.lock().unwrap();
            ("200 OK", html_page(&d, &m))
        }
        ("POST", "/msg") => {
            if let Some(msg) = parse_post(&body, "msg") {
                if !msg.is_empty() {
                    let mut m = messages.lock().unwrap();
                    m.push(format!("toi: {}", msg));

                    let mut d = daemon.lock().unwrap();
                    let response = d.process(&msg);
                    m.push(response);

                    // keep last 100 messages
                    while m.len() > 100 {
                        m.remove(0);
                    }
                }
            }
            ("303 See Other", String::new())
        }
        _ => ("404 Not Found", String::from("not found")),
    };

    let response = if status.starts_with("303") {
        format!("HTTP/1.1 {}\r\nLocation: /\r\n\r\n", status)
    } else {
        format!(
            "HTTP/1.1 {}\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {}\r\n\r\n{}",
            status, content.len(), content
        )
    };

    let _ = stream.write_all(response.as_bytes());
}

fn web_mode(daemon: Arc<Mutex<Daemon>>, messages: Arc<Mutex<Vec<String>>>) {
    let addr = "127.0.0.1:8080";
    let listener = match TcpListener::bind(addr) {
        Ok(l) => l,
        Err(e) => {
            eprintln!("cannot bind: {}", e);
            return;
        }
    };

    let d = daemon.lock().unwrap();
    println!();
    println!("  {} {} en ligne", d.symbol, d.name);
    println!("  http://{}", addr);
    println!("  {}", d.status());
    println!();
    drop(d);

    for stream in listener.incoming().flatten() {
        handle_client(stream, Arc::clone(&daemon), Arc::clone(&messages));
    }
}

fn cli_mode(daemon: Arc<Mutex<Daemon>>) {
    let d = daemon.lock().unwrap();
    println!();
    println!("  {} {}", d.symbol, d.name);
    println!("  {}", d.status());
    println!();
    drop(d);

    let stdin = std::io::stdin();
    loop {
        print!("> ");
        std::io::stdout().flush().unwrap();

        let mut input = String::new();
        if stdin.read_line(&mut input).is_err() { break; }
        let input = input.trim();

        if input == "q" || input == "quit" {
            let d = daemon.lock().unwrap();
            println!("\n  {} → void\n", d.name);
            break;
        }

        if input.is_empty() { continue; }

        let mut d = daemon.lock().unwrap();
        let response = d.process(input);
        println!("\n  {}\n", response);
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();

    // find .flow file
    let flow_path = if args.len() > 1 && !args[1].starts_with('-') {
        args[1].clone()
    } else {
        // find first .flow in current dir
        fs::read_dir(".")
            .ok()
            .and_then(|entries| {
                entries
                    .filter_map(|e| e.ok())
                    .find(|e| e.path().extension().map(|x| x == "flow").unwrap_or(false))
                    .map(|e| e.path().to_string_lossy().to_string())
            })
            .unwrap_or_else(|| "daemon.flow".to_string())
    };

    let daemon = match Daemon::load(&flow_path) {
        Ok(d) => Arc::new(Mutex::new(d)),
        Err(e) => {
            eprintln!("cannot load {}: {}", flow_path, e);
            eprintln!("usage: daemon [file.flow] [web]");
            return;
        }
    };

    let messages = Arc::new(Mutex::new(Vec::new()));

    let web = args.iter().any(|a| a == "web");

    if web {
        web_mode(daemon, messages);
    } else {
        cli_mode(daemon);
    }
}

// shellexpand minimal
mod shellexpand {
    pub fn tilde(s: &str) -> std::borrow::Cow<str> {
        if s.starts_with("~/") {
            if let Some(home) = std::env::var_os("HOME") {
                return std::borrow::Cow::Owned(format!("{}{}", home.to_string_lossy(), &s[1..]));
            }
        }
        std::borrow::Cow::Borrowed(s)
    }
}
