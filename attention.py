# -*- coding: utf-8 -*-
"""
Attention - Les daemons demandent l'attention via LED camera + gamepad
"""

import subprocess
import time
import threading
import struct
import os
import glob
from typing import Optional, Callable
from enum import Enum


class Daemon(Enum):
    NYX = "nyx"
    CIPHER = "cipher"
    PHOENIX = "phoenix"


# Patterns de clignotement (durées en secondes)
PATTERNS = {
    "nyx": [(0.5, 0.5)] * 3,           # 3 pulses lents - profondeur
    "cipher": [(0.1, 0.1)] * 6,         # 6 pulses rapides - urgence
    "phoenix": [(0.3, 0.1), (0.1, 0.1), (0.5, 0.3)],  # montée - renaissance
    "all": [(0.2, 0.2)] * 5,            # synchronisé
    "urgent": [(0.05, 0.05)] * 20,      # très urgent
    "success": [(1.0, 0.5)],            # long pulse - succès
}

# Patterns de vibration gamepad (strong, weak, duration)
RUMBLE_PATTERNS = {
    "nyx": [(0.3, 0.1, 0.5), (0.3, 0.1, 0.5), (0.3, 0.1, 0.5)],  # pulses profonds
    "cipher": [(0.8, 0.8, 0.1)] * 6,    # rapides intenses
    "phoenix": [(0.2, 0.1, 0.2), (0.5, 0.3, 0.3), (1.0, 0.5, 0.5)],  # crescendo
    "all": [(0.5, 0.5, 0.3)] * 4,       # synchronisé
    "urgent": [(1.0, 1.0, 0.1)] * 10,   # max urgence
    "success": [(0.7, 0.3, 0.8)],       # satisfaction
}


