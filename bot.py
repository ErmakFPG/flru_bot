import telebot
import config
import parse
from pprint import pprint

bot = telebot.TeleBot(config.TOKEN)
options = {}


@bot.message_handler(content_types=['text'])
def dialog(message):
    user_id = message.from_user.id
    user_options = options.get(user_id)
    pprint(user_options)

    if message.text == 'parse':
        options[user_id] = {'value': None, 'status': 'pending'}
        bot.send_message(message.chat.id, 'Введите ключевые слова для поиска')

    elif message.text == 'dump':
        pprint(options)
        bot.send_message(message.chat.id, 'Изи дамп')

    else:
        bot.send_message(message.chat.id, 'Не понимаю :(')


# RUN
bot.polling(none_stop=True)
