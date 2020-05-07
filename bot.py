import telebot
import config
import tools
from pprint import pprint
import time

bot = telebot.TeleBot(config.TOKEN)


def send_tasks(user_id, tasks):  # отправляет результат парсинга
    # options = tools.js_read()
    for task in tasks:
        bot.send_message(user_id, task['title'] + ' ' + task['link'])
        time.sleep(1)


def run_bot():  # запускает обработчик сообщений

    try:
        options = tools.js_read()
    except FileNotFoundError:
        options = {}

    @bot.message_handler(content_types=['text'])
    def dialog(message):
        user_id = str(message.from_user.id)

        if message.text == 'parse':
            if options.get(user_id):  # if user is old
                options[user_id]['status'] = 'pending'
            else:
                options[user_id] = {'status': 'pending', 'history': {}}

            bot.send_message(user_id, 'Введите ключевое слово')
            pprint(options)

        elif options.get(user_id) and options[user_id]['status'] == 'pending':
            options[user_id]['current_keyword'] = message.text
            options[user_id]['status'] = 'turned'
            tools.js_write(options)
            pprint(options)

        elif message.text == 'dump':
            pprint(options)
            bot.send_message(user_id, 'Изи дамп')

        else:
            bot.send_message(user_id, 'Не понимаю :(')
            pprint(options)

    # RUN
    bot.polling(none_stop=False)