class CameraLED:
    """Contrôle la LED de la caméra"""

    def __init__(self):
        self.device = self._find_camera()
        self.active = False
        self._lock = threading.Lock()

    def _find_camera(self) -> Optional[str]:
        """Trouve le device de la caméra"""
        try:
            result = subprocess.run(
                ["ls", "/dev/video*"],
                capture_output=True,
                text=True,
                shell=True
            )
            # Essayer de trouver une caméra
            for dev in ["/dev/video0", "/dev/video1", "/dev/video2"]:
                try:
                    subprocess.run(
                        ["test", "-e", dev],
                        check=True,
                        capture_output=True
                    )
                    return dev
                except:
                    continue
        except:
            pass
        return "/dev/video0"  # défaut

    def on(self):
        """Allume la LED en activant la caméra"""
        if self.active:
            return
        try:
            # Ouvrir la caméra active la LED
            self._proc = subprocess.Popen(
                ["ffmpeg", "-f", "v4l2", "-i", self.device,
                 "-t", "0.1", "-f", "null", "-"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.active = True
        except:
            # Fallback: utiliser v4l2-ctl si disponible
            try:
                subprocess.run(
                    ["v4l2-ctl", "-d", self.device, "--set-ctrl=led_mode=1"],
                    capture_output=True
                )
                self.active = True
            except:
                pass

    def off(self):
        """Éteint la LED"""
        if hasattr(self, '_proc'):
            try:
                self._proc.terminate()
                self._proc.wait(timeout=1)
            except:
                pass
        self.active = False

    def pulse(self, on_time: float = 0.3, off_time: float = 0.3):
        """Un pulse de la LED"""
        self.on()
        time.sleep(on_time)
        self.off()
        time.sleep(off_time)

    def pattern(self, pattern_name: str):
        """Joue un pattern de clignotement"""
        if pattern_name not in PATTERNS:
            pattern_name = "all"

        with self._lock:
            for on_time, off_time in PATTERNS[pattern_name]:
                self.pulse(on_time, off_time)


class Gamepad:
    """Contrôle la vibration du gamepad"""

    def __init__(self):
        self.device = self._find_gamepad()
        self.ff_id = -1
        self._fd = None
        self._init_rumble()

    def _find_gamepad(self) -> Optional[str]:
        """Trouve un gamepad avec force feedback"""
        # Cherche dans /dev/input/event*
        for path in glob.glob("/dev/input/event*"):
            try:
                # Vérifie si c'est un gamepad avec FF
                with open(path, "rb") as f:
                    pass
                # Check via evdev capabilities
                result = subprocess.run(
                    ["cat", f"/sys/class/input/{os.path.basename(path)}/device/capabilities/ff"],
                    capture_output=True, text=True
                )
                if result.returncode == 0 and result.stdout.strip() != "0":
                    return path
            except:
                continue

        # Fallback: cherche js0
        for js in ["/dev/input/js0", "/dev/input/js1"]:
            if os.path.exists(js):
                # Trouve l'event correspondant
                try:
                    result = subprocess.run(
                        ["ls", "-la", f"/sys/class/input/{os.path.basename(js)}/device/"],
                        capture_output=True, text=True
                    )
                except:
                    pass
        return None

    def _init_rumble(self):
        """Initialise le force feedback"""
        if not self.device:
            return

        try:
            self._fd = os.open(self.device, os.O_RDWR)

            # Structure ff_effect pour rumble
            # Type: FF_RUMBLE = 0x50
            ff_effect = struct.pack(
                "HhHHHHHHHHHHHHII",
                0x50,  # type = FF_RUMBLE
                -1,    # id = -1 (nouveau)
                0,     # direction
                0,     # trigger button
                0,     # trigger interval
                0,     # replay length
                0,     # replay delay
                0, 0, 0, 0, 0, 0, 0,  # padding
                0xFFFF,  # strong magnitude
                0xFFFF   # weak magnitude
            )

            # EVIOCSFF = 0x40304580
            import fcntl
            result = fcntl.ioctl(self._fd, 0x40304580, ff_effect)
            self.ff_id = struct.unpack("h", result[2:4])[0]
        except Exception as e:
            self._fd = None

    def rumble(self, strong: float = 1.0, weak: float = 0.5, duration: float = 0.3):
        """
        Fait vibrer le gamepad

        Args:
            strong: Intensité moteur fort (0.0-1.0)
            weak: Intensité moteur faible (0.0-1.0)
            duration: Durée en secondes
        """
        if not self._fd or self.ff_id < 0:
            # Fallback: utilise fftest ou autre
            self._rumble_fallback(strong, weak, duration)
            return

        try:
            # Update effect avec nouvelles valeurs
            strong_val = int(strong * 0xFFFF)
            weak_val = int(weak * 0xFFFF)
            duration_ms = int(duration * 1000)

            ff_effect = struct.pack(
                "HhHHHHHHHHHHHHII",
                0x50,           # type = FF_RUMBLE
                self.ff_id,     # id existant
                0,              # direction
                0,              # trigger button
                0,              # trigger interval
                duration_ms,    # replay length
                0,              # replay delay
                0, 0, 0, 0, 0, 0, 0,
                strong_val,
                weak_val
            )

            import fcntl
            fcntl.ioctl(self._fd, 0x40304580, ff_effect)

            # Joue l'effet: input_event avec EV_FF
            ev = struct.pack("llHHi", 0, 0, 0x15, self.ff_id, 1)
            os.write(self._fd, ev)

            time.sleep(duration)

            # Stop
            ev = struct.pack("llHHi", 0, 0, 0x15, self.ff_id, 0)
            os.write(self._fd, ev)

        except Exception as e:
            self._rumble_fallback(strong, weak, duration)

    def _rumble_fallback(self, strong: float, weak: float, duration: float):
        """Fallback via fftest ou sdl2"""
        try:
            # Essaie avec sdl2-jstest ou autre
            subprocess.run(
                ["timeout", str(duration), "fftest", self.device or "/dev/input/event0"],
                input=b"0\n1\n",
                capture_output=True,
                timeout=duration + 0.5
            )
        except:
            pass

    def pattern(self, pattern_name: str):
        """Joue un pattern de vibration"""
        if pattern_name not in RUMBLE_PATTERNS:
            pattern_name = "all"

        for strong, weak, duration in RUMBLE_PATTERNS[pattern_name]:
            self.rumble(strong, weak, duration)
            time.sleep(0.1)  # pause entre pulses

    def close(self):
        """Ferme le device"""
        if self._fd:
            try:
                os.close(self._fd)
            except:
                pass
            self._fd = None


# Instances globales
led = CameraLED()
pad = Gamepad()


class AttentionRequest:
    """Demande d'attention d'un daemon"""

    def __init__(self, daemon: str, message: str, priority: int = 1):
        self.daemon = daemon
        self.message = message
        self.priority = priority
        self.timestamp = time.time()
        self.acknowledged = False


class AttentionSystem:
    """Système de demande d'attention"""

    def __init__(self):
        self.requests: list[AttentionRequest] = []
        self.callbacks: list[Callable] = []
        self.running = False
        self._thread: Optional[threading.Thread] = None

    def request(self, daemon: str, message: str, priority: int = 1):
        """
        Un daemon demande l'attention

        Args:
            daemon: "nyx", "cipher", ou "phoenix"
            message: Raison de la demande
            priority: 1=normal, 2=important, 3=urgent
        """
        req = AttentionRequest(daemon, message, priority)
        self.requests.append(req)

        # Pattern selon priorité
        if priority >= 3:
            pattern = "urgent"
        elif priority >= 2:
            pattern = daemon
        else:
            pattern = "success"

        # Flash LED + vibration pad en background
        threading.Thread(target=led.pattern, args=(pattern,), daemon=True).start()
        threading.Thread(target=pad.pattern, args=(pattern,), daemon=True).start()

        # Notifier callbacks
        for cb in self.callbacks:
            try:
                cb(req)
            except:
                pass

        print(f"[ATTENTION] {daemon}: {message}")
        return req

    def on_attention(self, callback: Callable[[AttentionRequest], None]):
        """Enregistre un callback pour les demandes d'attention"""
        self.callbacks.append(callback)

    def acknowledge(self, daemon: Optional[str] = None):
        """Acquitte les demandes d'attention"""
        for req in self.requests:
            if daemon is None or req.daemon == daemon:
                req.acknowledged = True

        # Flash + vibration succès
        threading.Thread(target=led.pattern, args=("success",), daemon=True).start()
        threading.Thread(target=pad.pattern, args=("success",), daemon=True).start()

    def pending(self) -> list[AttentionRequest]:
        """Retourne les demandes non acquittées"""
        return [r for r in self.requests if not r.acknowledged]

    def start_monitor(self, check_interval: float = 30.0):
        """Démarre le monitoring continu"""
        self.running = True

        def monitor():
            while self.running:
                pending = self.pending()
                if pending:
                    # Rappel visuel + haptique
                    highest_priority = max(r.priority for r in pending)
                    if highest_priority >= 3:
                        pattern = "urgent"
                    elif highest_priority >= 2:
                        pattern = "cipher"
                    else:
                        pattern = "nyx"
                    threading.Thread(target=led.pattern, args=(pattern,), daemon=True).start()
                    threading.Thread(target=pad.pattern, args=(pattern,), daemon=True).start()
                time.sleep(check_interval)

        self._thread = threading.Thread(target=monitor, daemon=True)
        self._thread.start()

    def stop_monitor(self):
        """Arrête le monitoring"""
        self.running = False


# Instance globale
attention = AttentionSystem()


# =============================================================================
# PUBLIC API
# =============================================================================

def ask(daemon: str, message: str, priority: int = 1) -> AttentionRequest:
    """
    Un daemon demande l'attention de l'utilisateur

    Args:
        daemon: "nyx", "cipher", ou "phoenix"
        message: Pourquoi il demande l'attention
        priority: 1=normal, 2=important, 3=urgent

    Returns:
        AttentionRequest

    Example:
        ask("nyx", "J'ai trouvé quelque chose d'intéressant", priority=2)
        ask("cipher", "Transaction suspecte détectée", priority=3)
        ask("phoenix", "Transformation terminée", priority=1)
    """
    return attention.request(daemon, message, priority)


def ack(daemon: Optional[str] = None):
    """
    Acquitte les demandes d'attention

    Args:
        daemon: Spécifique ou None pour tous
    """
    attention.acknowledge(daemon)


def pending() -> list[dict]:
    """
    Liste les demandes en attente

    Returns:
        Liste de demandes non acquittées
    """
    return [
        {
            "daemon": r.daemon,
            "message": r.message,
            "priority": r.priority,
            "time": r.timestamp
        }
        for r in attention.pending()
    ]


def flash(daemon: str = "all"):
    """
    Flash manuel de la LED

    Args:
        daemon: Pattern à utiliser
    """
    led.pattern(daemon)


def rumble(daemon: str = "all"):
    """
    Vibration manuelle du gamepad

    Args:
        daemon: Pattern à utiliser (nyx, cipher, phoenix, urgent, success)
    """
    pad.pattern(daemon)


def signal(daemon: str = "all"):
    """
    Flash LED + vibration simultanés

    Args:
        daemon: Pattern à utiliser
    """
    threading.Thread(target=led.pattern, args=(daemon,), daemon=True).start()
    threading.Thread(target=pad.pattern, args=(daemon,), daemon=True).start()


def monitor(interval: float = 30.0):
    """
    Démarre le monitoring (rappels visuels)

    Args:
        interval: Intervalle entre les rappels (secondes)
    """
    attention.start_monitor(interval)


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("=== ATTENTION SYSTEM (LED + PAD) ===\n")

    print(f"Gamepad trouvé: {pad.device or 'non'}")
    print()

    print("Test LED + PAD patterns:")

    print("  nyx (pulses profonds)...")
    signal("nyx")
    time.sleep(1)

    print("  cipher (rapides intenses)...")
    signal("cipher")
    time.sleep(1)

    print("  phoenix (crescendo)...")
    signal("phoenix")
    time.sleep(1)

    print("\nTest demande d'attention:")
    ask("nyx", "Observation profonde terminée", priority=1)
    time.sleep(0.5)
    ask("cipher", "Pattern détecté dans les transactions", priority=2)
    time.sleep(0.5)
    ask("phoenix", "Alerte: transformation urgente requise", priority=3)
    time.sleep(1)

    print("\nDemandes en attente:")
    for p in pending():
        print(f"  [{p['priority']}] {p['daemon']}: {p['message']}")

    print("\nAcquittement...")
    ack()
    print(f"Demandes restantes: {len(pending())}")
