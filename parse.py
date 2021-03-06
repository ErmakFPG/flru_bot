import requests
from bs4 import BeautifulSoup as Bs

URL = 'https://www.fl.ru/projects/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
           'accept': '*/*'}
HOST = 'https://www.fl.ru'


def get_html(url, session, params=None):
    r = session.get(url, headers=HEADERS, params=params)
    return r


def post_html(url, session, find, token):
    payload = {
        'action': 'postfilter',
        'kind': '5',
        'pf_category': '',
        'pf_subcategory': '',
        'comboe_columns%5B1%5D': '0',
        'comboe_columns%5B0%5D': '0',
        'comboe_column_id': '0',
        'comboe_db_id': '0',
        'comboe': '%D0%92%D1%81%D0%B5+%D1%81%D0%BF%D0%B5%D1%86%D0%B8%D0%B0%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8',
        'location_columns%5B1%5D': '0',
        'location_columns%5B0%5D': '0',
        'location_column_id': '0',
        'location_db_id': '0',
        'location': '%D0%92%D1%81%D0%B5+%D1%81%D1%82%D1%80%D0%B0%D0%BD%D1%8B',
        'pf_pro_only': '1',
        'pf_cost_from': '',
        'pf_cost_to': '',
        'pf_keywords': find,
        'u_token_key': token
       }
    session.post(url, headers=HEADERS, data=payload)


def get_token(url, session, token_count=34):
    for el in get_html(url, session):
        if 'U_TOKEN_KEY' in str(el):
            end = str(el).find(';')
            return str(el)[end - token_count: end]


def get_pages_count():
    return 1


def find_price(html):
    start = html.find('&nbsp')
    end = html.rfind('&nbsp')
    count = html[start - 4: start].replace('>', '').replace('a', '').strip()

    if start != end:
        count += html[end - 3: end]

    html_end = html[end:]

    if 'euro' in html_end:
        currency = 'EUR'
    elif '$' in html_end:
        currency = 'USD'
    elif '₽' in html_end:
        currency = 'RUB'
    else:
        count = None
        currency = None

    return {'count': count, 'currency': currency}


def get_content(html):
    soup = Bs(html, 'html.parser')
    items = soup.find_all('div', class_='b-post_padbot_15')

    tasks = []
    for item in items:
        tasks.append({
            'title': item.find('a', class_='b-post__link').get_text(),
            'link': HOST + item.find('a', class_='b-post__link').get('href'),
            'price': find_price(str(item.find('script'))),
            'id': int(item.find('a', class_='b-post__link').get('name')[3:])
        })
    return tasks


def parse(find):
    s = requests.Session()

    post_html(URL, s, find, get_token(URL, s))
    tasks = []
    pages_count = get_pages_count()
    for page in range(pages_count):
        html = get_html(URL, s, params={'page': page + 1})
        tasks.extend(get_content(html.text))
    return tasks
