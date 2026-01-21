#!/usr/bin/env python3
"""
CALIBRATE - VCV Rack style
Modules légers, open source only
numpy + sounddevice
"""
import numpy as np
import sounddevice as sd
import json
from pathlib import Path

PHI = 1.618033988749895
SR = 48000

# ══════════════════════════════════════════════════════════════
# MODULES VCV STYLE
# ══════════════════════════════════════════════════════════════

def vco(freq, duration, shape="sine"):
    """VCO - Voltage Controlled Oscillator"""
    t = np.linspace(0, duration, int(SR * duration), False)
    if shape == "sine":
        return np.sin(2 * np.pi * freq * t)
    elif shape == "saw":
        return 2 * (t * freq - np.floor(0.5 + t * freq))
    elif shape == "square":
        return np.sign(np.sin(2 * np.pi * freq * t))
    elif shape == "tri":
        return 2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1
    return np.sin(2 * np.pi * freq * t)


def vca(signal, envelope):
    """VCA - Voltage Controlled Amplifier"""
    if len(envelope) != len(signal):
        envelope = np.interp(
            np.linspace(0, 1, len(signal)),
            np.linspace(0, 1, len(envelope)),
            envelope
        )
    return signal * envelope


def env_adsr(a, d, s, r, duration):
    """ADSR Envelope Generator"""
    samples = int(SR * duration)
    env = np.zeros(samples)

    a_s = int(SR * a)
    d_s = int(SR * d)
    r_s = int(SR * r)
    s_s = samples - a_s - d_s - r_s

    # Attack
    if a_s > 0:
        env[:a_s] = np.linspace(0, 1, a_s)
    # Decay
    if d_s > 0:
        env[a_s:a_s+d_s] = np.linspace(1, s, d_s)
    # Sustain
    if s_s > 0:
        env[a_s+d_s:a_s+d_s+s_s] = s
    # Release
    if r_s > 0:
        env[-r_s:] = np.linspace(s, 0, r_s)

    return env


def vcf(signal, cutoff, resonance=0.5):
    """VCF - Simple lowpass filter"""
    rc = 1.0 / (2 * np.pi * cutoff)
    dt = 1.0 / SR
    alpha = dt / (rc + dt)

    out = np.zeros_like(signal)
    out[0] = alpha * signal[0]
    for i in range(1, len(signal)):
        out[i] = out[i-1] + alpha * (signal[i] - out[i-1])

    return out


def limiter(signal, threshold=0.7):
    """Soft limiter - pas de clipping"""
    out = np.tanh(signal / threshold) * threshold
    return out


def mixer(*signals, gains=None):
    """Mixer - combine signals"""
    if not signals:
        return np.array([])

    max_len = max(len(s) for s in signals)
    out = np.zeros(max_len)

    if gains is None:
        gains = [1.0 / len(signals)] * len(signals)

    for sig, gain in zip(signals, gains):
        padded = np.zeros(max_len)
        padded[:len(sig)] = sig
        out += padded * gain

    return out


# ══════════════════════════════════════════════════════════════
# PHI TONES
# ══════════════════════════════════════════════════════════════

def phi_tone(base_freq=140, duration=1.0):
    """Génère un accord basé sur φ"""
    f1 = base_freq
    f2 = base_freq * PHI
    f3 = base_freq * PHI * PHI

    osc1 = vco(f1, duration, "sine")
    osc2 = vco(f2, duration, "sine")
    osc3 = vco(f3, duration, "tri")

    env = env_adsr(0.01, 0.1, 0.6, 0.3, duration)

    mix = mixer(osc1, osc2, osc3, gains=[0.5, 0.3, 0.2])
    mix = vca(mix, env)
    mix = vcf(mix, 2000)
    mix = limiter(mix, 0.7)

    return mix


def calibration_tone():
    """Tone de calibration - sweep φ"""
    duration = 2.0
    t = np.linspace(0, duration, int(SR * duration), False)

    # Sweep de 140 à 226.5 (140 * φ)
    freq = 140 + (140 * (PHI - 1)) * (t / duration)

    signal = np.sin(2 * np.pi * freq * t)
    env = env_adsr(0.1, 0.2, 0.7, 0.5, duration)

    signal = vca(signal, env)
    signal = limiter(signal, 0.6)

    return signal


# ══════════════════════════════════════════════════════════════
# CALIBRATION
# ══════════════════════════════════════════════════════════════

