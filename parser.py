import cards as cards
import requests
from bs4 import BeautifulSoup
import csv

CSV = 'cards.csv'
HOST = 'https://rozetka.com.ua/ua/'
URL = 'https://rozetka.com.ua/ua/mobile-phones/c80003/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='goods-tile__inner')
    cards = []

    for item in items:
        cards.append(
            {
                'title': item.find('span', class_='goods-tile__title').get_text(strip=True),
                'link_product': HOST + item.find('a', class_='goods-tile__heading').get('href'),
                'price': item.find('span', class_='goods-tile__price-value').get_text(strip=True),
#                'image': HOST + item.find('img', class_='lazy_img_hover').get('src')
                'image': item.contents[9].contents[1].attrs['src']
#                'image': HOST + item.find('img', loading='lazy').get('src')
            }
        )

    return cards

def save_doc(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['title', 'price'])
        for item in items:
            writer.writerow([item['title'], item['price']])

def parser():
    PAGENATION = input('set number of pages for parser: ')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, PAGENATION):
            print(f'Parsing is going now:{page}')
            html = get_html(URL, params={'page': page})
            cards.extend(get_content(html.text))
        save_doc(cards, CSV)
    else:
        print('Fucking error')

parser()