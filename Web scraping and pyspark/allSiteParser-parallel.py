# Затрачено 833.7029304504395 сек.
import time
import concurrent.futures
import importlib

# список скриптов
SCRIPTS = [
    'siteParser-1socapteka',
    'siteParser-aptekaotsklada',
    'siteParser-farma',
    'siteParser-gorzdrav',
    'siteParser-planetazdorovo',
    'siteParser-vita',
    'siteParser-zdorov',
    'siteParser-zdrav',
    'siteParser-zhivayapteka',
    'siteParser-zhivika',
]

# функция запуска python-файла
def start_script(name):
    print(f'Скрипт {name}: запущен')
    mod = importlib.import_module(name)
    mod.parse()
    print(f'Скрипт {name}: завершён')

start = time.time()

# запускаем параллельно с установленным максимумом потоков
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(start_script, SCRIPTS)

finish = time.time() - start
print("Затрачено "+str(finish)+" сек.")