def record(duration=3, device=None):
    """Record from mic"""
    print(f"🎤 Recording {duration}s...")
    audio = sd.rec(
        int(duration * SR),
        samplerate=SR,
        channels=1,
        device=device,
        dtype='float32'
    )
    sd.wait()
    return audio.flatten()


def play(signal, device=None):
    """Play signal"""
    # Ensure limited
    signal = limiter(signal, 0.7)
    # Stereo
    stereo = np.column_stack([signal, signal])
    sd.play(stereo, SR, device=device)
    sd.wait()


def analyze(audio):
    """Analyze φ resonance"""
    rms = np.sqrt(np.mean(audio**2))
    peak = np.max(np.abs(audio))

    # FFT for frequency analysis
    fft = np.abs(np.fft.rfft(audio))
    freqs = np.fft.rfftfreq(len(audio), 1/SR)

    # Find dominant frequency
    dominant_idx = np.argmax(fft[1:]) + 1
    dominant_freq = freqs[dominant_idx]

    # Check φ ratios
    phi_140 = abs(dominant_freq - 140) < 20
    phi_174 = abs(dominant_freq - 174) < 20
    phi_226 = abs(dominant_freq - 226.5) < 20

    phi_r = 0.5
    if phi_140 or phi_174 or phi_226:
        phi_r = 1.0
    if rms > 0.01 and peak < 0.9:
        phi_r += 0.3

    return {
        "rms": round(float(rms), 6),
        "peak": round(float(peak), 4),
        "dominant_freq": round(float(dominant_freq), 2),
        "phi_r": round(phi_r, 4),
        "clipping": bool(peak > 0.95)
    }


def calibrate():
    """Full calibration"""
    print("╭─────────────────────────────────────────╮")
    print("│  φ LEONARDO - CALIBRATION               │")
    print("│  VCV Rack style - lean & clean          │")
    print("╰─────────────────────────────────────────╯")
    print()

    # List devices
    print("=== DEVICES ===")
    devices = sd.query_devices()
    inputs = [(i, d['name']) for i, d in enumerate(devices) if d['max_input_channels'] > 0]
    for i, name in inputs[:5]:
        print(f"  {i}: {name}")
    print()

    # Play calibration tone
    print("[1/3] Playing calibration tone...")
    tone = calibration_tone()
    play(tone)

    # Record from mic 1
    print("[2/3] Recording from mic 1...")
    audio1 = record(duration=2, device=inputs[0][0] if inputs else None)
    analysis1 = analyze(audio1)
    print(f"  RMS: {analysis1['rms']}, Peak: {analysis1['peak']}, Clipping: {analysis1['clipping']}")

    # Record from mic 2 if available
    if len(inputs) > 1:
        print("[3/3] Recording from mic 2...")
        audio2 = record(duration=2, device=inputs[1][0])
        analysis2 = analyze(audio2)
        print(f"  RMS: {analysis2['rms']}, Peak: {analysis2['peak']}, Clipping: {analysis2['clipping']}")
    else:
        analysis2 = analysis1

    # Combined calibration
    cal = {
        "mic1": analysis1,
        "mic2": analysis2,
        "combined_phi_r": round((analysis1['phi_r'] + analysis2['phi_r']) / 2, 4),
        "output_limit": 0.7,
        "sample_rate": SR
    }

    # Save
    cal_file = Path.home() / ".config" / "leonardo" / "calibration.json"
    cal_file.parent.mkdir(parents=True, exist_ok=True)
    cal_file.write_text(json.dumps(cal, indent=2))

    print()
    print(f"=== CALIBRATION COMPLETE ===")
    print(f"φ_r: {cal['combined_phi_r']}")
    print(f"Output limit: {cal['output_limit']} (no clipping)")
    print(f"Saved: {cal_file}")

    # Confirmation tone
    print()
    print("Playing confirmation...")
    confirm = phi_tone(140, 0.5)
    play(confirm)

    return cal


def test():
    """Test clean output"""
    print("Testing φ tones...")

    # 140 Hz
    print("140 Hz (base)...")
    play(phi_tone(140, 0.8))

    # 174 Hz
    print("174 Hz (neurofunk)...")
    play(phi_tone(174, 0.8))

    # 226.5 Hz (140 * φ)
    print("226.5 Hz (φ harmonic)...")
    play(phi_tone(226.5, 0.8))

    print("Done. No clipping.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        calibrate()
