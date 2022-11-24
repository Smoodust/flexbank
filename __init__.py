import telebot as tb
from enum import Enum
from telebot import types
import backend

# class syntax
class State(Enum):
    authorize = 1
    main_menu = 2
    accounts = 3
    ops = 4
    concrete_card = 5

bot = tb.TeleBot("5832977748:AAH0WbooWs5awOwb0ZfegCaH4j_zil4paBo")

global states, connection
states = {}
connection = backend.get_connection()

def print_authorize(message):
    markup = types.ReplyKeyboardMarkup(row_width=4).add(types.KeyboardButton('Гончарова Мария'), types.KeyboardButton('Кондратьев Семен'))
    bot.send_message(message.chat.id, "Хот ты?", reply_markup=markup)

def print_main_menu(message):
    card_reply = types.KeyboardButton('Счета')
    ops_reply = types.KeyboardButton('Операции')
    markup = types.ReplyKeyboardMarkup(row_width=4).add(card_reply, ops_reply)
    
    id = message.from_user.id
    user_info = backend.get_user_by_login_pass(connection, states[id]['login'], states[id]['pass'])
    bot.send_message(message.chat.id, "Здраствуйте {} {}! Чем могу вам быть полезен?".format(user_info['surname'], user_info['name']), reply_markup=markup)

def print_account(message):
    id = message.from_user.id
    user_info = backend.get_user_by_login_pass(connection, states[id]['login'], states[id]['pass'])
    accounts = backend.get_active_accounts_by_user(connection, user_info['id'])
    accounts = ['{} {} {}'.format(x['number'], x['status'], x['type']) for x in accounts]
    accounts = [str(i+1)+'. '+x for i, x in enumerate(accounts)]
    markup = types.ReplyKeyboardMarkup(row_width=4).add(*[str(x+1) for x in range(len(accounts))], types.KeyboardButton('Назад'))
    bot.send_message(message.chat.id, '\n'.join(accounts), reply_markup=markup)

def print_concrete_account(message):
    id = message.from_user.id
    user_info = backend.get_user_by_login_pass(connection, states[id]['login'], states[id]['pass'])
    accounts = backend.get_active_accounts_by_user(connection, user_info['id'])
    markup = types.ReplyKeyboardMarkup(row_width=4).add(types.KeyboardButton('Назад'))
    bot.send_message(message.chat.id, str(accounts[states[id]['index']]), reply_markup=markup)

def print_ops(message):
    back_reply = types.KeyboardButton('Назад')

    markup = types.ReplyKeyboardMarkup(row_width=4).add(back_reply)
    bot.send_message(message.chat.id, "Операции", reply_markup=markup)

@bot.message_handler(commands=['start'])
def handle_start(message):
    id = message.from_user.id
    states[id] = {'state':State.authorize}
    print_authorize(message)

@bot.message_handler(content_types=['text'])
def handle_messages(message):
    id = message.from_user.id
    if id not in states:
        states[id] = {'state':State.authorize}
    
    if states[id]['state'] == State.authorize:
        if message.text == 'Гончарова Мария':
            states[id] = {'state':State.main_menu, 'login':'QQKGJFPVFY', 'pass':'FociSsQIb8'}
            print_main_menu(message)
        elif message.text == 'Кондратьев Семен':
            states[id] = {'state':State.main_menu, 'login':'WQLXCYMEUZ', 'pass':'BGdcN1G72e'}
            print_main_menu(message)
        else:
            print_authorize(message)
    elif states[id]['state'] == State.main_menu:
        if message.text == 'Счета':
            states[id]['state'] = State.accounts
            print_account(message)
        elif message.text == 'Операции':
            states[id]['state'] = {'state':State.ops}
            print_ops(message)
        else:
            print_main_menu(message)
    elif states[id]['state'] == State.accounts:
        if message.text == 'Назад':
            states[id]['state'] = State.main_menu
            print_main_menu(message)
        elif message.text.isnumeric():
            user_info = backend.get_user_by_login_pass(connection, states[id]['login'], states[id]['pass'])
            accounts = backend.get_active_accounts_by_user(connection, user_info['id'])
            if int(message.text) > 0 and int(message.text) <= len(accounts):
                states[id]['state'] = State.concrete_card
                states[id]['index'] = int(message.text) - 1
            print_concrete_account(message)
        else:
            print_account(message)
    elif states[id]['state'] == State.ops:
        if message.text == 'Назад':
            states[id]['state'] = State.main_menu
            print_main_menu(message)
        else:
            print_ops(message)
    elif states[id]['state'] == State.concrete_card:
        if message.text == 'Назад':
            states[id]['state'] = State.accounts
            print_account(message)
        else:
            print_concrete_account(message)

if __name__ == '__main__':
    print('Setted up')
    while True:
        try:
            bot.polling(timeout=1000)
        except Exception as e:
            print(e)