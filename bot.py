import telebot
import config
import json
from pprint import pprint


def js_write(data):
    with open("options.json", "w") as write_file:
        json.dump(data, write_file)


def js_read():
    with open("options.json", "r") as read_file:
        return json.load(read_file)


bot = telebot.TeleBot(config.TOKEN)

try:
    options = js_read()
except FileNotFoundError:
    options = {}


@bot.message_handler(content_types=['text'])
def dialog(message):
    user_id = str(message.from_user.id)
    message_id = message.chat.id
    # user_options = options.get(user_id)

    if message.text == 'parse':
        if options.get(user_id):  # if user is old
            options[user_id]['status'] = 'pending'
            print('old')
        else:
            options[user_id] = {'status': 'pending', 'chat_id': message_id}
            print('new')

        bot.send_message(message_id, 'Введите ключевое слово')
        pprint(options)

    elif options.get(user_id) and options[user_id]['status'] == 'pending':
        options[user_id]['current_keyword'] = message.text
        options[user_id]['status'] = 'turned'
        js_write(options)
        pprint(options)

    elif message.text == 'dump':
        pprint(options)
        bot.send_message(message_id, 'Изи дамп')

    else:
        bot.send_message(message_id, 'Не понимаю :(')
        pprint(options)


# RUN
bot.polling(none_stop=True)
