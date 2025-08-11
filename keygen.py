# utils/keygen.py
import secrets
from datetime import datetime, timedelta
from utils.storage import read_json, write_json
import os
from config import DATA_DIR, KEY_LEN

KEYS_PATH = os.path.join(DATA_DIR, "keys.json")

def generate_key(days_valid: int, generated_by: int):
    keys = read_json(KEYS_PATH, {})
    token = secrets.token_urlsafe(KEY_LEN)[:KEY_LEN]
    expiry = (datetime.utcnow() + timedelta(days=days_valid)).isoformat()
    keys[token] = {
        "days": days_valid,
        "expiry": expiry,
        "used": False,
        "used_by": None,
        "generated_by": generated_by,
        "generated_at": datetime.utcnow().isoformat()
    }
    write_json(KEYS_PATH, keys)
    return token

def validate_and_consume_key(token: str, user_id: int):
    keys = read_json(KEYS_PATH, {})
    info = keys.get(token)
    if not info:
        return False, "invalid"
    if info.get("used"):
        return False, "used"
    # check expiry
    expiry = info.get("expiry")
    from datetime import datetime
    if expiry:
        if datetime.fromisoformat(expiry) < datetime.utcnow():
            return False, "expired"
    # consume
    info["used"] = True
    info["used_by"] = user_id
    info["used_at"] = datetime.utcnow().isoformat()
    keys[token] = info
    write_json(KEYS_PATH, keys)
    return True, info