# templates/keyboards.py
from telebot import types

def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(types.KeyboardButton("Account Generator 🧩"), types.KeyboardButton("AI Assist 🤖"))
    kb.row(types.KeyboardButton("Get Methods 👑"), types.KeyboardButton("Saved Accounts ♻️"))
    return kb

def quick_buttons():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Account Generator 🧩", callback_data="gen_ac"))
    kb.add(types.InlineKeyboardButton("AI Assist 🤖", callback_data="ai_assist"))
    return kb