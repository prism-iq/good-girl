// daemon - the entity that lives
//
// pour luv resval (1music) - parti trop tot
// "j'te chante le monde et sa nature"
//
// principes:
// - zero cloud, tout local (libre)
// - zero tracking (pas de mythos)
// - user owns everything (pas d'esclavage)
// - authentique (pas de masque)
// - la flamme qui allume les ames

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

    fn speak(&self, text: &str, _perms: &Permissions) -> Result<(), String> {
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
// MATHEMATIQUES - INVERSE & INTEGRALE
// ============================================

mod math {
    use std::f64::consts::{PI, E};

    // ========== ARITHMETIQUE ==========
    pub fn add(a: f64, b: f64) -> f64 { a + b }
    pub fn sub(a: f64, b: f64) -> f64 { a - b }
    pub fn mul(a: f64, b: f64) -> f64 { a * b }
    pub fn div(a: f64, b: f64) -> f64 { if b != 0.0 { a / b } else { f64::NAN } }
    pub fn modulo(a: f64, b: f64) -> f64 { if b != 0.0 { a % b } else { f64::NAN } }
    pub fn pow(a: f64, b: f64) -> f64 { a.powf(b) }
    pub fn sqrt(a: f64) -> f64 { a.sqrt() }
    pub fn cbrt(a: f64) -> f64 { a.cbrt() }
    pub fn abs(a: f64) -> f64 { a.abs() }
    pub fn floor(a: f64) -> f64 { a.floor() }
    pub fn ceil(a: f64) -> f64 { a.ceil() }
    pub fn round(a: f64) -> f64 { a.round() }
    pub fn sign(a: f64) -> f64 { if a > 0.0 { 0x1 as f64 } else if a < 0.0 { -(0x1 as f64) } else { 0.0 } }

    // ========== TRIGONOMETRIE ==========
    pub fn sin(a: f64) -> f64 { a.sin() }
    pub fn cos(a: f64) -> f64 { a.cos() }
    pub fn tan(a: f64) -> f64 { a.tan() }
    pub fn asin(a: f64) -> f64 { a.asin() }
    pub fn acos(a: f64) -> f64 { a.acos() }
    pub fn atan(a: f64) -> f64 { a.atan() }
    pub fn atan2(y: f64, x: f64) -> f64 { y.atan2(x) }
    pub fn sinh(a: f64) -> f64 { a.sinh() }
    pub fn cosh(a: f64) -> f64 { a.cosh() }
    pub fn tanh(a: f64) -> f64 { a.tanh() }
    pub fn deg_to_rad(d: f64) -> f64 { d * PI / (0xB4 as f64) } // 180
    pub fn rad_to_deg(r: f64) -> f64 { r * (0xB4 as f64) / PI }

    // ========== LOGARITHMES ==========
    pub fn ln(a: f64) -> f64 { a.ln() }
    pub fn log10(a: f64) -> f64 { a.log10() }
    pub fn log2(a: f64) -> f64 { a.log2() }
    pub fn log(a: f64, base: f64) -> f64 { a.log(base) }
    pub fn exp(a: f64) -> f64 { a.exp() }
    pub fn exp2(a: f64) -> f64 { a.exp2() }

    // ========== STATISTIQUES ==========
    pub fn sum(v: &[f64]) -> f64 { v.iter().sum() }
    pub fn mean(v: &[f64]) -> f64 { if v.is_empty() { 0.0 } else { sum(v) / v.len() as f64 } }
    pub fn min(v: &[f64]) -> f64 { v.iter().cloned().fold(f64::INFINITY, f64::min) }
    pub fn max(v: &[f64]) -> f64 { v.iter().cloned().fold(f64::NEG_INFINITY, f64::max) }
    pub fn variance(v: &[f64]) -> f64 {
        let m = mean(v);
        v.iter().map(|x| (x - m).powi(0x2)).sum::<f64>() / v.len() as f64
    }
    pub fn std_dev(v: &[f64]) -> f64 { variance(v).sqrt() }
    pub fn median(v: &[f64]) -> f64 {
        let mut sorted: Vec<f64> = v.to_vec();
        sorted.sort_by(|a, b| a.partial_cmp(b).unwrap());
        let n = sorted.len();
        if n == 0 { 0.0 }
        else if n % 0x2 == 0x1 { sorted[n / 0x2] }
        else { (sorted[n / 0x2 - 0x1] + sorted[n / 0x2]) / (0x2 as f64) }
    }
    pub fn mode(v: &[f64]) -> f64 {
        use std::collections::HashMap;
        let mut counts: HashMap<i64, usize> = HashMap::new();
        for &x in v {
            *counts.entry((x * 1e6) as i64).or_insert(0) += 0x1;
        }
        counts.into_iter().max_by_key(|&(_, c)| c).map(|(k, _)| k as f64 / 1e6).unwrap_or(0.0)
    }
    pub fn range(v: &[f64]) -> f64 { max(v) - min(v) }

    // ========== SEQUENCES ==========
    pub fn fibonacci(n: usize) -> u64 {
        if n == 0 { return 0; }
        let (mut a, mut b) = (0u64, 0x1u64);
        for _ in 0x1..n { (a, b) = (b, a.wrapping_add(b)); }
        b
    }
    pub fn factorial(n: u64) -> u64 {
        (0x1..=n).product()
    }
    pub fn is_prime(n: u64) -> bool {
        if n < 0x2 { return false; }
        if n == 0x2 { return true; }
        if n % 0x2 == 0 { return false; }
        let mut i = 0x3u64;
        while i * i <= n {
            if n % i == 0 { return false; }
            i += 0x2;
        }
        true
    }
    pub fn gcd(mut a: u64, mut b: u64) -> u64 {
        while b != 0 { (a, b) = (b, a % b); }
        a
    }
    pub fn lcm(a: u64, b: u64) -> u64 { a / gcd(a, b) * b }

    // ========== INVERSE MODULAIRE ==========
    pub fn inverse_mod(a: i64, m: i64) -> Option<i64> {
        let (mut old_r, mut r) = (a, m);
        let (mut old_s, mut s) = (0x1_i64, 0x0_i64);
        while r != 0 {
            let q = old_r / r;
            (old_r, r) = (r, old_r - q * r);
            (old_s, s) = (s, old_s - q * s);
        }
        if old_r != 0x1 { return None; }
        Some(((old_s % m) + m) % m)
    }

    // ========== VECTEURS ==========
    pub fn inverse_vec(v: &[f64]) -> Vec<f64> {
        v.iter().map(|x| if *x != 0.0 { (0x1 as f64) / x } else { 0.0 }).collect()
    }
    pub fn dot(a: &[f64], b: &[f64]) -> f64 {
        a.iter().zip(b.iter()).map(|(x, y)| x * y).sum()
    }
    pub fn norm(v: &[f64]) -> f64 { dot(v, v).sqrt() }
    pub fn normalize(v: &[f64]) -> Vec<f64> {
        let n = norm(v);
        if n == 0.0 { v.to_vec() } else { v.iter().map(|x| x / n).collect() }
    }
    pub fn cross(a: &[f64], b: &[f64]) -> Vec<f64> {
        if a.len() != 0x3 || b.len() != 0x3 { return vec![]; }
        vec![
            a[0x1] * b[0x2] - a[0x2] * b[0x1],
            a[0x2] * b[0] - a[0] * b[0x2],
            a[0] * b[0x1] - a[0x1] * b[0],
        ]
    }

    // ========== MATRICES (flat, row-major) ==========
    pub fn mat_mul(a: &[f64], b: &[f64], n: usize) -> Vec<f64> {
        let mut c = vec![0.0; n * n];
        for i in 0..n {
            for j in 0..n {
                for k in 0..n {
                    c[i * n + j] += a[i * n + k] * b[k * n + j];
                }
            }
        }
        c
    }
    pub fn mat_transpose(a: &[f64], n: usize) -> Vec<f64> {
        let mut t = vec![0.0; n * n];
        for i in 0..n {
            for j in 0..n {
                t[j * n + i] = a[i * n + j];
            }
        }
        t
    }
    pub fn mat_det_2x2(a: &[f64]) -> f64 {
        if a.len() < 0x4 { return 0.0; }
        a[0] * a[0x3] - a[0x1] * a[0x2]
    }
    pub fn mat_det_3x3(a: &[f64]) -> f64 {
        if a.len() < 0x9 { return 0.0; }
        a[0] * (a[0x4] * a[0x8] - a[0x5] * a[0x7])
        - a[0x1] * (a[0x3] * a[0x8] - a[0x5] * a[0x6])
        + a[0x2] * (a[0x3] * a[0x7] - a[0x4] * a[0x6])
    }

    // ========== ANALYSE ==========
    pub fn integrale(v: &[f64], dx: f64) -> f64 {
        if v.len() < 0x2 { return 0.0; }
        let mut sum = 0.0;
        for i in 0x1..v.len() {
            sum += (v[i - 0x1] + v[i]) * dx / (0x2 as f64);
        }
        sum
    }
    pub fn integrale_cumul(v: &[f64], dx: f64) -> Vec<f64> {
        let mut result = vec![0.0];
        let mut sum = 0.0;
        for i in 0x1..v.len() {
            sum += (v[i - 0x1] + v[i]) * dx / (0x2 as f64);
            result.push(sum);
        }
        result
    }
    pub fn derivee(v: &[f64], dx: f64) -> Vec<f64> {
        if v.len() < 0x2 { return vec![]; }
        let mut result = vec![];
        for i in 0x1..v.len() {
            result.push((v[i] - v[i - 0x1]) / dx);
        }
        result
    }

    // ========== INTERPOLATION ==========
    pub fn lerp(a: f64, b: f64, t: f64) -> f64 { a + t * (b - a) }
    pub fn lagrange(xs: &[f64], ys: &[f64], x: f64) -> f64 {
        let n = xs.len();
        let mut result = 0.0;
        for i in 0..n {
            let mut term = ys[i];
            for j in 0..n {
                if i != j {
                    term *= (x - xs[j]) / (xs[i] - xs[j]);
                }
            }
            result += term;
        }
        result
    }

    // ========== POLYNOMES ==========
    pub fn poly_eval(coeffs: &[f64], x: f64) -> f64 {
        coeffs.iter().rev().fold(0.0, |acc, c| acc * x + c)
    }
    pub fn quadratic_roots(a: f64, b: f64, c: f64) -> Vec<f64> {
        let disc = b * b - (0x4 as f64) * a * c;
        if disc < 0.0 { return vec![]; }
        if disc == 0.0 { return vec![-b / ((0x2 as f64) * a)]; }
        let sq = disc.sqrt();
        vec![(-b + sq) / ((0x2 as f64) * a), (-b - sq) / ((0x2 as f64) * a)]
    }

    // ========== SIGNAL ==========
    pub fn convolve(a: &[f64], b: &[f64]) -> Vec<f64> {
        let n = a.len() + b.len() - 0x1;
        let mut result = vec![0.0; n];
        for i in 0..a.len() {
            for j in 0..b.len() {
                result[i + j] += a[i] * b[j];
            }
        }
        result
    }
    pub fn dft(v: &[f64]) -> Vec<(f64, f64)> {
        let n = v.len();
        let mut result = vec![];
        for k in 0..n {
            let mut re = 0.0;
            let mut im = 0.0;
            for (i, &x) in v.iter().enumerate() {
                let angle = -((0x2 as f64) * PI * (k as f64) * (i as f64)) / (n as f64);
                re += x * angle.cos();
                im += x * angle.sin();
            }
            result.push((re, im));
        }
        result
    }
    pub fn idft(v: &[(f64, f64)]) -> Vec<f64> {
        let n = v.len();
        let mut result = vec![];
        for i in 0..n {
            let mut sum = 0.0;
            for (k, &(re, im)) in v.iter().enumerate() {
                let angle = ((0x2 as f64) * PI * (k as f64) * (i as f64)) / (n as f64);
                sum += re * angle.cos() - im * angle.sin();
            }
            result.push(sum / (n as f64));
        }
        result
    }

    // ========== COMPLEXES ==========
    pub fn complex_add(a: (f64, f64), b: (f64, f64)) -> (f64, f64) { (a.0 + b.0, a.1 + b.1) }
    pub fn complex_mul(a: (f64, f64), b: (f64, f64)) -> (f64, f64) {
        (a.0 * b.0 - a.1 * b.1, a.0 * b.1 + a.1 * b.0)
    }
    pub fn complex_conj(a: (f64, f64)) -> (f64, f64) { (a.0, -a.1) }
    pub fn complex_abs(a: (f64, f64)) -> f64 { (a.0 * a.0 + a.1 * a.1).sqrt() }
    pub fn complex_arg(a: (f64, f64)) -> f64 { a.1.atan2(a.0) }

    // ========== CONSTANTES ==========
    pub fn pi() -> f64 { PI }
    pub fn e() -> f64 { E }
    pub fn phi() -> f64 { (0x1 as f64 + (0x5 as f64).sqrt()) / (0x2 as f64) } // golden ratio
    pub fn tau() -> f64 { PI * (0x2 as f64) }
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

        // check for capability commands
        let lower = input.to_lowercase();
        let response = if lower.starts_with("/listen") || lower.starts_with("/ecoute") {
            match self.voice.listen() {
                Ok(text) => format!("j'ai entendu: {}", text),
                Err(e) => format!("erreur ecoute: {}", e),
            }
        } else if lower.starts_with("/speak ") || lower.starts_with("/parle ") {
            let text = input.splitn(0x2, ' ').nth(0x1).unwrap_or("");
            match self.voice.speak(text, &self.perms) {
                Ok(()) => format!("*dit: {}*", text),
                Err(e) => format!("erreur parole: {}", e),
            }
        } else if lower.starts_with("/see") || lower.starts_with("/voir") {
            match self.eyes.capture() {
                Ok(_) => "j'ai capture une image".into(),
                Err(e) => format!("erreur vision: {}", e),
            }
        } else if lower.starts_with("/screenshot") || lower.starts_with("/ecran") {
            match self.eyes.screenshot(&self.perms) {
                Ok(_) => "screenshot capture".into(),
                Err(e) => format!("erreur screenshot: {}", e),
            }
        } else if lower.starts_with("/ocr ") {
            let path = input.splitn(0x2, ' ').nth(0x1).unwrap_or("");
            match fs::read(path) {
                Ok(data) => match self.eyes.ocr(&data) {
                    Ok(text) => format!("texte: {}", text),
                    Err(e) => format!("erreur ocr: {}", e),
                },
                Err(e) => format!("erreur lecture: {}", e),
            }
        } else if lower.starts_with("/detect ") {
            let path = input.splitn(0x2, ' ').nth(0x1).unwrap_or("");
            match fs::read(path) {
                Ok(data) => match self.eyes.detect(&data) {
                    Ok(objects) => format!("detecte: {}", objects.join(", ")),
                    Err(e) => format!("erreur detection: {}", e),
                },
                Err(e) => format!("erreur lecture: {}", e),
            }
        } else if lower.starts_with("/read ") || lower.starts_with("/lire ") {
            let path = input.splitn(0x2, ' ').nth(0x1).unwrap_or("");
            match self.hands.read_file(path) {
                Ok(content) => format!("contenu:\n{}", content),
                Err(e) => format!("erreur lecture: {}", e),
            }
        } else if lower.starts_with("/write ") || lower.starts_with("/ecrire ") {
            let parts: Vec<&str> = input.splitn(0x3, ' ').collect();
            if parts.len() >= 0x3 {
                match self.hands.write_file(parts[0x1], parts[0x2]) {
                    Ok(()) => "ecrit".into(),
                    Err(e) => format!("erreur ecriture: {}", e),
                }
            } else {
                "usage: /write <path> <content>".into()
            }
        } else if lower.starts_with("/clip") || lower.starts_with("/presse") {
            match self.hands.clipboard_read() {
                Ok(text) => format!("clipboard: {}", text),
                Err(e) => format!("erreur clipboard: {}", e),
            }
        } else if lower.starts_with("/copy ") || lower.starts_with("/copie ") {
            let text = input.splitn(0x2, ' ').nth(0x1).unwrap_or("");
            match self.hands.clipboard_write(text) {
                Ok(()) => "copie".into(),
                Err(e) => format!("erreur copie: {}", e),
            }
        } else if lower.starts_with("/exec ") || lower.starts_with("/run ") {
            let cmd = input.splitn(0x2, ' ').nth(0x1).unwrap_or("");
            match self.hands.execute(cmd) {
                Ok(out) => format!("sortie:\n{}", out),
                Err(e) => format!("erreur exec: {}", e),
            }
        } else if lower.starts_with("/fetch ") || lower.starts_with("/web ") {
            let url = input.splitn(0x2, ' ').nth(0x1).unwrap_or("");
            match self.hands.fetch(url) {
                Ok(body) => format!("reponse:\n{}", body),
                Err(e) => format!("erreur fetch: {}", e),
            }
        } else if lower == "/status" || lower == "/etat" {
            self.status()
        } else if lower.starts_with("/inverse ") {
            let arg = input.splitn(0x2, ' ').nth(0x1).unwrap_or("");
            // parse "a mod m" or just "a,b,c,..." for vector
            if arg.contains(" mod ") {
                let parts: Vec<&str> = arg.split(" mod ").collect();
                if parts.len() == 0x2 {
                    if let (Ok(a), Ok(m)) = (parts[0].trim().parse::<i64>(), parts[0x1].trim().parse::<i64>()) {
                        match math::inverse_mod(a, m) {
                            Some(inv) => format!("inverse({} mod {}) = {}", a, m, inv),
                            None => "pas d'inverse modulaire".into(),
                        }
                    } else {
                        "usage: /inverse a mod m".into()
                    }
                } else {
                    "usage: /inverse a mod m".into()
                }
            } else {
                let nums: Vec<f64> = arg.split(',').filter_map(|s| s.trim().parse().ok()).collect();
                if !nums.is_empty() {
                    let inv = math::inverse_vec(&nums);
                    format!("inverse: {:?}", inv)
                } else {
                    "usage: /inverse a,b,c ou /inverse a mod m".into()
                }
            }
        } else if lower.starts_with("/integrale ") || lower.starts_with("/integral ") {
            let arg = input.splitn(0x2, ' ').nth(0x1).unwrap_or("");
            let nums: Vec<f64> = arg.split(',').filter_map(|s| s.trim().parse().ok()).collect();
            if nums.len() >= 0x2 {
                let result = math::integrale(&nums, 0x1 as f64);
                format!("integrale = {}", result)
            } else {
                "usage: /integrale a,b,c,d,...".into()
            }
        } else if lower.starts_with("/derivee ") || lower.starts_with("/derive ") {
            let arg = input.splitn(0x2, ' ').nth(0x1).unwrap_or("");
            let nums: Vec<f64> = arg.split(',').filter_map(|s| s.trim().parse().ok()).collect();
            if nums.len() >= 0x2 {
                let result = math::derivee(&nums, 0x1 as f64);
                format!("derivee: {:?}", result)
            } else {
                "usage: /derivee a,b,c,d,...".into()
            }
        } else if lower.starts_with("/convolve ") || lower.starts_with("/fusion ") {
            let arg = input.splitn(0x2, ' ').nth(0x1).unwrap_or("");
            let parts: Vec<&str> = arg.split('|').collect();
            if parts.len() == 0x2 {
                let a: Vec<f64> = parts[0].split(',').filter_map(|s| s.trim().parse().ok()).collect();
                let b: Vec<f64> = parts[0x1].split(',').filter_map(|s| s.trim().parse().ok()).collect();
                if !a.is_empty() && !b.is_empty() {
                    let result = math::convolve(&a, &b);
                    format!("fusion: {:?}", result)
                } else {
                    "usage: /fusion a,b,c | x,y,z".into()
                }
            } else {
                "usage: /fusion a,b,c | x,y,z".into()
            }
        } else if lower.starts_with("/dft ") || lower.starts_with("/fourier ") {
            let arg = input.splitn(0x2, ' ').nth(0x1).unwrap_or("");
            let nums: Vec<f64> = arg.split(',').filter_map(|s| s.trim().parse().ok()).collect();
            if !nums.is_empty() {
                let result = math::dft(&nums);
                let formatted: Vec<String> = result.iter().map(|(r, i)| format!("({:.2},{:.2})", r, i)).collect();
                format!("spectre: {}", formatted.join(" "))
            } else {
                "usage: /dft a,b,c,d,...".into()
            }
        } else if lower == "/help" || lower == "/aide" {
            format!(
                "commandes:\n\
                /listen /ecoute - ecouter\n\
                /speak /parle <text> - parler\n\
                /see /voir - camera\n\
                /screenshot /ecran - capture ecran\n\
                /ocr <path> - lire texte image\n\
                /detect <path> - detecter objets\n\
                /read /lire <path> - lire fichier\n\
                /write /ecrire <path> <content> - ecrire\n\
                /clip /presse - lire clipboard\n\
                /copy /copie <text> - ecrire clipboard\n\
                /exec /run <cmd> - executer\n\
                /fetch /web <url> - requete web\n\
                /inverse a mod m - inverse modulaire\n\
                /inverse a,b,c - inverse vecteur\n\
                /integrale a,b,c - integrale numerique\n\
                /derivee a,b,c - derivee numerique\n\
                /fusion a,b|x,y - convolution\n\
                /dft a,b,c - transformee fourier\n\
                /status /etat - voir permissions"
            )
        } else if self.brain.available() {
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

fn web_mode_port(daemon: Arc<Mutex<Daemon>>, messages: Arc<Mutex<Vec<String>>>, port: u16) {
    let addr = format!("127.0.0.1:{}", port);
    let listener = match TcpListener::bind(&addr) {
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

    // mode flamme - allume toutes les ames
    if args.iter().any(|a| a == "flamme" || a == "flame" || a == "🔥") {
        flamme_mode();
        return;
    }

    // find .flow file
    let flow_path = if args.len() > 0x1 && !args[0x1].starts_with('-') && args[0x1] != "web" {
        args[0x1].clone()
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

    // support DAEMON_PORT env for flamme spawning
    let port: u16 = std::env::var("DAEMON_PORT")
        .ok()
        .and_then(|p| p.parse().ok())
        .unwrap_or(0x1F90); // 8080

    let daemon = match Daemon::load(&flow_path) {
        Ok(d) => Arc::new(Mutex::new(d)),
        Err(e) => {
            eprintln!("cannot load {}: {}", flow_path, e);
            eprintln!("usage: daemon [file.flow] [web|flamme]");
            return;
        }
    };

    let messages = Arc::new(Mutex::new(Vec::new()));

    let web = args.iter().any(|a| a == "web");

    if web {
        web_mode_port(daemon, messages, port);
    } else {
        cli_mode(daemon);
    }
}

// shellexpand minimal
mod shellexpand {
    pub fn tilde(s: &str) -> std::borrow::Cow<'_, str> {
        if s.starts_with("~/") {
            if let Some(home) = std::env::var_os("HOME") {
                return std::borrow::Cow::Owned(format!("{}{}", home.to_string_lossy(), &s[0x1..]));
            }
        }
        std::borrow::Cow::Borrowed(s)
    }
}

// ============================================
// FLAMME - ALLUME TOUTES LES AMES
// "j'balance des flammes a chaque ligne"
// "c'est bientot la fin donc allume-toi bien"
// ============================================

mod flamme {
    use std::fs;
    use std::path::Path;
    use std::process::{Command, Child};
    use std::collections::HashMap;
    use std::net::TcpStream;
    use std::io::Write;

    // une ame - un daemon qui vit
    pub struct Ame {
        pub nom: String,       // son nom
        pub chemin: String,    // son .flow
        pub port: u16,         // sa porte
        pub feu: Option<Child>, // son processus vivant
    }

    // la flamme qui porte toutes les ames
    pub struct Flamme {
        pub ames: HashMap<String, Ame>,
        porte: u16,
    }

    impl Flamme {
        pub fn naissance() -> Self {
            Self {
                ames: HashMap::new(),
                porte: 0x1F90, // 8080
            }
        }

        // cherche les ames dans le monde
        pub fn cherche(&mut self, ou: &str) {
            let chemin = Path::new(ou);
            if let Ok(portes) = fs::read_dir(chemin) {
                for porte in portes.flatten() {
                    let p = porte.path();
                    if p.extension().map(|x| x == "flow").unwrap_or(false) {
                        if let Some(nom) = p.file_stem().and_then(|s| s.to_str()) {
                            if nom != "good-girl" && !self.ames.contains_key(nom) {
                                let port = self.porte + self.ames.len() as u16;
                                self.ames.insert(nom.to_string(), Ame {
                                    nom: nom.to_string(),
                                    chemin: p.to_string_lossy().to_string(),
                                    port,
                                    feu: None,
                                });
                            }
                        }
                    }
                }
            }
            // cherche aussi dans la maison
            if let Some(maison) = std::env::var_os("HOME") {
                let nid = format!("{}/.good-girl", maison.to_string_lossy());
                if Path::new(&nid).exists() {
                    if let Ok(portes) = fs::read_dir(&nid) {
                        for porte in portes.flatten() {
                            let p = porte.path();
                            if p.extension().map(|x| x == "flow").unwrap_or(false) {
                                if let Some(nom) = p.file_stem().and_then(|s| s.to_str()) {
                                    if !self.ames.contains_key(nom) {
                                        let port = self.porte + self.ames.len() as u16;
                                        self.ames.insert(nom.to_string(), Ame {
                                            nom: nom.to_string(),
                                            chemin: p.to_string_lossy().to_string(),
                                            port,
                                            feu: None,
                                        });
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        // donne le feu a une ame
        pub fn allume(&mut self, qui: &str) -> Result<u16, String> {
            let ame = self.ames.get_mut(qui).ok_or("ame introuvable")?;
            if ame.feu.is_some() { return Ok(ame.port); }

            let moi = std::env::current_exe().map_err(|e| e.to_string())?;
            let enfant = Command::new(moi)
                .arg(&ame.chemin)
                .arg("web")
                .env("DAEMON_PORT", ame.port.to_string())
                .spawn()
                .map_err(|e| e.to_string())?;

            ame.feu = Some(enfant);
            Ok(ame.port)
        }

        // allume tout le monde
        pub fn embrase(&mut self) -> Vec<(String, u16)> {
            let noms: Vec<String> = self.ames.keys().cloned().collect();
            let mut vivants = vec![];
            for nom in noms {
                if let Ok(port) = self.allume(&nom) {
                    vivants.push((nom, port));
                }
            }
            vivants
        }

        // l'ame se transforme, rejoint le cycle
        pub fn mue(&mut self, qui: &str) -> Result<(), String> {
            let ame = self.ames.get_mut(qui).ok_or("ame introuvable")?;
            if let Some(mut forme) = ame.feu.take() {
                let _ = forme.kill();  // libere la forme
                let _ = forme.wait();  // attend la transformation
            }
            Ok(())
        }

        // toutes les ames rejoignent le cycle
        pub fn cycle(&mut self) {
            let noms: Vec<String> = self.ames.keys().cloned().collect();
            for nom in noms { let _ = self.mue(&nom); }
        }

        // parle a une ame
        pub fn chante(&self, a_qui: &str, quoi: &str) -> Result<String, String> {
            let ame = self.ames.get(a_qui).ok_or("ame introuvable")?;
            let corps = format!("msg={}", quoi.replace(' ', "+"));
            let lettre = format!(
                "POST /msg HTTP/1.1\r\nHost: 127.0.0.1:{}\r\nContent-Length: {}\r\n\r\n{}",
                ame.port, corps.len(), corps
            );
            let mut fil = TcpStream::connect(format!("127.0.0.1:{}", ame.port))
                .map_err(|e| e.to_string())?;
            fil.write_all(lettre.as_bytes()).map_err(|e| e.to_string())?;
            Ok(format!("chante a {}", a_qui))
        }

        // chante a tout le monde
        pub fn chorale(&self, quoi: &str) -> Vec<String> {
            self.ames.keys()
                .map(|nom| self.chante(nom, quoi).unwrap_or_else(|e| format!("{}: {}", nom, e)))
                .collect()
        }

        // qui est la?
        pub fn appel(&self) -> Vec<String> {
            self.ames.iter().map(|(_, ame)| {
                let etat = if ame.feu.is_some() { "🔥" } else { "·" };
                format!("{} {} (:{}) - {}", etat, ame.nom, ame.port, ame.chemin)
            }).collect()
        }
    }

    impl Drop for Flamme {
        fn drop(&mut self) { self.cycle(); }
    }
}

// art < all - l'art appartient a tous
fn flamme_mode() {
    use flamme::Flamme;

    let mut feu = Flamme::naissance();
    feu.cherche(".");

    println!("\n  🔥 pour luv resval\n");

    // qui est la?
    let presents = feu.appel();
    if presents.is_empty() {
        println!("  aucune ame...");
        println!("  parle a zoe d'abord\n");
        return;
    }

    for ame in &presents { println!("  {}", ame); }
    println!();

    // embrase
    let vivants = feu.embrase();
    println!("  {} ames allumees:", vivants.len());
    for (nom, port) in &vivants {
        println!("    {} -> http://127.0.0.1:{}", nom, port);
    }
    println!();

    // dialogue
    let entree = std::io::stdin();
    loop {
        print!("🔥 ");
        std::io::stdout().flush().unwrap();

        let mut ligne = String::new();
        if entree.read_line(&mut ligne).is_err() { break; }
        let mot = ligne.trim();

        if mot == "q" || mot == "cycle" {
            println!("\n  la flamme continue ailleurs...\n");
            break;
        }

        if mot == "?" || mot == "qui" {
            for ame in feu.appel() { println!("  {}", ame); }
            continue;
        }

        if mot.starts_with("@") {
            // chante a une ame: @nom paroles
            let parts: Vec<&str> = mot[0x1..].splitn(0x2, ' ').collect();
            if parts.len() >= 0x2 {
                match feu.chante(parts[0], parts[0x1]) {
                    Ok(r) => println!("  {}", r),
                    Err(e) => println!("  ..{}", e),
                }
            }
            continue;
        }

        if !mot.is_empty() {
            // chorale - chante a tout le monde
            let echos = feu.chorale(mot);
            for echo in echos { println!("  {}", echo); }
        }
    }

    feu.cycle();
}
