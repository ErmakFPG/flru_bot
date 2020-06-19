from parse import parse
import tools
import time
import bot
import datetime


def parse_for_current_settings():
    options = tools.js_read()
    for user_id, settings in options.items():
        if settings['time'] is not None:
            start_time = datetime.time(settings['time'][0], settings['time'][1])
            end_time = datetime.time(settings['time'][2], settings['time'][3])
        else:
            start_time = datetime.time(0, 0)
            end_time = datetime.time(23, 59)
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
                    if options_new.get(user_id):  # для обхода KeyError при очистке истории во время парсинга
                        options_new[user_id]['keywords'][keyword]['last_task_id'] = new_last_task_id
                        tools.js_write(options_new)


def start_monitoring():
    while True:
        parse_for_current_settings()
        time.sleep(600)
