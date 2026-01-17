# -*- coding: utf-8 -*-
"""
l = immortal loop
never dies
hot reload
"""

import signal
import time
import os
import importlib

def immortal():
    """ignore all kill signals"""
    for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
        try:
            signal.signal(sig, lambda s, f: None)
        except:
            pass

def daemon(tick_fn, interval=1.0, reload_modules=None):
    """
    immortal daemon with hot reload
    touch .reload to reload modules without killing
    """
    immortal()
    reload_modules = reload_modules or []
    reload_file = ".reload"

    while True:
        try:
            # hot reload check
            if os.path.exists(reload_file):
                os.remove(reload_file)
                for mod in reload_modules:
                    try:
                        importlib.reload(mod)
                        print(f"reloaded: {mod.__name__}")
                    except Exception as e:
                        print(f"reload failed: {e}")

            # tick
            tick_fn()
            time.sleep(interval)

        except KeyboardInterrupt:
            pass  # immortal
        except Exception as e:
            print(f"error: {e}")
            time.sleep(interval)

def once(fn, *args, **kwargs):
    """run once, never fail"""
    try:
        return fn(*args, **kwargs)
    except:
        return None
