from email import message
from urllib.parse import uses_params
import telebot as tb
from telebot import types
from telebot.types import InputFile


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

def but_bills():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    Bill = types.KeyboardButton(text="Обновить")
    Ops = types.KeyboardButton(text="В меню")
    keyboard.add(Bill, Ops)
    return keyboard

def but_choose_cards():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    Bill = types.KeyboardButton(text="История операций")
    Ops = types.KeyboardButton(text="Закрыть")
    keyboard.add(Bill, Ops)
    return keyboard

def but_operation():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    Bill = types.KeyboardButton(text="Перевод на карту")
    Suggest = types.KeyboardButton(text="Закрыть")
    News = types.KeyboardButton(text="Перевыпустить")
    Info = types.KeyboardButton(text="Заблокировать")
    A = types.KeyboardButton(text="Выбрать другую карту")
    O = types.KeyboardButton(text="В меню")
    keyboard.add(Bill, Suggest, News, Info, A, O)
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

def but_money_choose_bank(message):
    bot.send_mesage(message.chat.id, text = "Выберите банк:", reply_markup=but_empty())
    #сохранить ввод

def but_money_to(message):
    bot.send_mesage(message.chat.id, text = "Введите номер телефона или номер карты куда хотите перевести деньги", reply_markup=but_empty())
    #сохранить ввод

def but_money_you_good(message):
    bot.send_mesage(message.chat.id, text = "Перевод успешно осуществлен :)\nСпасибо за то, что пользуетесь нашей системой", reply_markup=but_empty())
    #сохранить ввод

def print_logo(message):
    bot.send_animation(message.chat.id, InputFile(r"C:\Users\USER\Documents\flexbank\content\FlexBank.gif"), caption='Здравствуйте! Я банкинг-бот Neo! Для начала работы пройдите авторизацию. \n Нажмите Да для продолжения.', reply_markup=but_main_menu())


@bot.message_handler(commands=['start'])
def handle_start(message):
    print_logo(message)

if __name__ == '__main__':
     bot.infinity_polling() #бесконечное выполнение