from parse import parse
import tools
from pprint import pprint
import time
import bot


def parse_for_current_settings(data):

    for user_id, setting in data.items():

        keyword = setting['current_keyword']

        if setting['status'] == 'turned':

            tasks = parse(keyword)

            if not setting['history'].get(keyword):  # если ключевого слова еще не было в истории
                last_task_id = 0
            else:
                last_task_id = int(setting['history'][keyword]['last_task_id'])

            for task in tasks:
                if int(task['id']) > last_task_id:
                    last_task_id = int(task['id'])

            bot.send_tasks(user_id, tasks)

            data[user_id]['history'][keyword] = {'last_task_id': last_task_id, 'last_tasks': tasks}
            data[user_id]['status'] = 'prepare_to_send'
            tools.js_write(data)
            pprint(data)


def start_monitoring():
    while True:
        try:
            options = tools.js_read()
            parse_for_current_settings(options)
        except FileNotFoundError:
            print('Not found')
        print('хуй')
        time.sleep(5)


start_monitoring()
