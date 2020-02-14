#Версия python 3.7.1
import re, csv

legend = {
    'A': 'Added',
    'C': 'Conflict',
    'D': 'Deleted',
    'M': 'Modified',
    'R': 'Replaced',
    'X': 'Externals',
    'I': 'Ignored',
    '?': 'Item is not under version control',
    '!': 'Item is missing',
    '~': 'Item is versioned as one kind of object (replaced by a different kind of object)',
    'L': 'Locked',
    '+': 'Yes',
    'K': 'Locked in this working copy',
    'O': 'Locked either by another user or in another working copy',
    'T': 'Locked and is invalid',
    'B': 'Broken'
}

myData = [
    [
        "Статус файла",
        "Свойста файлов и каталогов",
        "Свойства рабочей области",
        "Добавление с историей",
        "Переключение на ветку",
        "Блокировка",
        "Конфликт дерева",
        "Есть более новая версия файла",
        "Ревизия файла в текущей копии проекта",
        "Последняя ревизия",
        "Автор изменений",
        "Директория",
        "Комментарий"
    ]
]

f = open('.\\данные.txt')
# цикл для обработки строк и добавления в массив
for line in f.readlines():
#если комментарий, то добавляем в конец предыдущей строки
    if line[6] == ">":
        myData[-1].append(line[10:])
        continue
#парсинг строк    
    a = line[0:7]+line[8]
    b = line[10:]
    result = re.sub(r'\s+', ' ', b)
    arrB = result.split()
    
    LineA = list(a)
#добавление столбцов в случае наличия знака    
    if a[0] == '?':
        for i in range(3):
            LineA.append('')
    
    LineA += arrB
    
    myData.append(LineA)
#количество элементов в массиве
lineCnt = len(myData)
#пропуская первый элемент, заменяем буквы, определяющие состояние файла
for i in range(lineCnt):
    if i == 0:
        continue
    for j in range(8):
        s = myData[i][j]
        if s != ' ':
            myData[i][j] = legend[s]


myFile = open('script.csv', 'w')
with myFile:
    writer = csv.writer(myFile, delimiter=';')
    writer.writerows(myData)
     
print("Writing complete")   
