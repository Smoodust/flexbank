from abc import ABC, abstractmethod
from telebot import types
from telebot.types import InputFile
from backend import *
from utils import *

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
        self.bot.send_animation(message.chat.id, InputFile(r"C:\Users\USER\Documents\flexbank\content\FlexBank.gif"), caption='Здравствуйте! Я банкинг-бот Neo! Для начала работы пройдите авторизацию.\nНажмите Да для продолжения.', reply_markup=markup)

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
            self.bot.send_photo(message.chat.id, InputFile(r"C:\Users\USER\Documents\flexbank\content\Dead_Svin.jpg"), caption='Мы не нашли такого пользователя. Попробуйте еще раз')
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
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(accounts_reply, ops_reply, offers_reply, news_reply)
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
        else:
            return MainMenu(self.bot, self.login, self.passw)

class Accounts(State):
    def __init__(self, bot, login, passw):
        self.bot = bot
        self.login = login
        self.passw = passw

    def render(self, message, connection):
        user_info = get_user_by_login_pass(connection, self.login, self.passw)
        accounts = get_accounts_by_user(connection, user_info['id'])
        result = [f"🧾 {i+1}. {str(x['number'])} - {status_to_string[x['status']]} {type_to_string[x['type']]}" for i, x in enumerate(accounts)]
        result = '\n'.join(result)
        buttons = [types.KeyboardButton('Назад'), types.KeyboardButton('Обновить')]
        buttons = buttons + [types.KeyboardButton(str(i+1)) for i in range(len(accounts))]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)
        self.bot.send_message(message.chat.id, result, reply_markup=markup)

    def next(self, message, connection):
        user_info = get_user_by_login_pass(connection, self.login, self.passw)
        accounts = get_accounts_by_user(connection, user_info['id'])
        if message.text == 'Назад':
            return MainMenu(self.bot, self.login, self.passw)
        elif message.text == 'Обновить':
            return Accounts(self.bot, self.login, self.passw)
        elif message.text.isdigit():
            if int(message.text) > 0 and int(message.text) <= len(accounts):
                return ConcreteAccount(self.bot, self.login, self.passw, int(message.text) - 1)
        else:
            return Accounts(self.bot, self.login, self.passw)

class ConcreteAccount(State):
    def __init__(self, bot, login, passw, index):
        self.bot = bot
        self.login = login
        self.passw = passw
        self.index = index

    def render(self, message, connection):
        user_info = get_user_by_login_pass(connection, self.login, self.passw)
        account = get_accounts_by_user(connection, user_info['id'])[self.index]
        cards = get_cards_by_account(connection, account['id'])
        result = concrete_account_first.format(account['number'], get_diff_transaction_account(connection, account['id']), len(cards))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton('Назад'))
        #types.ReplyKeyboardRemove()
        self.bot.send_message(message.chat.id, result, reply_markup=markup)

    def next(self, message, connection):
        if message.text == 'Назад':
            return Accounts(self.bot, self.login, self.passw)
        else:
            return ConcreteAccount(self.bot, self.login, self.passw, self.index)

class Operations(State):
    def __init__(self, bot, login, passw):
        self.bot = bot
        self.login = login
        self.passw = passw

    def render(self, message, connection):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton('Назад'))
        self.bot.send_message(message.chat.id, "ops", reply_markup=markup)

    def next(self, message, connection):
        if message.text == 'Назад':
            return MainMenu(self.bot, self.login, self.passw)
        elif message.text == 'Переводы':
            return Operations(self.bot, self.login, self.passw)
        else:
            return Operations(self.bot, self.login, self.passw)

class TransactionsBetweenBills(State):
    def __init__(self, bot, login, passw):
        self.bot = bot
        self.login = login
        self.passwd = passwd

    def render(self, message, connection):
        self.bot.send_message(message.chat.id, "Переводы между счетами", reply_markup=but_operation())

    def next(self, message, connection):
        if message.text == 'Назад':
            return MainMenu(self.bot, self.login, self.passw)
        else:
            return Transactions(self.bot, self.login, self.passw)

class TransactionsBetweenPersons(State):
    def __init__(self, bot, login, passw):
        self.bot = bot
        self.login = login
        self.passwd = passwd

    def render(self, message, connection):
        self.bot.send_message(message.chat.id, "Переводы между счетами", reply_markup=but_operation())

    def next(self, message, connection):
        if message.text == 'Назад':
            return MainMenu(self.bot, self.login, self.passw)
        else:
            return Transactions(self.bot, self.login, self.passw)

class TransactionsToEbenya(State):
    def __init__(self, bot, login, passw):
        self.bot = bot
        self.login = login
        self.passwd = passwd

    def render(self, message, connection):
        self.bot.send_message(message.chat.id, "Переводы между счетами", reply_markup=but_operation())

    def next(self, message, connection):
        if message.text == 'Назад':
            return MainMenu(self.bot, self.login, self.passw)
        else:
            return Transactions(self.bot, self.login, self.passw)

class Offers(State):
    def __init__(self, bot, login, passw):
        self.bot = bot
        self.login = login
        self.passw = passw

    def render(self, message, connection):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton('Назад'))
        user = get_user_by_login_pass(connection, self.login, self.passw)
        if get_sum_transaction_user(connection, user['id']) > 2000000:
            self.bot.send_message(message.chat.id, text='За последний месяц вы сделали переводов на сумму, превышающую 2 млн. рублей. Для того чтобы оформить вип статус, перейдите по ссылке http://exampe.com', reply_markup=markup)
        elif get_diff_transaction_user(connection, user['id']) < 0:
            self.bot.send_message(message.chat.id, text='Ваши траты за последний месяц превысили ваш доход. Наш банк предлагает оформить кредитную карту с увеличенным рассрочным периодом. Перейдите по ссылкке: http://exampe.com', reply_markup=markup)
        else:
            self.bot.send_message(message.chat.id, text='Flexbank для всех новых пользователей предлагает ипотеку под пониженный процент. Если хотите оформить перейдите по ссылке: http://exampe.com', reply_markup=markup)

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
        index = random.randint(0, 3)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton(text="Назад"))
        self.bot.send_photo(message.chat.id, InputFile(news_dict[index]['image']), text=news_dict[index]['desc'], reply_markup=markup, parse_mode="Markdown")

    def next(self, message, connection):
        if message.text == 'Назад':
            return MainMenu(self.bot, self.login, self.passw)
        else:
            return News(self.bot, self.login, self.passw)
