import os

# BOT Token from env var or fallback
BOT_TOKEN = os.getenv("BOT_TOKEN", "yaha_apna_bot_token_dal")

# Admin ID from env var or fallback
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))

# File paths
DATA_FILE = os.getenv("DATA_FILE", "data.json")
KEYS_FILE = os.getenv("KEYS_FILE", "keys.json")

# Safety check
if BOT_TOKEN == "yaha_apna_bot_token_dal":
    raise ValueError("Please set BOT_TOKEN in config.py or as an environment variable.")
