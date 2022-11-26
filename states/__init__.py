from abc import ABC, abstractmethod
from telebot import types
from telebot.types import InputFile
from backend import *
from utils import *
from datetime import datetime
import random
import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

class State(ABC):
    @abstractmethod
    def render(self, message, connection):
        pass

    @abstractmethod
    def next(self, message, connection):
        pass

class Start(State):
    def __init__(self, bot):
        self.bot = bot

    def render(self, message, connection):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton('Да'))
        self.bot.send_animation(message.chat.id, InputFile(os.path.join(os.getcwd(), 'content', 'FlexBank.gif')), caption='Здравствуйте! Я банкинг-бот Свинота! Для начала работы пройдите авторизацию.\nНажмите Да для продолжения.', reply_markup=markup)

    def next(self, message, connection):
        if message.text == 'Да':
            return LoginInput(self.bot)
        else:
            return Start(self.bot)

class LoginInput(State):
    def __init__(self, bot):
        self.bot = bot

    def render(self, message, connection):
        self.bot.send_message(message.chat.id, "Введите ваш логин:", reply_markup=types.ReplyKeyboardRemove())

    def next(self, message, connection):
        return PasswordInput(self.bot, message.text)

class PasswordInput(State):
    def __init__(self, bot, login):
        self.bot = bot
        self.login = login

    def render(self, message, connection):
        self.bot.send_message(message.chat.id, "Введите ваш пароль:")

    def next(self, message, connection):
        passw = message.text
        if check_authentication(connection, self.login, passw):
            return VerifyPerson(self.bot, self.login, passw)
        else:
            self.bot.send_photo(message.chat.id, InputFile(os.path.join(os.getcwd(), 'content', 'Dead_Svin.jpg')), caption='Мы не нашли такого пользователя. Попробуйте еще раз')
            return LoginInput(self.bot)

class VerifyPerson(State):
    def __init__(self, bot, login, passw):
        self.bot = bot
        self.login = login
        self.passw = passw

    def render(self, message, connection):
        user_info = get_user_by_login_pass(connection, self.login, self.passw)
        user_info['name'], user_info['surname']
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton('Да'), types.KeyboardButton('Нет'))
        self.bot.send_message(message.chat.id, '{} {}, это вы?'.format(user_info['surname'], user_info['name']), reply_markup=markup)

    def next(self, message, connection):
        if message.text == 'Да':
            return MainMenu(self.bot, self.login, self.passw)
        elif message.text == 'Нет':
            self.bot.send_message(message.chat.id, "Ничего. Можете попробовать еще раз ;)")
            return LoginInput(self.bot)
        else:
            return VerifyPerson(self.bot, self.login, self.passw)

class MainMenu(State):
    def __init__(self, bot, login, passw):
        self.bot = bot
        self.login = login
        self.passw = passw

    def render(self, message, connection):
        user_info = get_user_by_login_pass(connection, self.login, self.passw)
        accounts_reply = types.KeyboardButton('Счета')
        ops_reply = types.KeyboardButton('Операции')
        offers_reply = types.KeyboardButton('Предложения')
        news_reply = types.KeyboardButton('Новости')
        anal_reply = types.KeyboardButton('Аналитика')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(accounts_reply, ops_reply, offers_reply, news_reply, anal_reply)
        self.bot.send_message(message.chat.id, "Здравствуйте, {}!\nЧто хотите сделать?".format(user_info['name']), reply_markup=markup)

    def next(self, message, connection):
        if message.text == 'Счета':
            return Accounts(self.bot, self.login, self.passw)
        elif message.text == 'Операции':
            return Operations(self.bot, self.login, self.passw)
        elif message.text == 'Предложения':
            return Offers(self.bot, self.login, self.passw)
        elif message.text == 'Новости':
            return News(self.bot, self.login, self.passw)
        elif message.text == 'Аналитика':
            return Analytic(self.bot, self.login, self.passw)
        else:
            return MainMenu(self.bot, self.login, self.passw)

