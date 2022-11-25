from email import message
from telnetlib import SEND_URL
from urllib.parse import uses_params
import telebot as tb
from telebot import types
from telebot.types import InputFile

from backend import get_diff_transaction, get_sum_transaction


bot = tb.TeleBot("5928558655:AAHOQcmlQTMJRVe_7IFEnAHHUw2qvvYhaZM")
connection = backend.get_connection()

def but_main_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    Bill = types.KeyboardButton(text="Счета")
    Suggest = types.KeyboardButton(text="Предложения")
    News = types.KeyboardButton(text="Новости")
    Info = types.KeyboardButton(text="Помощь")
    keyboard.add(Bill, Suggest, News, Info)
    return keyboard

def but_offer():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    Ops = types.KeyboardButton(text="В меню")
    keyboard.add(Ops)
    return keyboard

def send_offers(message):
    if get_sum_transaction(connection, message.user.id )>2000000:
        bot.send_message(message.chat.id, text='За последний месяц вы сделали переводов на сумме превышающую 2 млн. рублей. Для того чтобы оформить вип статус перейдите по ссылке '+SEND_URL("http/exampe.com"))
    if get_diff_transaction (connection, message.user.id )<0:
        bot.send_message(message.chat.id, text='Ваши траты за последнйи месяц превысили ваш доход. Наш банк предлагает оформить кредитную карту с увеличенным рассрочным периодом. Если хотите оформить перейдите оп ссылкке: '+SEND_URL("http/exampe.com"))
    bot.send_message(message.chat.id, text='Flexbank для всех новых пользователей предлагает ипотеку под пониженный процент. Если хотите оформить перейдите по ссылке: '+SEND_URL("http/exampe.com"))

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, reply_markup=but_main_menu)

@bot.message_handler(chat_types=['text'])
def bills(message):
    if message.text == 'В меню':
        bot.send_message(message.chat.id, reply_markup=but_main_menu)
    elif message.text == 'Предложения':
        send_offers(message);
        bot.send_message(message.chat.id, reply_markup=but_offer)

if __name__ == '__main__':
     bot.infinity_polling() #бесконечное выполнение