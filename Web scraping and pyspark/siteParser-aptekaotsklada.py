import requests
from bs4 import BeautifulSoup
from os import path
import csv
import os

scr_dir = path.dirname(path.abspath(__file__))
csv_file_out = scr_dir + r'\CSV\aptekaotsklada.csv'

URL = 'https://apteka-ot-sklada.ru/catalog/medikamenty-i-bady/allergiya/'
HOST = 'https://apteka-ot-sklada.ru'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0', 'accept': '*/*'}


def save_file(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Ссылка', 'Наименование', 'Описание'])
        for item in items:
            writer.writerow([item['link'], item['title'], item['description']])


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('nav', class_='paginator-list').find_all('a')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1
    

def get_goods(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='product-name')
    goods = []
    for item in items:
        #title = item.find('h3', class_='proposition_name').get_text(strip=True)
        #nameblock = item.find('div', class_='proposition_title')
        link = item.get('href')
        #city = item.find('svg', class_='svg-i16_pin').find_next('strong').get_text(strip=True)
        if link not in goods:
            goods.append(HOST+link)
    return goods


def get_content(link):
    html=get_html(link)
    soup = BeautifulSoup(html.text, 'html.parser')
    title = soup.find('h1', class_='product-name').get_text(strip=True)
    description = "Без описания"
    find_div = soup.find('div', class_='good-note-text')
    if find_div:
        description = find_div.get_text()
    return {'link':link, 'title':title, 'description':description}


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        goods = []
        pages_count = get_pages_count(html.text)
        for page in range(0, pages_count):
            page_items = page*10
            print(f'Парсинг страницы {(page+1)} из {pages_count}...')
            html = get_html(URL, params={'start': page_items})
            goods.extend(get_goods(html.text))
        print(f'Получено {len(goods)} товаров')
        items = []
        count = 1
        for good in goods:
            item = get_content(good)
            items.append(item)
            print(f'Парсинг товара {count}...')
            count+=1
            #if count==20:
                #break
        save_file(items, csv_file_out)    
        #os.startfile(csv_file_out)
    else:
        print('Error')

parse()