class Accounts(State):
    def __init__(self, bot, login, passw):
        self.bot = bot
        self.login = login
        self.passw = passw

    def render(self, message, connection):
        user_info = get_user_by_login_pass(connection, self.login, self.passw)
        accounts = get_not_canceled_accounts_by_user(connection, user_info['id'])
        result = [f"🧾 {i+1}. {str(x['number'])} - {status_to_string[x['status']]} {type_to_string[x['type']]}. Баланс: {get_diff_transaction_account(connection, x['id'])}" for i, x in enumerate(accounts)]
        result = '\n'.join(result)
        buttons = [types.KeyboardButton('Назад'), types.KeyboardButton('Обновить')]
        buttons = buttons + [types.KeyboardButton(str(i+1)) for i in range(len(accounts))]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)
        self.bot.send_message(message.chat.id, result, reply_markup=markup)

    def next(self, message, connection):
        user_info = get_user_by_login_pass(connection, self.login, self.passw)
        accounts = get_not_canceled_accounts_by_user(connection, user_info['id'])
        if message.text == 'Назад':
            return MainMenu(self.bot, self.login, self.passw)
        elif message.text == 'Обновить':
            return Accounts(self.bot, self.login, self.passw)
        elif message.text.isdigit():
            if int(message.text) > 0 and int(message.text) <= len(accounts):
                return ConcreteAccount(self.bot, self.login, self.passw, accounts[int(message.text) - 1]['id'])
        else:
            return Accounts(self.bot, self.login, self.passw)

class ConcreteAccount(State):
    def __init__(self, bot, login, passw, id_account):
        self.bot = bot
        self.login = login
        self.passw = passw
        self.id_account = id_account

    def render(self, message, connection):
        account = get_account_by_id(connection, self.id_account)
        cards = get_not_canceled_cards_by_account(connection, account['id'])
        result = concrete_account_first.format(account['number'], get_diff_transaction_account(connection, account['id']), len(cards))
        self.bot.send_message(message.chat.id, result, reply_markup=types.ReplyKeyboardRemove())

        buttons = [types.KeyboardButton('История операций'), types.KeyboardButton('Назад')]
        if account['status'] == 'active':
            buttons += [types.KeyboardButton('Заблокировать'), types.KeyboardButton('Закрыть')]
        elif account['status'] == 'blocked':
            buttons += [types.KeyboardButton('Активировать')]
        buttons += [f'{i+1} карта' for i, _ in enumerate(cards)]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)
        result = [f"💳 {i+1}. {str(x['card_number'])} - {status_to_string[x['status']]}" for i, x in enumerate(cards)]
        result = '\n'.join(result)
        self.bot.send_message(message.chat.id, result, reply_markup=markup)


    def next(self, message, connection):
        account = get_account_by_id(connection, self.id_account)
        cards = get_not_canceled_cards_by_account(connection, account['id'])
        message_card_match = re.search('^(\d+) карта$', message.text, re.IGNORECASE)
        
        if message.text == 'Заблокировать' and account['status'] == 'active':
            return Confirmation(self.bot, self.login, self.passw, Accounts(self.bot, self.login, self.passw), lambda: block_account(connection, account['id']))
        elif message.text == 'Закрыть' and account['status'] == 'active':
            return Confirmation(self.bot, self.login, self.passw, Accounts(self.bot, self.login, self.passw), lambda: close_account(connection, account['id']))
        elif message.text == 'Активировать' and account['status'] == 'blocked':
            return Confirmation(self.bot, self.login, self.passw, Accounts(self.bot, self.login, self.passw), lambda: activate_account(connection, account['id']))
        elif message.text == 'История операций':
            transactions = get_transactions_by_account(connection, account['id'])
            transactions = sorted(transactions, key=lambda x: datetime.strptime(x['date'], r'%d/%m/%y'))
            transactions = transactions[:10]
            result = [f"💸 {i+1}. {format_transaction(account, x)}" for i, x in enumerate(transactions)]
            result = '\n'.join(result)
            self.bot.send_message(message.chat.id, result)
            return ConcreteAccount(self.bot, self.login, self.passw, self.index)
        elif message.text == 'Назад':
            return Accounts(self.bot, self.login, self.passw)
        elif message_card_match:
            return ConcreteCards(self.bot, self.login, self.passw, cards[int(message_card_match.group(1)) - 1]['id'])
        else:
            return ConcreteAccount(self.bot, self.login, self.passw, self.index)

