from parse import parse
import tools
import time
import bot


def parse_for_current_settings(options):

    for user_id, setting in options.items():

        if setting['status'] == 'turned':

            keyword = setting['current_keyword']
            tasks = parse(keyword)

            if not setting['history'].get(keyword):
                last_task_id = 0
                options[user_id]['history'][keyword] = 0

            else:
                last_task_id = int(setting['history'][keyword])

            bot.send_tasks(user_id, tasks, options, keyword)

            for task in tasks:
                if int(task['id']) > last_task_id:
                    last_task_id = int(task['id'])

            options[user_id]['history'][keyword] = last_task_id

    tools.js_write(options)


def start_monitoring():
    while True:
        try:
            options = tools.js_read()
            parse_for_current_settings(options)
        except FileNotFoundError:
            pass

        time.sleep(10)


start_monitoring()
