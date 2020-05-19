import telebot
import config
import tools
from pprint import pprint

bot = telebot.TeleBot(config.TOKEN)


def run_bot():  # запускает обработчик сообщений

    try:
        options = tools.js_read()
    except FileNotFoundError:
        options = {}

    @bot.message_handler(content_types=['text'])
    def dialog(message):
        user_id = str(message.from_user.id)

        if message.text == 'parse':
            if options.get(user_id):  # если пользователь уже существует
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
            tools.js_read()
            pprint(options)

        else:
            bot.send_message(user_id, 'Используйте команду "parse" для активации бота')
            pprint(options)

    bot.polling(none_stop=False)


def send_tasks(user_id, tasks, options, keyword):  # отправляет результат парсинга
    for task in tasks[0:3]:  # для удобства тестирования отправляет 3 сообщения [0:3]
        # if task['id'] > options[user_id]['history'][keyword]:
        bot.send_message(user_id, task['title'] + ' ' + task['link'] + ' ' + task['price']['count'])
