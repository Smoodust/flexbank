import telebot

bot = telebot.TeleBot("5815112728:AAHcJ_GcAXDAzemA731QYrKNY_w-leAWugI")

@bot.message_handler(commands=['/start', '/help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

if __name__ == '__main__':
    bot.infinity_polling()