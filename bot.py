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
    user_id = message.from_user.id
    message_id = message.chat.id
    # user_options = options.get(user_id)

    if options.get(user_id) and options.get(user_id).get('status') == 'pending':
        options[user_id]['status'] = 'tuned'
        options[user_id]['current_keyword'] = message.text
        bot.send_message(message_id, 'Кручу-верчу, пропарсить хочу')
        pprint(options)

    elif message.text == 'parse':

        if options.get(user_id):
            options[user_id]['status'] = 'pending'
            options[user_id]['chat_id'] = message_id
        else:
            options[user_id] = {'status': 'pending', 'chat_id': message_id}

        bot.send_message(message_id, 'Введите ключевое слово')
        pprint(options)

    elif message.text == 'dump':
        pprint(options)
        bot.send_message(message_id, 'Изи дамп')

    else:
        bot.send_message(message_id, 'Не понимаю :(')
        pprint(options)


# RUN
bot.polling(none_stop=True)
