# handlers/start.py
from telebot import types
from templates.keyboards import main_menu

START_TEXT = ("Welcome To Aizen Bot ⚡️\n\n"
              "Please Use this /redeem Command For Get Prime video 🧑‍💻\n"
              "For Premium use This Command /premium")

def register_start(bot):
    @bot.message_handler(commands=["start"])
    def start_cmd(message):
        bot.send_message(message.chat.id, START_TEXT, reply_markup=main_menu())