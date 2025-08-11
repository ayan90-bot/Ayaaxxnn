# config.py
import os
from datetime import timedelta

# Telegram bot token
BOT_TOKEN = os.getenv("BOT_TOKEN", "REPLACE_WITH_YOUR_BOT_TOKEN")

# Admin IDs (list of ints). Replace with your Telegram user id(s)
ADMIN_IDS = [123456789]  # <-- put your telegram id(s) here

# Default directory for data (relative)
DATA_DIR = "data"

# Redeem settings
FREE_USER_ONE_TIME = True   # default: free users can redeem only 1 time (unless free_access toggle enabled)
PROCESSING_MESSAGE = "Processing..."
PURCHASE_PROMPT = "please Purchase Premium Key For Use 🗝️"
REDEEM_FORWARD_PREFIX = "User used /redeem — forwarded message:"

# Key length (characters)
KEY_LEN = 16

# Premium default timezone/expiry helper
PREMIUM_DAY_UNIT = timedelta(days=1)