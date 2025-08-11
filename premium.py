# handlers/premium.py
from utils.keygen import validate_and_consume_key
from utils.storage import read_json, write_json
from utils.notify import notify_admins
import os
from config import DATA_DIR
from datetime import datetime, timedelta

USERS_PATH = os.path.join(DATA_DIR, "users.json")

def register_premium(bot, admin_ids):
    @bot.message_handler(commands=["premium"])
    def premium_cmd(message):
        # ask for key (we'll expect user to send the key as next message)
        msg = bot.send_message(message.chat.id, "Send your premium key (paste it here):")
        bot.register_next_step_handler(msg, process_key)

    def process_key(message):
        token = message.text.strip()
        uid = message.from_user.id
        ok, info = validate_and_consume_key(token, uid)
        if not ok:
            bot.send_message(uid, "Invalid or used/expired key.")
            return
        # info contains days, expiry, generated_by
        days = info.get("days", 0)
        expiry_iso = (datetime.utcnow() + timedelta(days=days)).isoformat() if days else None
        users = read_json(USERS_PATH, {})
        users[str(uid)] = users.get(str(uid), {})
        users[str(uid)].update({
            "id": uid,
            "is_premium": True,
            "premium_expiry": expiry_iso,
            "redeemed_once": users.get(str(uid), {}).get("redeemed_once", False),
            "banned": users.get(str(uid), {}).get("banned", False)
        })
        write_json(USERS_PATH, users)
        bot.send_message(uid, "Premium Activated ⚡️")
        # notify admin that user activated premium (do not reveal private text)
        notify_text = f"User {message.from_user.id} ({message.from_user.username or 'no-username'}) activated premium for {days} day(s)."
        notify_admins(bot, notify_text)