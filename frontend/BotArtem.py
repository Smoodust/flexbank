import asyncio
import telebot as tb
import kb

bot = tb.TeleBot("5815112728:AAHcJ_GcAXDAzemA731QYrKNY_w-leAWugI")

@bot.message_handler(commands=['start'])
def start_menu(message):
    bot.send_message(message.chat.id, message.text, reply_markup=kb.main_menu)

@bot.message_handler(commands=['dhisjhf'])
def start(message):
    message.text = 'Здравствуйте! Я банкинг-бот Neo! Для начала работы пройдите авторизацию.'
    bot.send_message(message.chat.id, message.text)
    message.text = 'Введите ваш *login и пароль.*'
    bot.send_message(message.chat.id, message.text, parse_mode="Markdown")

    # Здесь запрос к базе
    message.text = 'Вас зовут ' + '?'
    bot.send_message(message.chat.id, message.text)

@bot.message_handler(chat_types=['text'])
def bills(message):
    if message.text == 'Счета':
        bot.send_message(message.chat.id, message.text, reply_markup=kb.bills_menu)

@bot.message_handler(chat_types=['text'])
def back_to_menu(message):
    if message.text == 'Назад в меню':
        bot.send_message(message.chat.id, message.text, reply_markup=kb.main_menu)


@bot.message_handler(content_types=['text'])
def clear_buttons(message):
    bot.send_message(message.chat.id, message.text, reply_markup=kb.empty)



if __name__ == '__main__':
    bot.infinity_polling()