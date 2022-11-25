from abc import ABC, abstractmethod
from telebot import types

class State(ABC):
    @abstractmethod
    def render(self, message):
        pass

    @abstractmethod
    def next(self, message):
        pass

class Start(State):
    def __init__(self, bot):
        self.bot = bot

    def render(self, message):
        self.bot.send_message(message.chat.id, "Start")

    def next(self, message):
        return LoginInput(self.bot)

class LoginInput(State):
    def __init__(self, bot):
        self.bot = bot

    def render(self, message):
        self.bot.send_message(message.chat.id, "Login")

    def next(self, message):
        return PasswordInput(self.bot)

class PasswordInput(State):
    def __init__(self, bot):
        self.bot = bot

    def render(self, message):
        self.bot.send_message(message.chat.id, "Pass")

    def next(self, message):
        return VerifyPerson(self.bot)

class VerifyPerson(State):
    def __init__(self, bot):
        self.bot = bot

    def render(self, message):
        markup = types.ReplyKeyboardMarkup(row_width=4).add(types.KeyboardButton('Да'), types.KeyboardButton('Нет'))
        print(markup)
        self.bot.send_message(message.chat.id, "verify", reply_markup=markup)

    def next(self, message):
        if message.text == 'Да':
            return MainMenu(self.bot)
        elif message.text == 'Нет':
            return LoginInput(self.bot)
        else:
            return VerifyPerson(self.bot)

class MainMenu(State):
    def __init__(self, bot):
        self.bot = bot

    def render(self, message):
        accounts_reply = types.KeyboardButton('Счета')
        ops_reply = types.KeyboardButton('Операции')
        offers_reply = types.KeyboardButton('Предложения')
        markup = types.ReplyKeyboardMarkup(row_width=4).add(accounts_reply, ops_reply, offers_reply)
        self.bot.send_message(message.chat.id, "main menu", reply_markup=markup)

    def next(self, message):
        if message.text == 'Счета':
            return Accounts(self.bot)
        elif message.text == 'Операции':
            return Operations(self.bot)
        elif message.text == 'Предложения':
            return Offers(self.bot)
        else:
            return MainMenu(self.bot)

class Accounts(State):
    def __init__(self, bot):
        self.bot = bot

    def render(self, message):
        markup = types.ReplyKeyboardMarkup(row_width=4).add(types.KeyboardButton('Назад'))
        self.bot.send_message(message.chat.id, "account", reply_markup=markup)

    def next(self, message):
        if message.text == 'Назад':
            return MainMenu(self.bot)
        else:
            return Accounts(self.bot)

class Operations(State):
    def __init__(self, bot):
        self.bot = bot

    def render(self, message):
        markup = types.ReplyKeyboardMarkup(row_width=4).add(types.KeyboardButton('Назад'))
        self.bot.send_message(message.chat.id, "ops", reply_markup=markup)

    def next(self, message):
        if message.text == 'Назад':
            return MainMenu(self.bot)
        else:
            return Operations(self.bot)

class Offers(State):
    def __init__(self, bot):
        self.bot = bot

    def render(self, message):
        markup = types.ReplyKeyboardMarkup(row_width=4).add(types.KeyboardButton('Назад'))
        self.bot.send_message(message.chat.id, "offers", reply_markup=markup)
    def next(self, message):
        if message.text == 'Назад':
            return MainMenu(self.bot)
        else:
            return Offers(self.bot)