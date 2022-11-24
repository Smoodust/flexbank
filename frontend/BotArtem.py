import asyncio
import telebot as tb
from telebot import types
import kb

bot = tb.TeleBot("5815112728:AAHcJ_GcAXDAzemA731QYrKNY_w-leAWugI")

@bot.message_handler(commands=['start'])
def Start(message):
    bot.send_message(message.chat.id, message.text, reply_markup=kb.main_menu)

if __name__ == '__main__':
    bot.infinity_polling()