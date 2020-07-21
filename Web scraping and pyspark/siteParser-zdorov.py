import requests
from bs4 import BeautifulSoup
from os import path
import csv
import os
import re

scr_dir = path.dirname(path.abspath(__file__))
csv_file_out = scr_dir + r'\CSV\zdorov.csv'

URL = 'https://zdorov.ru/catalog/344/354?size=30'
HOST = 'https://zdorov.ru'
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
    pagination = soup.find('li', class_='last').find('a')
    if pagination:
        href = pagination.get('href')
        res = re.findall(r'Goods_page=(\w+)&size=30', href)[0]
        return int(res)
    else:
        return 1
    

def get_goods(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='good_desc')
    goods = []
    for item in items:
        #title = item.find('h3', class_='proposition_name').get_text(strip=True)
        #nameblock = item.find('div', class_='proposition_title')
        link = item.find('a').get('href')
        #city = item.find('svg', class_='svg-i16_pin').find_next('strong').get_text(strip=True)
        if link not in goods:
            goods.append(HOST+link)
    return goods


def get_content(link):
    html=get_html(link)
    soup = BeautifulSoup(html.text, 'html.parser')
    title = soup.find('div', id='topheader').get_text(strip=True)
    description = "Без описания"
    find_div = soup.find('td', id='slider')
    if find_div:
        description = find_div.get_text()
    return {'link':link, 'title':title, 'description':description}

#print(pages_count)
       # exit()


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        goods = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count+1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'Goods_page': page})
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