class ConcreteCards(State):
    def __init__(self, bot, login, passw, id_card):
        print(id_card)
        self.bot = bot
        self.login = login
        self.passw = passw
        self.id_card = id_card

    def render(self, message, connection):
        try:
            card = get_card_by_id(connection, self.id_card)
            result = f'''{card['card_number']} - {status_to_string[card['status']]}'''
            buttons = [types.KeyboardButton('Получить CVC'), types.KeyboardButton('Получить дату до завершения'), types.KeyboardButton('Назад')]
            if card['status'] == 'active':
                buttons += [types.KeyboardButton('Заблокировать'), types.KeyboardButton('Закрыть')]
            elif card['status'] == 'blocked':
                buttons += [types.KeyboardButton('Активировать')]
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)
            self.bot.send_message(message.chat.id, result, reply_markup=markup)
        except Exception as e:
            print(e)

    def next(self, message, connection):
        card = get_card_by_id(connection, self.id_card)
        
        if message.text == 'Заблокировать' and card['status'] == 'active':
            return Confirmation(self.bot, self.login, self.passw, Accounts(self.bot, self.login, self.passw), lambda: block_card(connection, card['id']))
        elif message.text == 'Закрыть' and card['status'] == 'active':
            return Confirmation(self.bot, self.login, self.passw, Accounts(self.bot, self.login, self.passw), lambda: close_card(connection, card['id']))
        elif message.text == 'Активировать' and card['status'] == 'blocked':
            return Confirmation(self.bot, self.login, self.passw, Accounts(self.bot, self.login, self.passw), lambda: activate_card(connection, card['id']))
        elif message.text == 'Назад':
            return Accounts(self.bot, self.login, self.passw)
        elif message.text == 'Получить CVC':
            return Confirmation(self.bot, self.login, self.passw, Accounts(self.bot, self.login, self.passw), lambda: self.bot.send_message(message.chat.id, f"CVC: {card['cvc']}"))
        elif message.text == 'Получить дату до завершения':
            return Confirmation(self.bot, self.login, self.passw, Accounts(self.bot, self.login, self.passw), lambda: self.bot.send_message(message.chat.id, f"Действие до: {card['validity_period']}"))
        else:
            return ConcreteAccount(self.bot, self.login, self.passw, self.index)

class Confirmation(State):
    def __init__(self, bot, login, passw, previous_state, action):
        self.bot = bot
        self.login = login
        self.passw = passw
        self.previous_state = previous_state
        self.action = action

    def render(self, message, connection):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton('Да'), types.KeyboardButton('Нет'))
        self.bot.send_message(message.chat.id, "Вы точно уверены?", reply_markup=markup)

    def next(self, message, connection):
        if message.text == 'Да':
            self.action()
            return self.previous_state
        elif message.text == 'Нет':
            return self.previous_state
        else:
            return Confirmation(self.bot, self.login, self.passw, self.previous_state, self.action)

