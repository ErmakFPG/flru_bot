from parse import parse
import tools
from pprint import pprint


try:
    options = tools.js_read()
    pprint(options)
    print('')
except FileNotFoundError:
    options = {}
    print('Not found')

for user_id, setting in options.items():
    if setting['status'] == 'tuned':
        tasks = parse(setting['current_keyword'])
