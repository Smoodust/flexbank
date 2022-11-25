import telebot as tb
import flask
import states
import backend

API_TOKEN = "5928558655:AAHOQcmlQTMJRVe_7IFEnAHHUw2qvvYhaZM"
APP_HOST = '127.0.0.1'
APP_PORT = '8444'
WEB_HOOK_URL = 'https://123f-213-80-237-142.eu.ngrok.io'

bot = tb.TeleBot(API_TOKEN)
app = flask.Flask(__name__)

global states_dict, connection
states_dict = {}
connection = backend.get_connection()

@bot.message_handler(commands=['start'])
def handle_start(message):
    id = message.from_user.id
    states_dict[id] = states.Start(bot)
    states_dict[id].render(message, connection)

@bot.message_handler(content_types=['text'])
def handle_messages(message):
    id = message.from_user.id
    if id not in states_dict:
        states_dict[id] = states_dict.Start(bot)
    
    states_dict[id] = states_dict[id].next(message, connection)
    states_dict[id].render(message, connection)
    print(states_dict)

@app.route('/', methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = tb.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=WEB_HOOK_URL)
    print('ITS WORKING')
    app.run(host=APP_HOST, port=APP_PORT, debug=True)