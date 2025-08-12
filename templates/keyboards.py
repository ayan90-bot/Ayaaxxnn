from telebot import types

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("/redeem"))
markup.add(types.KeyboardButton("/premium"))
    return markup
