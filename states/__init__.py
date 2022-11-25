from abc import ABC, abstractmethod
from telebot import types
from telebot.types import InputFile
from backend import *
from frontend.News import start_help
from offer import but_offer, send_offers
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
        markup = types.ReplyKeyboardMarkup(row_width=4).add(types.KeyboardButton('Да'))
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
        markup = types.ReplyKeyboardMarkup(row_width=4).add(types.KeyboardButton('Да'), types.KeyboardButton('Нет'))
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
        markup = types.ReplyKeyboardMarkup(row_width=4).add(accounts_reply, ops_reply, offers_reply)
        self.bot.send_message(message.chat.id, "Здравствуйте, {}!\nЧто хотите сделать?".format(user_info['name']), reply_markup=markup)

    def next(self, message, connection):
        if message.text == 'Счета':
            return Accounts(self.bot, self.login, self.passw)
        elif message.text == 'Операции':
            return Operations(self.bot, self.login, self.passw)
        elif message.text == 'Предложения':
            return Offers(self.bot, self.login, self.passw)
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
        buttons = [types.KeyboardButton('Назад')]
        buttons = buttons 
        markup = types.ReplyKeyboardMarkup(row_width=4).add(*buttons)
        self.bot.send_message(message.chat.id, result, reply_markup=markup)

    def next(self, message, connection):
        if message.text == 'Назад':
            return MainMenu(self.bot, self.login, self.passw)
        else:
            return Accounts(self.bot, self.login, self.passw)

class Operations(State):
    def __init__(self, bot, login, passw):
        self.bot = bot
        self.login = login
        self.passw = passw

    def render(self, message, connection):
        markup = types.ReplyKeyboardMarkup(row_width=4).add(types.KeyboardButton('Назад'))
        self.bot.send_message(message.chat.id, "ops", reply_markup=markup)

    def next(self, message, connection):
        if message.text == 'Назад':
            return MainMenu(self.bot)
        elif message.text == 'Переводы':
            return 
        else:
            return Operations(self.bot, self.login, self.passw)

class Offers(State):
    def __init__(self, bot, login, passw):
        self.bot = bot
        self.login = login
        self.passw = passw

    def but_offer():
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        Ops = types.KeyboardButton(text="В меню")
        keyboard.add(Ops)
        return keyboard

    def send_offers(self, message):
        if get_sum_transaction(connection, message.user.id )>2000000:
            self.bot.send_message(message.chat.id, text='За последний месяц вы сделали переводов на сумме превышающую 2 млн. рублей. Для того чтобы оформить вип статус перейдите по ссылке '+SEND_URL("http/exampe.com"))
        if get_diff_transaction (connection, message.user.id )<0:
            self.bot.send_message(message.chat.id, text='Ваши траты за последнйи месяц превысили ваш доход. Наш банк предлагает оформить кредитную карту с увеличенным рассрочным периодом. Если хотите оформить перейдите оп ссылкке: '+SEND_URL("http/exampe.com"))
        self.bot.send_message(message.chat.id, text='Flexbank для всех новых пользователей предлагает ипотеку под пониженный процент. Если хотите оформить перейдите по ссылке: '+SEND_URL("http/exampe.com"))

    def render(self, message, connection):
        send_offers(self, message)
        self.bot.send_message(message.chat.id, reply_markup=but_offer)

    def next(self, message, connection):
        if message.text == 'В меню':
            return MainMenu(self.bot, self.login, self.passw)
        else:
            return Offers(self.bot, self.login, self.passw)

class News(State):
    def __init__(self, bot, login, passw):
        self.bot = bot
        self.login = login
        self.passw = passw

    def but_offer():
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        Ops = types.KeyboardButton(text="В меню")
        keyboard.add(Ops)
        return keyboard

    #def send_news(self, message):
        
    def render(self, message, connection):
        send_offers(self, message)
        self.bot.send_message(message.chat.id, "offers", reply_markup=but_offer)
    def next(self, message, connection):
        if message.text == 'В меню':
            return MainMenu(self.bot, self.login, self.passw)
        else:
            return Offers(self.bot, self.login, self.passw)

class Helps(State):
    def __init__(self, bot, login, passw):
        self.bot = bot
        self.login = login
        self.passw = passw

    def start_help(self, message):
        self.bot.send_message(message.chat.id, """Что делают кнопки меню?
1.*Счета*. С помощью этой кнопки вы можете сменить свой счет/карту и настроить выбранную карту.
2.*Операции*. С помощью этой кнопки вы можете перевести или зачислить средства.
3.*Предложения*. С помощью этой кнопки вы можете получить специальные предложения от нас ;).
4.*Новости*. С помощью этой кнопки вы можете узнать о наших последних новостях.""", reply_markup=types.KeyboardButton("В меню"), parse_mode='Markdown')


    def render(self, message, connection):
        start_help(self, message)

    def next(self, message, connection):
        if message.text == 'В меню':
            return MainMenu(self.bot, self.login, self.passw)
        else:
            return Offers(self.bot, self.login, self.passw)