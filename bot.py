import monitoring
import telebot
import config
import tools
from pprint import pprint
import time
from telebot import apihelper
import datetime

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
        command = message.text.split()[0]

        try:
            args = ''.join(message.text.split()[1:])
        except IndexError:
            args = ''

        if command == 'start':
            execute_start(user_id, options, args, message)
        elif command == 'stop':
            execute_stop(user_id, options, args, message)
        elif message.text == 'get':
            execute_get(user_id, options)
        elif message.text == 'get_all':
            bot.send_message(user_id, f"`{options}`", parse_mode='Markdown')
        elif command == 'remove':
            execute_remove(user_id, options, args)
        elif message.text == 'clear':
            execute_clear(user_id, options)
        elif command == 'time':
            execute_time(user_id, options, args)
        else:
            execute_help(user_id)

        pprint(options)

    bot.polling(none_stop=False)


def execute_start(user_id, options, args, message):
    if message.text == 'start':
        if not options.get(user_id):
            bot.send_message(user_id, 'В истории нет ключевых слов для поиска')
        else:
            for keyword in options[user_id]['keywords']:
                options[user_id]['keywords'][keyword]['status'] = 'active'
            bot.send_message(user_id, 'Активирован поиск по ключевым словам из истории')
            tools.js_write(options)
            monitoring.parse_for_current_settings()

    elif not options.get(user_id):
        options[user_id] = {'keywords': {args: {'last_task_id': 0,
                                                'status': 'active'}},
                            'time': None}
        bot.send_message(user_id, f'Активирован поиск по ключевому слову "{args}"')
        tools.js_write(options)
        monitoring.parse_for_current_settings()

    elif args not in options[user_id]['keywords'].keys():
        options[user_id]['keywords'][args] = {'last_task_id': 0, 'status': 'active'}
        bot.send_message(user_id, f'Активирован поиск по ключевому слову "{args}"')
        tools.js_write(options)
        monitoring.parse_for_current_settings()

    else:
        options[user_id]['keywords'][args]['status'] = 'active'
        bot.send_message(user_id, f'Активирован поиск по ключевому слову "{args}"')
        tools.js_write(options)
        monitoring.parse_for_current_settings()


def execute_stop(user_id, options, args, message):
    if message.text == 'stop':
        if not options.get(user_id):
            bot.send_message(user_id, 'История пустая, нечего останавливать')
        else:
            for keyword in options[user_id]['keywords']:
                options[user_id]['keywords'][keyword]['status'] = 'passive'
            bot.send_message(user_id, 'Поиск остановлен')
            tools.js_write(options)

    elif not options.get(user_id):
        bot.send_message(user_id, 'Настройки пользователя остутствуют')

    elif args not in options[user_id]['keywords'].keys():
        bot.send_message(user_id, 'Ключевого слова нет в истории')

    else:
        options[user_id]['keywords'][args]['status'] = 'passive'
        bot.send_message(user_id, f'Поиск по ключевому слову "{args}" остановлен')
        tools.js_write(options)


def execute_get(user_id, options):
    if options.get(user_id):
        bot.send_message(user_id, f"`{str(options[user_id])}`", parse_mode='Markdown')
    else:
        bot.send_message(user_id, 'Настройки пользователя отсутствуют')


def execute_remove(user_id, options, args):
    if not options.get(user_id):
        bot.send_message(user_id, 'Настройки пользователя отсутствуют')
    elif args not in options[user_id]['keywords'].keys():
        bot.send_message(user_id, f'Ключевого слова "{args}" нет в настройках')
    else:
        options[user_id]['keywords'].pop(args)
        bot.send_message(user_id, f'Ключевое слово "{args}" удалено из настроек')
        tools.js_write(options)


def execute_clear(user_id, options):
    if options.get(user_id):
        options.pop(user_id)
        bot.send_message(user_id, 'Настройки пользователя удалены')
        tools.js_write(options)
    else:
        bot.send_message(user_id, 'Настройки пользователя отстутствуют')


def execute_time(user_id, options, args):
    if args and options.get(user_id):

        try:
            my_time = [el.split(':') for el in args.split('-')]
            my_time = list(map(int, my_time[0] + my_time[1]))
            test_my_time = dict(start_time=datetime.time(my_time[0], my_time[1]),
                                stop_time=datetime.time(my_time[2], my_time[3]))
            if test_my_time['stop_time'] > test_my_time['start_time']:
                options[user_id]['time'] = my_time
                tools.js_write(options)
                bot.send_message(user_id, 'Задачи будут направляться в указанное время, но это не точно')
            else:
                bot.send_message(user_id, 'Введено некорректное время')

        except ValueError:
            bot.send_message(user_id, 'Введено некорректное время')
        except IndexError:
            bot.send_message(user_id, 'Введено некорректное время')

    else:
        execute_help(user_id)


def execute_help(user_id):
    bot.send_message(user_id, 'Команды:\n"start *keyword*" - начать поиск по ключевому слову'
                              '\n"start" - начать поиск по всем ключевым словам из истории'
                              '\n"stop *keyword*" - остановить поиск по ключевому слову'
                              '\n"stop - остановить поиск по всем ключевым словам из истории'
                              '\n"get" - показать настройки пользователя\n"get_all" - показать все настройки'
                              '\n"remove *keyword*" - удалить ключевое слово из истории'
                              '\n"clear" - очистить историю пользователя'
                              '\n"time XX:XX-XX:XX" - задать время отправки сообщений')


def send_tasks(user_id, tasks, keyword):  # отправляет результат парсинга
    for task in tasks:

        if task['price']['count'] is None:
            task['price']['count'] = 'без ценника'
            task['price']['currency'] = ''

        keyboard = telebot.types.InlineKeyboardMarkup()
        link_button = telebot.types.InlineKeyboardButton(text="Подробнее", url=task['link'])
        keyboard.add(link_button)
        bot.send_message(user_id, f"{keyword} - {task['price']['count']} {task['price']['currency']}\n"
                                  f"{task['title']} ", reply_markup=keyboard)

        time.sleep(1)
