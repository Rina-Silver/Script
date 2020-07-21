import time
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

# запускаем последовательно
for s in SCRIPTS:
    start_script(s)

finish = time.time() - start
print("Затрачено "+str(finish)+" сек.")