import os
import json

def _ensure_file(path, default_content=None):
    """
    Agar file exist nahi karti to create karo,
    aur default_content likho agar diya hai.
    """
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            if default_content is None:
                default_content = {}
            json.dump(default_content, f)

def read_json(path, default=None):
    """
    JSON file read karo, agar error aaya to default return karo.
    """
    if not os.path.exists(path):
        return default if default is not None else {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default if default is not None else {}

def write_json(path, data):
    """
    Data ko JSON file me write karo.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