class Operations(State):
    def __init__(self, bot, login, passw):
        self.bot = bot
        self.login = login
        self.passw = passw

    def render(self, message, connection):
        user_info = get_user_by_login_pass(connection, self.login, self.passw)
        accounts = get_accounts_by_user(connection, user_info['id'])
        buttons = [types.KeyboardButton('Назад'),types.KeyboardButton('Перевод на счёт внутри банка'), types.KeyboardButton('Перевод на счёт вне банка')]
        if len(accounts) > 1:
            buttons += [types.KeyboardButton('Перевод между счетами')]
        markup = types.ReplyKeyboardMarkup().add(*buttons)
        self.bot.send_message(message.chat.id, 'Какой тип транзакции вы хотите совершить?', reply_markup=markup)
        
    def next(self, message, connection):
        user_info = get_user_by_login_pass(connection, self.login, self.passw)
        accounts = get_accounts_by_user(connection, user_info['id'])
        if message.text == 'Назад':
            return MainMenu(self.bot, self.login, self.passw)
        elif message.text == 'Перевод между счетами' and len(accounts) > 1:
            return FromTransaction(self.bot, self.login, self.passw, 'Перевод между счетами')
        elif message.text in ['Перевод на счёт внутри банка', 'Перевод на счёт вне банка']:
            return FromTransaction(self.bot, self.login, self.passw, message.text)
        else:
            return Operations(self.bot, self.login, self.passw)
            
class FromTransaction(State):
    def __init__(self, bot, login, passw, type):
        self.bot = bot
        self.login = login
        self.passw = passw
        self.type = type

    def render(self, message, connection):
        user_info = get_user_by_login_pass(connection, self.login, self.passw)
        accounts = get_accounts_by_user(connection, user_info['id'])
        result = [f"🧾 {i+1}. {str(x['number'])} - {status_to_string[x['status']]} {type_to_string[x['type']]}. Баланс: {get_diff_transaction_account(connection, x['id'])}" for i, x in enumerate(accounts)]
        result = '\n'.join(result)
        buttons = [types.KeyboardButton(str(i+1)) for i in range(len(accounts))] 
        buttons += [types.KeyboardButton('Назад')]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)
        self.bot.send_message(message.chat.id, "Выберите с какого счета хотите перевести деньги:\n" + result, reply_markup=markup)

    def next(self, message, connection):
        try:
            user_info = get_user_by_login_pass(connection, self.login, self.passw)
            accounts = get_not_canceled_accounts_by_user(connection, user_info['id'])
            if message.text.isdigit():
                if int(message.text) > 0 and int(message.text) <= len(accounts):
                    return WhereTransaction(self.bot, self.login, self.passw, self.type, accounts[int(message.text) - 1]['id'])
            elif message.text == 'Назад':
                return Operations(self.bot, self.login, self.passw)
            else:
                return FromTransaction(self.bot, self.login, self.passw, self.type)
        except Exception as e:
            print(e)

class WhereTransaction(State):
    def __init__(self, bot, login, passw, type, id_from):
        self.bot = bot
        self.login = login
        self.passw = passw
        self.type = type
        self.id_from = id_from

    def render(self, message, connection):
        try:
            if self.type == 'Перевод между счетами':
                user_info = get_user_by_login_pass(connection, self.login, self.passw)
                accounts = get_accounts_by_user(connection, user_info['id'])
                result = [f"🧾 {i+1}. {str(x['number'])} - {status_to_string[x['status']]} {type_to_string[x['type']]}. Баланс: {get_diff_transaction_account(connection, x['id'])}" for i, x in enumerate(accounts)]
                result = '\n'.join(result)
                buttons = [types.KeyboardButton(str(i+1)) for i in range(len(accounts))] 
                buttons += [types.KeyboardButton('Назад')]
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)
                self.bot.send_message(message.chat.id, "Выберите на какой счет хотите перевести деньги:\n" + result, reply_markup=markup)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton('Назад'))
                self.bot.send_message(message.chat.id, "Введите на какой счет хотите перевести деньги:", reply_markup=markup)
        except Exception as e:
            print(e)

    def next(self, message, connection):
        try:
            user_info = get_user_by_login_pass(connection, self.login, self.passw)
            accounts = get_not_canceled_accounts_by_user(connection, user_info['id'])
            if message.text.isdigit():
                if int(message.text) > 0 and int(message.text) <= len(accounts) and self.type == 'Перевод между счетами':
                    return AmountTransaction(self.bot, self.login, self.passw, self.type, self.id_from, accounts[int(message.text) - 1]['id'])
                elif len(message.text) == 20 and self.type in ['Перевод на счёт внутри банка', 'Перевод на счёт вне банка']:
                    return AmountTransaction(self.bot, self.login, self.passw, self.type, self.id_from, int(message.text))
                else:
                    self.bot.send_message(message.chat.id, "Попробуйте еще раз")
                    return WhereTransaction(self.bot, self.login, self.passw)
            elif message.text == 'Назад':
                return Operations(self.bot, self.login, self.passw)
            else:
                self.bot.send_message(message.chat.id, "Попробуйте еще раз")
                return WhereTransaction(self.bot, self.login, self.passw)
        except Exception as e:
            print(e)

