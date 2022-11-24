from telebot import types

# Main menu buttons
Bills = types.KeyboardButton('Счета')
Operations = types.KeyboardButton('Операции')
News = types.KeyboardButton('Новости')

main_menu = types.ReplyKeyboardMarkup(row_width=4).add(Bills, Operations, News) # Menu object