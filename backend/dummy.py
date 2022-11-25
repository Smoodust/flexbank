import hashlib

logins = ['QQKGJFPVFY', 'WQLXCYMEUZ', 'FGYZQVWSNS', 'TNQRQGZWDB', 'NLJDQKYSSR', 'UOWXLWJFCB', 'MFAFJDZJTH', 'CPNCGDDYLP', 'YYPRYAKWWA', 'YZDLPBTSDY']
passwords = ['FociSsQIb8', 'BGdcN1G72e', 'bAx9Jq8f4f', 'TsdGuGx0Sh', '6PZ4FyjB8L', 'ttEP2XtV3I', 'TLOEkC7Vqm', 'l4gPdrN9Ik', 'Z3wp7vobZn', '773cyOaEEo']

def print_main_menu(message):
    card_reply = types.KeyboardButton('Счета')
    ops_reply = types.KeyboardButton('Операции')
    markup = types.ReplyKeyboardMarkup(row_width=4).add(card_reply, ops_reply)
    
    id = message.from_user.id
    user_info = backend.get_user_by_login_pass(connection, states[id]['login'], states[id]['pass'])
    bot.send_message(message.chat.id, "Здраствуйте {} {}! Чем могу вам быть полезен?".format(user_info['surname'], user_info['name']), reply_markup=markup)

def print_account(message):
    id = message.from_user.id
    user_info = backend.get_user_by_login_pass(connection, states[id]['login'], states[id]['pass'])
    accounts = backend.get_active_accounts_by_user(connection, user_info['id'])
    accounts = ['{} {} {}'.format(x['number'], x['status'], x['type']) for x in accounts]
    accounts = [str(i+1)+'. '+x for i, x in enumerate(accounts)]
    markup = types.ReplyKeyboardMarkup(row_width=4).add(*[str(x+1) for x in range(len(accounts))], types.KeyboardButton('Назад'))
    bot.send_message(message.chat.id, '\n'.join(accounts), reply_markup=markup)

def print_concrete_account(message):
    id = message.from_user.id
    user_info = backend.get_user_by_login_pass(connection, states[id]['login'], states[id]['pass'])
    accounts = backend.get_active_accounts_by_user(connection, user_info['id'])
    markup = types.ReplyKeyboardMarkup(row_width=4).add(types.KeyboardButton('Назад'))
    bot.send_message(message.chat.id, str(accounts[states[id]['index']]), reply_markup=markup)
