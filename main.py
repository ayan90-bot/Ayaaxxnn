import sys
import os
sys.path.append(os.path.dirname(__file__))
# main.py
import telebot
from flask import Flask
import threading
import time
import os
from config import BOT_TOKEN, ADMIN_IDS, DATA_DIR
from handlers.start import register_start
from handlers.redeem import register_redeem
from handlers.premium import register_premium
from handlers.admin import register_admin
from templates.keyboards import main_menu
from utils.storage import read_json, write_json
from utils.notify import notify_admins

# Setup simple global state
global_state = {
    "free_access": False
}

# ensure data dir exists and json files
os.makedirs(DATA_DIR, exist_ok=True)
users_path = os.path.join(DATA_DIR, "users.json")
keys_path = os.path.join(DATA_DIR, "keys.json")
# initialize if needed
from utils.storage import _ensure_file
_try_default = {}
_ensure_file(users_path, {})
_ensure_file(keys_path, {})

if BOT_TOKEN == "REPLACE_WITH_YOUR_BOT_TOKEN" or not BOT_TOKEN:
    raise SystemExit("Please set BOT_TOKEN in config.py or environment variable.")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# register handlers
register_start(bot)
register_redeem(bot, ADMIN_IDS, global_state)
register_premium(bot, ADMIN_IDS)
register_admin(bot, global_state)

# small health-check Flask app (we won't use webhook)
app = Flask(__name__)

@app.route("/")
def home():
    return "AizenBot Running (polling mode)"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))

def run_polling():
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=90)
        except Exception as e:
            print("Polling error, retrying in 5s:", e)
            time.sleep(5)

if __name__ == "__main__":
    t1 = threading.Thread(target=run_flask)
    t1.daemon = True
    t1.start()

    print("Starting bot polling...")
    run_polling()