class AmountTransaction(State):
    def __init__(self, bot, login, passw, type, id_from, id_to):
        self.bot = bot
        self.login = login
        self.passw = passw
        self.type = type
        self.id_from = id_from
        self.id_to = id_to
    
    def render(self, message, connection):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton('Назад'))
        self.bot.send_message(message.chat.id, "Введите сколько денег перевести:", reply_markup=markup)
    
    def next(self, message, connection):
        try:
            account_from = get_account_by_id(connection, self.id_from)
            balance = get_diff_transaction_account(connection, account_from['id'])
            print(self.id_from, self.id_to, message.text, self.type)
            if message.text.lstrip('-+').isdigit():
                if balance > float(message.text):
                    if float(message.text) > 0:
                        if self.type == 'Перевод между счетами':
                            make_between_accounts(connection, self.id_from, self.id_to, float(message.text))
                        elif self.type == 'Перевод на счёт внутри банка':
                            account_to = get_account_by_number(connection, self.id_to)
                            make_between_accounts(connection, self.id_from, account_to['id'], float(message.text))
                        else:
                            make_transaction(connection, self.id_from, 'transfer', -float(message.text), str(self.id_to))
                        return Operations(self.bot, self.login, self.passw)
                    else:
                        self.bot.send_message(message.chat.id, "Вы хотите отправить отрицательное число средств.\nКак?")
                        return AmountTransaction(self.bot, self.login, self.passw, self.type, self.id_from, self.id_to)
                else:
                    self.bot.send_message(message.chat.id, "У вас недостаточно средств")
                    return AmountTransaction(self.bot, self.login, self.passw, self.type, self.id_from, self.id_to)
            elif message.text == 'Назад':
                return Operations(self.bot, self.login, self.passw)
            else:
                return AmountTransaction(self.bot, self.login, self.passw, self.type, self.id_from, self.id_to)
        except Exception as e:
            print(e)

class Offers(State):
    def __init__(self, bot, login, passw):
        self.bot = bot
        self.login = login
        self.passw = passw

    def render(self, message, connection):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton('Назад'))
        user = get_user_by_login_pass(connection, self.login, self.passw)
        if get_sum_transaction_user(connection, user['id']) > 2000000:
            self.bot.send_photo(message.chat.id, InputFile(os.path.join(os.getcwd(), 'content', 'twomillion.png')), caption='За последний месяц вы сделали переводов на сумму, превышающую 2 млн. рублей. Для того чтобы оформить вип статус, перейдите по ссылке http://exampe.com', reply_markup=markup, parse_mode="Markdown")
        elif get_diff_transaction_user(connection, user['id']) < 0:
            self.bot.send_photo(message.chat.id, InputFile(os.path.join(os.getcwd(), 'content', 'credit.png')), caption='Ваши траты за последний месяц превысили ваш доход. Наш банк предлагает оформить кредитную карту с увеличенным рассрочным периодом. Перейдите по ссылкке: http://exampe.com', reply_markup=markup, parse_mode="Markdown")
        else:
            self.bot.send_photo(message.chat.id, InputFile(os.path.join(os.getcwd(), 'content', 'ipoteka.png')), caption='Flexbank для всех новых пользователей предлагает ипотеку под пониженный процент. Если хотите оформить перейдите по ссылке: http://exampe.com', reply_markup=markup, parse_mode="Markdown")

    def next(self, message, connection):
        if message.text == 'Назад':
            return MainMenu(self.bot, self.login, self.passw)
        else:
            return Offers(self.bot, self.login, self.passw)

