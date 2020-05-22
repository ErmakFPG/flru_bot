from parse import parse
import tools
import time
import bot


def parse_for_current_settings(options):
    for user_id, setting in options.items():
        if setting['status'] == 'ready':
            keyword = setting['current_keyword']

            if setting['history'].get(keyword):
                last_task_id = int(setting['history'][keyword])
            else:
                last_task_id = 0

            tasks = parse(keyword)
            tasks_for_send = []
            new_last_task_id = last_task_id

            for task in tasks:
                if task['id'] > last_task_id:
                    tasks_for_send.append(task)
                if task['id'] > new_last_task_id:
                    new_last_task_id = task['id']

            bot.send_tasks(user_id, tasks_for_send)
            options = tools.js_read()
            options[user_id]['history'][keyword] = new_last_task_id
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
