from urllib.parse import uses_params
import telebot as tb
from telebot import types


bot = tb.TeleBot("5928558655:AAHOQcmlQTMJRVe_7IFEnAHHUw2qvvYhaZM")


def but_main_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    Bill = types.KeyboardButton(text="Счета")
    Suggest = types.KeyboardButton(text="Предложения")
    News = types.KeyboardButton(text="Новости")
    Info = types.KeyboardButton(text="Помощь")
    keyboard.add(Bill, Suggest, News, Info)
    return keyboard

def but_authorize():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    Bill = types.KeyboardButton(text="Я новый пользователь")
    Ops = types.KeyboardButton(text="Войти")
    keyboard.add(Bill, Ops)
    return keyboard

def but_empty():
    empty = types.ReplyKeyboardRemove()
    return empty


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, text = "Гандон", reply_markup=but_main_menu())

if __name__ == '__main__':
     bot.infinity_polling() #бесконечное выполнение