class News(State):
    def __init__(self, bot, login, passw):
        self.bot = bot
        self.login = login
        self.passw = passw

    def render(self, message, connection):
        try:
            index = random.randint(0, 3)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton(text="Назад"))
            self.bot.send_photo(message.chat.id, InputFile(os.path.join(os.getcwd(), 'content', news_dict[index]['image'])), caption=news_dict[index]['desc'], reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(e)
    def next(self, message, connection):
        return MainMenu(self.bot, self.login, self.passw)

class Analytic(State):
    def __init__(self, bot, login, passw):
        self.bot = bot
        self.login = login
        self.passw = passw
    
    def make_income_plot(self, df):
        df = df[df['amount'] > 0]
        df = df.set_index('date')
        df = df.groupby(pd.Grouper(freq='M'))['amount'].sum().reset_index()
        my_plot = sns.relplot(
            data=df,
            x="date", y="amount", kind="line"
        )
        buf = BytesIO()
        my_plot.figure.savefig(buf, format = 'png')
        buf.seek(0)
        return buf.getvalue()
    
    def make_expense_plot(self, df):
        df = df[df['amount'] < 0]
        df['amount'] = abs(df['amount'])
        df = df.set_index('date')
        df = df.groupby(pd.Grouper(freq='M'))['amount'].sum().reset_index()
        my_plot = sns.relplot(
            data=df,
            x="date", y="amount", kind="line"
        )
        buf = BytesIO()
        my_plot.figure.savefig(buf, format = 'png')
        buf.seek(0)
        return buf.getvalue()
    
    def make_income_category_plot(self, df):
        df = df[df['amount'] > 0]
        count = df['another_subject'].value_counts()
        colors = sns.color_palette('pastel')
        fig, ax = plt.subplots()
        ax.pie(count,  labels=count.index, autopct='%1.1f%%', colors=colors, startangle=90)
        ax.axis('equal')
        buf = BytesIO()
        fig.savefig(buf, format = 'png')
        buf.seek(0)
        return buf.getvalue()
    
    def make_expense_category_plot(self, df):
        df = df[df['amount'] < 0]
        df['amount'] = abs(df['amount'])
        count = df['another_subject'].value_counts()
        colors = sns.color_palette('pastel')
        fig, ax = plt.subplots()
        ax.pie(count,  labels=count.index, autopct='%1.1f%%', colors=colors, startangle=90)
        ax.axis('equal')
        buf = BytesIO()
        fig.savefig(buf, format = 'png')
        buf.seek(0)
        return buf.getvalue()

    def render(self, message, connection):
        try:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton('Назад'))
            df = get_transactions_by_user(connection, get_user_by_login_pass(connection, self.login, self.passw)['id'])
            df = pd.DataFrame(df)
            df['date'] = pd.to_datetime(df['date'])
            
            self.bot.send_photo(message.chat.id, self.make_income_plot(df), caption='Доходы', parse_mode="Markdown")
            self.bot.send_photo(message.chat.id, self.make_expense_plot(df), caption='Расходы', parse_mode="Markdown")
            self.bot.send_photo(message.chat.id, self.make_income_category_plot(df), caption='Распределение доходов', parse_mode="Markdown")
            self.bot.send_photo(message.chat.id, self.make_expense_category_plot(df), caption='Распределение расходов', reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(e)
    def next(self, message, connection):
        return MainMenu(self.bot, self.login, self.passw)
