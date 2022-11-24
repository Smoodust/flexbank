import telebot

bot = telebot.TeleBot('5815112728:AAHcJ_GcAXDAzemA731QYrKNY_w-leAWugI')

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
     bot.infinity_polling()