from parse import parse
import tools
import time
import bot
import datetime


def parse_for_current_settings(options):
    for user_id, settings in options.items():
        start_time = datetime.time(9, 0)
        end_time = datetime.time(22, 0)
        current_time = datetime.datetime.now().time()

        if start_time < current_time < end_time:
            for keyword, setting in settings['keywords'].items():
                if setting['status'] == 'active':

                    tasks = parse(keyword)
                    tasks_for_send = []
                    new_last_task_id = setting['last_task_id']

                    for task in tasks:
                        if task['id'] > setting['last_task_id']:
                            tasks_for_send.append(task)
                        if task['id'] > new_last_task_id:
                            new_last_task_id = task['id']

                    bot.send_tasks(user_id, tasks_for_send, keyword)

                    options_new = tools.js_read()
                    options_new[user_id]['keywords'][keyword]['last_task_id'] = new_last_task_id
                    tools.js_write(options_new)


def start_monitoring():
    while True:
        try:
            options = tools.js_read()
            parse_for_current_settings(options)
        except FileNotFoundError:
            pass

        time.sleep(600)
