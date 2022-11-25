import telebot as tb
from telebot import types
from enum import Enum
import random
from telebot.types import InputFile

bot = tb.TeleBot("5815112728:AAHcJ_GcAXDAzemA731QYrKNY_w-leAWugI")

news_dict = {0:("""*FlexBank создал нового маскота!*
FlexBank создал нового маскота! Встречайте Свиноту!
 Свинота проведет вас по лабиринту user flow и создаст 
 настоящий приятный и удобный user experience…
""",r'D:\NewsPhotos\Swinota.jpg'),

 1:("""*FlexBank запускает беспроцентные переводы с кредитных карт*
FlexBank вносит изменения в тарифы кредитных карт, а также в правила
 применения тарифов по кредитным картам и условия по переводам, платежам
  и дополнительным услугам.  В новую редакцию тарифов добавлен льготный лимит
   в размере до 50 000 ₽ за расчетный период на переводы через сервисы FlexBank
    с кредитной карты: внутрибанковские переводы, переводы с карты на карту, переводы
     по номеру телефона (кроме карт иностранных банков-партнеров), включая СБП. При переводах
      в рамках этой суммы комиссия взиматься не будет и беспроцентный период будет сохранен. 
      Льготный лимит распространяется на текущих и будущих клиентов с кредитной картой FlexBank.""",
      r'D:\NewsPhotos\NoProcent.jpg'),
       2:("""*FlexBank запускает международные переводы для физических лиц в юанях и тенге*
FlexBank с 8 ноября 2022 года запускает исходящие SWIFT переводы для физических лиц в юанях 
и тенге во все банки Китая и Казахстана соответственно. Переводы бесплатны для клиентов с
 подключенной подпиской Premium или Private, в остальных случаях — 120 юаней или 9 000 тенге.
""",r'D:\NewsPhotos\Internati.jpg'),
 3:("""*FlexBank обновляет тарифы по переводам, платежам и дополнительным услугам*
FlexBank обновляет тарифы по переводам, платежам и дополнительным услугам. В частности:
•	уточнены условия совершения валютных переводов по реквизитам счета;
•	расширен перечень организаций, кредиты и займы в которых можно погашать через FlexBank.
Изменения вступают в силу с 22 декабря 2022 года.""",r"D:\NewsPhotos\Tariffes.jpg"),
 4:("""*FlexBank улучшает условия хранения долларов и евро на карточных и брокерских счетах*
FlexBank обновляет условия хранения евро и долларов на карточных и брокерских счетах (включая ИИС)
 физических лиц. С 24 ноября 2022 года сумма баланса, при превышении которой взимается комиссия за 
 обслуживание, повышается до 100 000 у.е. в валюте счета (ранее 10 000 долларов и 20 000 евро).
Новые условия распространяются на все тарифы FlexBank и FlexBank Инвестиций. Комиссия за хранение валюты
 свыше 100 000 у.е. по карточным и брокерским счетам остается прежней — 0,25% в месяц и списывается ежедневно.
Тренд по улучшению условий хранения обусловлен развитием независимых от иностранной инфраструктуры инструментов по размещению валюты.""",r"D:\NewsPhotos\Save.jpg")}

def start_help(message):
    bot.send_message(message.chat.id, """Что делают кнопки меню?
1.*Счета*. С помощью этой кнопки вы можете сменить свой счет/карту и настроить выбранную карту.
2.*Операции*. С помощью этой кнопки вы можете перевести или зачислить средства.
3.*Предложения*. С помощью этой кнопки вы можете получить специальные предложения от нас ;).
4.*Новости*. С помощью этой кнопки вы можете узнать о наших последних новостях.""", reply_markup=start_main_menu(), parse_mode='Markdown')

def start_news(message):
    Random = random.randint(0, 3)
    print(news_dict[Random][0])
    bot.send_photo(message.chat.id, open(news_dict[Random][1], 'rb'), news_dict[Random][0], reply_markup=start_main_menu(), parse_mode="Markdown")

def start_main_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    Bill = types.KeyboardButton(text="Счета")
    Ops = types.KeyboardButton(text="Операции")
    Suggest = types.KeyboardButton(text="Предложения")
    News = types.KeyboardButton(text="Новости")
    Info = types.KeyboardButton(text="Помощь")
    keyboard.row(Bill, Ops, Suggest)
    keyboard.row(News, Info)
    return keyboard


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Вы в главном меню", reply_markup=start_main_menu())

@bot.message_handler(content_types=['text'])
def check_message(message):
    if message.text == 'Новости':
        start_news(message)
    if message.text == 'Помощь':
        start_help(message)

if __name__ == '__main__':
    bot.infinity_polling()