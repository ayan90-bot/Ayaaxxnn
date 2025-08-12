import os

# Environment se values le raha hai
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Please set BOT_TOKEN in environment variables.")

ADMIN_ID = os.environ.get("ADMIN_ID")
if not ADMIN_ID:
    raise ValueError("Please set ADMIN_ID in environment variables.")

DATA_FILE = os.environ.get("DATA_DIR", "data.json")  # Default agar env me na ho
KEYS_FILE = "keys.json"
