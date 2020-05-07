from parse import parse
import tools
from pprint import pprint


try:
    options = tools.js_read()
except FileNotFoundError:
    options = {}
    print('Not found')

for user_id, setting in options.items():  # файл может быть пустым, тогда произойдет ошибка

    keyword = setting['current_keyword']
    pprint(keyword)

    if setting['status'] == 'turned':

        tasks = parse(keyword)

        if not setting['history'].get(keyword):  # если ключа еще не было в истории
            last_task_id = 0
        else:
            last_task_id = int(setting['history'][keyword]['last_task_id'])

        for task in tasks:
            if int(task['id']) > last_task_id:
                last_task_id = int(task['id'])

        options[user_id]['history'] = {keyword: {'last_task_id': last_task_id, 'last_tasks': tasks}}
        tools.js_write(options)

    pprint(options)
