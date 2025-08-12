import os

# BOT_TOKEN from environment variable or hardcoded value
BOT_TOKEN = os.environ.get("BOT_TOKEN") or "8432298627:AAFMs_bn-x1S9ZrTSOICLiSxfCBQtBHHZfw"

# Admin IDs (list of integers)
ADMIN_IDS = os.environ.get("ADMIN_IDS", "6324825537").split(",")

# Data directory
DATA_DIR = os.environ.get("DATA_DIR", "data")

# Safety check
if not BOT_TOKEN or BOT_TOKEN == "PUT_YOUR_BOT_TOKEN_HERE":
    raise ValueError("Please set BOT_TOKEN in environment variable or config.py")
