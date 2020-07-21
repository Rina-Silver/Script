# это м.б. неактуально для анаконды
import os
from os import sys
from os import path
import time

os.environ['JAVA_HOME'] = r"C:\Java"
#sys.path.append(r"C:\Python38\Lib\site-packages\pyspark\python")

# импортируем что нужно
from pyspark import SparkContext
from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.types import *
import pyspark.sql.functions as func

# путь к текущей папке скрипта
scr_dir = path.dirname(path.abspath(__file__))
# пути к csv файлам
csv_file_in = scr_dir + r'\allWords.csv' #исходный файл

csv_file_out = scr_dir + r'\Результаты'


sc = SparkContext()
sqlContext = SQLContext(sc)
df = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true', sep=';').load(csv_file_in)

SITES = {
    'https://zdravcity.ru/': 'zdrav',
    'https://aptekavita.ru/': 'vita',
    'https://apteka-ot-sklada.ru/': 'aptekaotsklada',
    'https://farmakopeika.ru/': 'farma',
    'https://gorzdrav.org/': 'gorzdrav',
    'https://apteka.planetazdorovo.ru/': 'planetazdorovo',
    'https://apteka.tomsk.ru/': 'zhivayapteka',
    'http://первая-социальная-аптека.рф/': '1socapteka',
    'https://zdorov.ru/': 'zdorov',
    'https://www.aptekazhivika.ru/': 'zhivika',
    }

# словарь топ 200 для каждого сайта
top200 = {}

# Получить список 200 наиболее используемых слов из полученного текста для каждого сайта
start = time.time()
for url in SITES:
    name_key = SITES[url]
    top200[url] = (df
            .filter(df['site'] == url)
            .groupBy('word', 'site')
            .count()
            .orderBy('count', ascending=False)
            .limit(200))
    print(f'Сайт "{url}", 200 самых частых слов...')
    file_path = csv_file_out + '/' + name_key + '.csv'
    #top200[url].toPandas().to_csv(file_path)
    top200[url].show(200)
finish1 = time.time() - start

#exit()
# Найти слова, которые попадают в список для одних сайтов и отсутствуют на других

# переменная для объединённого запроса топ 200 всех сайтов
start = time.time()
top200_merged = None

for url in SITES:
    tmp_df = top200[url]
    if top200_merged is None:
        top200_merged = tmp_df
    else:
        top200_merged = top200_merged.unionAll(tmp_df)

# удалим кол-во раз, что встречается слово на сайте
top200_merged = top200_merged.drop('count')

words_count = (top200_merged
        .groupBy('word')
        .count())
uniques_tmp = words_count.filter(words_count['count'] == 1)
uniques_words = [x['word'] for x in uniques_tmp.select('word').collect()]

uniques = top200_merged.filter(top200_merged['word'].isin(uniques_words))
print(f'Слова, которые попадают в список для одних сайтов и отсутствуют на других...')
uniques.show(20)
#exit()
finish2 = time.time() - start

# Найти слова, которые присутствуют в списках для всех сайтов
start = time.time()
sites_cnt = len(SITES)

universal_tmp = words_count.filter(words_count['count'] == sites_cnt)
universal_words = [x['word'] for x in universal_tmp.select('word').collect()]

universals = top200_merged.select('word').filter(top200_merged['word'].isin(universal_words)).distinct()
print(f'Всего сайтов: {sites_cnt}; слова которые встречаются на всех...')
universals.show(600)
finish3 = time.time() - start

print("Затрачено "+str(finish1)+" сек. задание №1")
print("Затрачено "+str(finish2)+" сек. задание №2")
print("Затрачено "+str(finish3)+" сек. задание №3")