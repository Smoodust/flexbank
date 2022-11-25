import telebot as tb
from telebot import types
from enum import Enum

# class syntax
class State(Enum):
    authorize = 1
    main_menu = 2
    accounts = 3
    ops = 4
    concrete_card = 5

bot = tb.TeleBot("5815112728:AAHcJ_GcAXDAzemA731QYrKNY_w-leAWugI")

login = ''
password = ''

def start_authorize(message):
    bot.send_message(message.chat.id, "Здравствуйте, меня зовут Свинота! Введите свой *логин и пароль*:", parse_mode="Markdown")
    bot.

def start_main_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    Bill = types.KeyboardButton(text="Счета")
    Ops = types.KeyboardButton(text="Операции")
    Suggest = types.KeyboardButton(text="Предложения")
    News = types.KeyboardButton(text="Новости")
    Info = types.KeyboardButton(text="Помощь")
    keyboard.add(Bill, Info)
    return keyboard


def start_bill_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    Bill = types.KeyboardButton(text="Что-то")
    Back = types.KeyboardButton(text="Меню")
    keyboard.add(Bill, Back)
    return keyboard

@bot.message_handler(commands=['start'])
def Start(message):
    start_authorize(message)

    

if __name__ == '__main__':
    bot.infinity_polling()