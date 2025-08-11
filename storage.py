# utils/storage.py
import json
import os
import threading

_lock = threading.Lock()

def _ensure_file(path, default):
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f)

def read_json(path, default=None):
    if default is None:
        default = {}
    _ensure_file(path, default)
    with _lock:
        with open(path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                return default

def write_json(path, data):
    _ensure_file(path, data)
    with _lock:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)