import telebot as tb
from telebot import types


bot = tb.TeleBot("5928558655:AAHOQcmlQTMJRVe_7IFEnAHHUw2qvvYhaZM")
input = 0
login = ''
password = ''
def start_main_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    Bill = types.KeyboardButton(text="Впервые")
    Info = types.KeyboardButton(text="Войти")
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
    bot.send_message(message.chat.id, message.text, reply_markup=start_main_menu())

@bot.message_handler(content_types=['text'])
def Check_Message(message):
    if message.text == 'Меню':
        bot.send_message(message.chat.id, message.text, reply_markup=start_main_menu())
    elif message.text == 'Счет':
        bot.send_message(message.chat.id, message.text, reply_markup=start_bill_menu())
    elif input == 1:
        login = message.text
    elif input == 2:
        password = message.text
        input = 0
    elif message.text == "Войти":
        input = 1

if __name__ == '__main__':
    bot.infinity_polling()