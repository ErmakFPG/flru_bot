import requests
from bs4 import BeautifulSoup as BS
import csv

URL = 'https://www.fl.ru/projects/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
           'accept': '*/*'}
HOST = 'https://www.fl.ru'
FILE = 'Tasks.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count():
    return 1


def find_price(html):
    start = html.find('&nbsp')
    end = html.rfind('&nbsp')
    count = html[start - 4: start].replace('>', '').replace('a', '').strip()

    if start != end:
        count += html[end - 3: end]

    if 'euro' in html:
        currency = 'EUR'
    elif '$' in html:
        currency = 'USD'
    elif '₽' in html:
        currency = 'RUB'
    else:
        count = None
        currency = None

    return {'count': count, 'currency': currency}


def get_content(html):
    soup = BS(html, 'html.parser')
    items = soup.find_all('div', class_='b-post_padbot_15')

    tasks = []
    for item in items:
        tasks.append({
            'title': item.find('a', class_='b-post__link').get_text(),
            'link': HOST + item.find('a', class_='b-post__link').get('href'),
            'price': find_price(str(item.find('script')))
        })
    return tasks


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Title', 'Link', 'Count', 'Currency'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['price']['count'], item['price']['currency']])


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        tasks = []
        pages_count = get_pages_count()
        for page in range(pages_count):
            html = get_html(URL, params={'page': page + 1})
            tasks.extend(get_content(html.text))
        save_file(tasks, FILE)
        print('All done')
    else:
        print('Error')


parse()
