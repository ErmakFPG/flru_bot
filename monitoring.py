from parse import parse
import tools
import time
import bot


def parse_for_current_settings(options):
    for user_id, keywords in options.items():
        for keyword, setting in keywords.items():
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
                options_new[user_id][keyword]['last_task_id'] = new_last_task_id
                tools.js_write(options_new)


def start_monitoring():
    while True:
        try:
            options = tools.js_read()
            parse_for_current_settings(options)
        except FileNotFoundError:
            pass

        time.sleep(600)
