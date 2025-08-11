# handlers/redeem.py
from config import DATA_DIR, FREE_USER_ONE_TIME, PROCESSING_MESSAGE, PURCHASE_PROMPT, REDEEM_FORWARD_PREFIX
from utils.storage import read_json, write_json
from utils.notify import notify_admins
import os
from datetime import datetime
import json

USERS_PATH = os.path.join(DATA_DIR, "users.json")

def register_redeem(bot, admin_ids, global_state):
    @bot.message_handler(commands=["redeem"])
    def redeem_cmd(message):
        uid = message.from_user.id
        users = read_json(USERS_PATH, {})
        user = users.get(str(uid), {
            "id": uid,
            "is_premium": False,
            "premium_expiry": None,
            "redeemed_once": False,
            "banned": False
        })

        # banned check
        if user.get("banned"):
            bot.send_message(uid, "You are banned from using this bot.")
            return

        # if user is premium -> allow
        if user.get("is_premium"):
            # forward message to admin(s)
            forward_text = f"{REDEEM_FORWARD_PREFIX} @{message.from_user.username or message.from_user.id}"
            try:
                # forward the user's full message
                for a in admin_ids:
                    try:
                        bot.forward_message(a, message.chat.id, message.message_id)
                    except Exception:
                        # if forward fails, send short notify
                        bot.send_message(a, forward_text)
            except Exception:
                pass

            bot.send_message(uid, PROCESSING_MESSAGE)
            # Here, put whatever logic to give the resource.
            bot.send_message(uid, "Redeem processed. (premium user)")

            # update user record (touch)
            users[str(uid)] = user
            write_json(USERS_PATH, users)
            return

        # if free access globally enabled
        if global_state.get("free_access"):
            # allow unlimited for free users
            try:
                for a in admin_ids:
                    try:
                        bot.forward_message(a, message.chat.id, message.message_id)
                    except Exception:
                        bot.send_message(a, REDEEM_FORWARD_PREFIX)
            except Exception:
                pass
            bot.send_message(uid, PROCESSING_MESSAGE)
            bot.send_message(uid, "Redeem processed. (free-access enabled)")
            users[str(uid)] = user
            write_json(USERS_PATH, users)
            return

        # default: free users only one-time (if FREE_USER_ONE_TIME True)
        if FREE_USER_ONE_TIME:
            if user.get("redeemed_once"):
                bot.send_message(uid, PURCHASE_PROMPT)
                return
            # first time free redeem
            try:
                for a in admin_ids:
                    try:
                        bot.forward_message(a, message.chat.id, message.message_id)
                    except Exception:
                        bot.send_message(a, REDEEM_FORWARD_PREFIX)
            except Exception:
                pass

            bot.send_message(uid, PROCESSING_MESSAGE)
            bot.send_message(uid, "Redeem processed. (free user - one time)")

            user["redeemed_once"] = True
            users[str(uid)] = user
            write_json(USERS_PATH, users)
            return

        # fallback: if not allowed
        bot.send_message(uid, PURCHASE_PROMPT)