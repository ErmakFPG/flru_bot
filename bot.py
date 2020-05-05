import telebot
import config
from pprint import pprint

bot = telebot.TeleBot(config.TOKEN)
options = {}


@bot.message_handler(content_types=['text'])
def dialog(message):
    user_id = message.from_user.id
    message_id = message.chat.id
    user_options = options.get(user_id)

    if options.get(user_id) and options.get(user_id).get('status') == 'pending':
        options[user_id]['status'] = 'tuned'
        options[user_id]['current_keyword'] = message.text
        pprint(options)

    elif message.text == 'parse':
        options[user_id] = {'status': 'pending', 'chat_id': message_id}
        bot.send_message(message_id, 'Введите ключевое слово')
        pprint(options)

    elif message.text == 'dump':
        pprint(options)
        bot.send_message(message_id, 'Изи дамп')
        pprint(options)

    else:
        bot.send_message(message_id, 'Не понимаю :(')
        pprint(options)


# RUN
bot.polling(none_stop=True)
