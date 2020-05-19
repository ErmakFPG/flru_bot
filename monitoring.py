from parse import parse
import tools
import time
import bot


def parse_for_current_settings(options):

    for user_id, setting in options.items():

        keyword = setting['current_keyword']

        if setting['status'] == 'turned':

            tasks = parse(keyword)

            if not setting['history'].get(keyword):  # если ключевого слова еще не было в истории
                last_task_id = 0
            else:
                last_task_id = int(setting['history'][keyword])

            for task in tasks:
                if int(task['id']) > last_task_id:
                    last_task_id = int(task['id'])

            options[user_id]['history'][keyword] = last_task_id
            tools.js_write(options)

            bot.send_tasks(user_id, tasks, options, keyword)


def start_monitoring():
    while True:
        try:
            options = tools.js_read()
            parse_for_current_settings(options)
        except FileNotFoundError:
            pass

        time.sleep(10)


start_monitoring()
