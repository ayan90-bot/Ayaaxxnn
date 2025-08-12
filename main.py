import os
import telebot
from telebot import types

# ================= CONFIG =================
BOT_TOKEN = os.environ.get("BOT_TOKEN") or "8432298627:AAFMs_bn-x1S9ZrTSOICLiSxfCBQtBHHZfw"
ADMIN_IDS = os.environ.get("ADMIN_IDS", "6324825537").split(",")
DATA_DIR = os.environ.get("DATA_DIR", "data")

if not BOT_TOKEN or BOT_TOKEN == "PUT_YOUR_BOT_TOKEN_HERE":
    raise ValueError("❌ Please set BOT_TOKEN in Render environment variables or in main.py directly.")

# ================= INIT BOT =================
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# ================= COMMAND HANDLERS =================
@bot.message_handler(commands=["start"])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Option 1"), types.KeyboardButton("Option 2"))
    bot.send_message(message.chat.id, "✅ Bot is running!\nChoose an option below:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "Option 1")
def handle_option1(message):
    bot.send_message(message.chat.id, "You selected Option 1 ✅")

@bot.message_handler(func=lambda msg: msg.text == "Option 2")
def handle_option2(message):
    bot.send_message(message.chat.id, "You selected Option 2 ✅")

# ================= ADMIN TEST =================
@bot.message_handler(commands=["admin"])
def admin_check(message):
    if str(message.chat.id) in ADMIN_IDS:
        bot.send_message(message.chat.id, "👑 You are an admin.")
    else:
        bot.send_message(message.chat.id, "❌ You are not an admin.")

# ================= START BOT =================
if __name__ == "__main__":
    print("🚀 Bot is starting...")
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=30)
    except Exception as e:
        print(f"❌ Error: {e}")
