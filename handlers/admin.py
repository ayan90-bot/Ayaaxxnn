# handlers/admin.py
from config import ADMIN_IDS
from utils.storage import read_json, write_json
from utils.keygen import generate_key
import os
from config import DATA_DIR
from utils.notify import notify_admins

USERS_PATH = os.path.join(DATA_DIR, "users.json")

def register_admin(bot, global_state):
    # generate key: /genk <days>
    @bot.message_handler(commands=["genk"])
    def genk_cmd(message):
        if message.from_user.id not in ADMIN_IDS:
            return
        parts = message.text.split()
        if len(parts) < 2:
            bot.send_message(message.chat.id, "Usage: /genk <days>\nExample: /genk 7")
            return
        try:
            days = int(parts[1])
        except ValueError:
            bot.send_message(message.chat.id, "Days must be a number.")
            return
        token = generate_key(days, message.from_user.id)
        bot.send_message(message.chat.id, f"Key generated:\n`{token}`\nValid for {days} day(s).", parse_mode="Markdown")

    # broadcast: /broadcast text...
    @bot.message_handler(commands=["broadcast"])
    def broadcast_cmd(message):
        if message.from_user.id not in ADMIN_IDS:
            return
        text = message.text.partition(" ")[2].strip()
        if not text:
            bot.send_message(message.chat.id, "Usage: /broadcast <message>")
            return
        users = read_json(USERS_PATH, {})
        count = 0
        for uid_str in users.keys():
            try:
                bot.send_message(int(uid_str), text)
                count += 1
            except Exception:
                pass
        bot.send_message(message.chat.id, f"Broadcast sent to {count} users.")

    # ban user: /ban <user_id>
    @bot.message_handler(commands=["ban"])
    def ban_cmd(message):
        if message.from_user.id not in ADMIN_IDS:
            return
        parts = message.text.split()
        if len(parts) < 2:
            bot.send_message(message.chat.id, "Usage: /ban <user_id>")
            return
        uid = parts[1]
        users = read_json(USERS_PATH, {})
        users.setdefault(uid, {})
        users[uid]["banned"] = True
        write_json(USERS_PATH, users)
        bot.send_message(message.chat.id, f"User {uid} banned.")

    @bot.message_handler(commands=["unban"])
    def unban_cmd(message):
        if message.from_user.id not in ADMIN_IDS:
            return
        parts = message.text.split()
        if len(parts) < 2:
            bot.send_message(message.chat.id, "Usage: /unban <user_id>")
            return
        uid = parts[1]
        users = read_json(USERS_PATH, {})
        users.setdefault(uid, {})
        users[uid]["banned"] = False
        write_json(USERS_PATH, users)
        bot.send_message(message.chat.id, f"User {uid} unbanned.")

    # freeaccess: allow unlimited free redeems
    @bot.message_handler(commands=["freeaccess", "freeacces"])
    def freeaccess_cmd(message):
        if message.from_user.id not in ADMIN_IDS:
            return
        global_state["free_access"] = True
        bot.send_message(message.chat.id, "Free access enabled: free users can use /redeem unlimited times.")

    @bot.message_handler(commands=["banaccess", "banacces"])
    def banaccess_cmd(message):
        if message.from_user.id not in ADMIN_IDS:
            return
        global_state["free_access"] = False
        bot.send_message(message.chat.id, "Free access disabled: free users limited according to policy.")