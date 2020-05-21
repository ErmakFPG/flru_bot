import telebot
import config
import tools
from pprint import pprint
import time

bot = telebot.TeleBot(config.TOKEN)


def run_bot():  # запускает обработчик сообщений

    @bot.message_handler(content_types=['text'])
    def dialog(message):

        try:
            options = tools.js_read()
        except FileNotFoundError:
            options = {}

        user_id = str(message.from_user.id)

        # ------------------------ CLEAR COMMAND ------------------------
        # if message.text == 'clear' and not options.get(user_id):
        #     bot.send_message(user_id, 'Настройки пользователя отсутствуют')
        #
        # elif message.text == 'clear' and options.get(user_id):  # and options['status'] != 'pending':
        #     options[user_id]['clear'] = True
        #     tools.js_write(options)
        #     bot.send_message(user_id, 'Вы уверены, молодой человек? Введите \'yes\' или \'no\'')
        #
        # elif options.get(user_id) and options[user_id]['clear']:  # and options['status'] != 'pending':
        #
        #     if message.text == 'yes':
        #         options.pop(user_id)
        #         tools.js_write(options)
        #         bot.send_message(user_id, 'История удалена')
        #     elif message.text == 'no':
        #         options[user_id]['clear'] = False
        #         tools.js_write(options)
        #         bot.send_message(user_id, 'Запрос на удаление истории отменен')
        #     else:
        #         bot.send_message(user_id, 'Введите \'yes\' или \'no\'')

        # ------------------------ PARSE COMMAND ------------------------
        if message.text == 'parse':
            if options.get(user_id):
                options[user_id]['status'] = 'pending'
            else:
                options[user_id] = {'status': 'pending', 'history': {}}

            bot.send_message(user_id, 'Введите ключевое слово')
            tools.js_write(options)

        elif options.get(user_id) and options[user_id]['status'] == 'pending':
            options[user_id]['current_keyword'] = message.text
            options[user_id]['status'] = 'ready'
            tools.js_write(options)

        # ------------------------ GET COMMAND ------------------------
        # elif message.text == 'get' and options.get(user_id):
        #     bot.send_message(user_id, f"`{str(options[user_id])}`", parse_mode='Markdown')
        #
        # elif message.text == 'get' and not options.get(user_id):
        #     bot.send_message(user_id, 'Настройки пользователя отсутствуют')

        # ------------------------ OTHER COMMANDS ------------------------
        # elif message.text == 'stop' and options.get(user_id) and options[user_id]['status'] == 'ready':
        #     options[user_id]['status'] = 'stopped'
        #     tools.js_write(options)

        else:
            bot.send_message(user_id, 'Используйте команды:\n"parse" - активация бота\n"stop" - остановка бота')

        pprint(options)

    bot.polling(none_stop=False)


def send_tasks(user_id, tasks, options, keyword):  # отправляет результат парсинга
    for task in tasks[0:3]:  # для удобства тестирования отправляет 3 сообщения [0:3]
        if task['id'] > options[user_id]['history'][keyword]:
            bot.send_message(user_id, f"{task['title']} {task['link']} {task['price']['count']} "
                                      f"{task['price']['currency']}")

        time.sleep(1)
