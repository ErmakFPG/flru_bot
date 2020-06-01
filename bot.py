import monitoring
import telebot
import config
import tools
from pprint import pprint
import time
from telebot import apihelper


apihelper.proxy = {'https': 'socks5h://733764577:lQZjuqmu@orbtl.s5.opennetwork.cc:999'}


bot = telebot.TeleBot(config.TOKEN)


def run_bot():  # запускает обработчик сообщений

    @bot.message_handler(content_types=['text'])
    def dialog(message):

        try:
            options = tools.js_read()
        except FileNotFoundError:
            options = {}

        user_id = str(message.from_user.id)
        first_word = message.text.split()[0]

        try:
            second_word = message.text.split()[1]
        except IndexError:
            second_word = ''

        # ------------------------ START COMMANDS ------------------------
        if first_word == 'start':

            if message.text == 'start':
                if not options.get(user_id):
                    bot.send_message(user_id, 'В истории нет ключевых слов для поиска')
                else:
                    for keyword in options[user_id]:
                        options[user_id][keyword]['status'] = 'active'
                    bot.send_message(user_id, 'Активирован поиск по ключевым словам из истории')

            elif not options.get(user_id):
                options[user_id] = {second_word: {'last_task_id': 0, 'status': 'active'}}
                bot.send_message(user_id, 'Активирован поиск по ключевому слову')

            elif options.get(user_id) and second_word not in options[user_id].keys():
                options[user_id][second_word] = {'last_task_id': 0, 'status': 'active'}
                bot.send_message(user_id, 'Активирован поиск по ключевому слову')

            else:
                options[user_id][second_word]['status'] = 'active'
                bot.send_message(user_id, 'Активирован поиск по ключевому слову')

        # ------------------------ STOP COMMANDS ------------------------
        elif first_word == 'stop':
            if message.text == 'stop':
                if not options.get(user_id):
                    bot.send_message(user_id, 'История пустая, нечего останавливать')
                else:
                    for keyword in options[user_id]:
                        options[user_id][keyword]['status'] = 'passive'
                    bot.send_message(user_id, 'Поиск остановлен')

            elif not options.get(user_id):
                bot.send_message(user_id, 'Настройки пользователя остутствуют')

            elif options.get(user_id) and second_word not in options[user_id].keys():
                bot.send_message(user_id, 'Ключевого слова нет в истории')

            else:
                options[user_id][second_word]['status'] = 'passive'
                bot.send_message(user_id, 'Поиск по ключевому слову остановлен')

        # ------------------------ GET COMMAND ------------------------
        elif message.text == 'get' and options.get(user_id):
            bot.send_message(user_id, f"`{str(options[user_id])}`", parse_mode='Markdown')

        elif message.text == 'get' and not options.get(user_id):
            bot.send_message(user_id, 'Настройки пользователя отсутствуют')

        elif message.text == 'get_all':
            bot.send_message(user_id, f"`{options}`", parse_mode='Markdown')

        # ------------------------ REMOVE COMMAND ------------------------
        elif first_word == 'remove':

            if message.text == 'remove':
                bot.send_message(user_id, 'Корректная команда: "remove keyword"')

            elif not options.get(user_id):
                bot.send_message(user_id, 'Настройки пользователя отсутствуют')

            elif options.get(user_id) and second_word not in options[user_id].keys():
                bot.send_message(user_id, 'Ключевого слова нет в настройках')

            else:
                options[user_id].pop(second_word)
                bot.send_message(user_id, f'Ключевое слово "{second_word}" удалено из настроек')

        # ------------------------ CLEAR COMMAND ------------------------
        elif message.text == 'clear' and not options.get(user_id):
            bot.send_message(user_id, 'Настройки пользователя отстутствуют')

        elif message.text == 'clear':
            options.pop(user_id)
            bot.send_message(user_id, 'Настройки пользователя удалены')

        # ------------------------ OTHER COMMANDS ------------------------
        else:
            bot.send_message(user_id, 'Команды:\n"start *keyword*" - начать поиск по ключевому слову'
                                      '\n"start" - начать поиск по всем ключевым словам из истории'
                                      '\n"stop *keyword*" - остановить поиск по ключевому слову'
                                      '\n"stop - остановить поиск по всем ключевым словам из истории'
                                      '\n"get" - показать настройки пользователя\n"get_all" - показать все настройки'
                                      '\n"remove *keyword*" - удалить ключевое слово из истории'
                                      '\n"clear" - очистить историю пользователя')

        tools.js_write(options)
        pprint(options)

    bot.polling(none_stop=False)


def send_tasks(user_id, tasks):  # отправляет результат парсинга
    for task in tasks[0:3]:  # для удобства тестирования отправляет 3 сообщения [0:3]
        bot.send_message(user_id, f"{task['title']} {task['link']} {task['price']['count']} "
                                  f"{task['price']['currency']}")

        time.sleep(1)
