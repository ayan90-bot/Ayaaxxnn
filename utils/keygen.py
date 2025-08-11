import random, string, time
from .storage import read_json, write_json
from .config import KEYS_FILE

def generate_key(days):
    keys = read_json(KEYS_FILE)
    key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    keys[key] = {
        "days": days,
        "created": int(time.time()),
        "used": False
    }
    write_json(KEYS_FILE, keys)
    return key

def validate_and_consume_key(key):
    keys = read_json(KEYS_FILE)
    if key in keys and not keys[key]["used"]:
        keys[key]["used"] = True
        write_json(KEYS_FILE, keys)
        return keys[key]["days"]
    return None
