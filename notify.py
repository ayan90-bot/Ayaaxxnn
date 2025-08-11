 # utils/notify.py
from config import ADMIN_IDS

def notify_admins(bot, text, disable_notification=True):
    for admin in ADMIN_IDS:
        try:
            bot.send_message(admin, text, disable_notification=disable_notification)
        except Exception:
            pass