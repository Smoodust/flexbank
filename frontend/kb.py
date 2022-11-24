from telebot import types

# Main menu buttons
bills = types.KeyboardButton('Счета')
operations = types.KeyboardButton('Операции')
suggests = types.KeyboardButton('Предложения')
news = types.KeyboardButton('Новости')

main_menu = types.ReplyKeyboardMarkup(row_width=4).add(bills, operations, suggests, news) # Menu object



back_tomenu = types.KeyboardButton('Назад в меню')
empty = types.ReplyKeyboardRemove()
bills_menu = types.ReplyKeyboardMarkup(row_width=1).add(back_tomenu)
