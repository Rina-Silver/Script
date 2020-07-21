import requests
from bs4 import BeautifulSoup
from os import path
import csv
import os
import re
import string
import time

#pip install nltk
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
#скачать stopwords в Corpora
#скачать punkt в Models
#nltk.download()

scr_dir = path.dirname(path.abspath(__file__))
csv_file_out = scr_dir + r'\allWords.csv'

#стоп-слова на русском
ext_words = stopwords.words('russian')
ext_words.extend(stopwords.words('english'))
ext_words.extend([
    'кап', 'х', 'мкг', 'мг', 'мл', 'это', 'гкс', 'паж', 'д', 'др', 'г', 'ад', 'ч/з', 'ра', 'кг', 'ст', 'п', 'па', 'ср', 
    'р', 'экг', 'цнс', 'сут', 'н', 'т', 'ч', 'ил', 'е', 'кажд', 'лс', 'ооо', 'ди', 'м', 'ва', 'л', 'оао', 'ф', 'ю', 'юсб',
    'ао', '/сут', 'oy', 'г/л', 'ггт', 'жкт', 'кк', 'см', 'ту', 'щф', 'мин', 'мг/сут', 'также', 'в/м', 'таб', 'зао', 'мл/мин',
    'шт',
    'x', 'p', 'ige', 'd', 'qt', 'h', 'r', 'ltd', 'auc', 's', 'a', 'pvt', 'hl', 'dr', 'lge', 'al', 'ax', 'c', 'ci', 'cl',
    'cyp', 'fd', 'g', 'hpc', 'i', '°c', 'ii', '°с', 'il', 'l', 'n', 'paf', 'q', 'qtc', 'th',
    '/', '+', '', "''", '``', "'", '–', '—', '*', '**', '[', ']', '±', '≤', '≥', '°', '№',
    ])
STOP_WORDS = set(ext_words)

#список файлов и сайтов
FILES = {
    'zdravcity.csv': 'https://zdravcity.ru/',
    'aptekavita.csv': 'https://aptekavita.ru/',
    'aptekaotsklada.csv': 'https://apteka-ot-sklada.ru/',
    'farmakopeika.csv': 'https://farmakopeika.ru/',
    'gorzdrav.csv': 'https://gorzdrav.org/',
    'planetazdorovo.csv': 'https://apteka.planetazdorovo.ru/',
    'zhivayapteka.csv': 'https://apteka.tomsk.ru/',
    '1socapteka.csv': 'http://первая-социальная-аптека.рф/',
    'zdorov.csv': 'https://zdorov.ru/',
    'zhivika.csv': 'https://www.aptekazhivika.ru/',

}

#функция, принимающая текст и отдающая список слов
def text_processing(text):
    #заменим цифры, скобки, знаки препинания и дефисы на пробелы
    text = re.sub(r'[«»<>=%!&?.,;:()1234567890-]', ' ', text)
    #используем word_tokenize для разбиения текста на список слов
    words = word_tokenize(text)
    #принудительно приводим к нижнему регистру
    words = [word.lower() for word in words]
    #исключаем стоп-слова
    words = [w for w in words if not w in STOP_WORDS]
    return words

#список для всех слов
all_words = []
#индексатор для слов
a_count = 0

start = time.time()

#цикл по всем файлам
for f in FILES:
    #текущий сайт
    site = FILES[f]
    print(f'Обработка файла {f}, сайт {site}...')

    #индексатор для описаний с сайта
    f_count = -1

    #путь к целевому файлу
    filepath = scr_dir + '/CSV/' + f

    #читаем csv файл
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            #если первая строка - пропускаем, это заголовок
            f_count+=1
            if f_count == 0:
                continue

            print(f'Обработка описания {f_count}...')

            text = row[2]
            if text=='Без описания' or text=='':
                continue
            words = text_processing(text)

            #добавляем все слова в общий список
            for w in words:
                all_words.append({
                    'id': a_count,
                    'site': site,
                    'word': w
                })
                a_count+=1

finish = time.time() - start
print("Затрачено "+str(finish)+" сек.")

#запишем слова в файл
with open(csv_file_out, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['id', 'site', 'word'])
    for w in all_words:
        writer.writerow([w['id'], w['site'], w['word']])
