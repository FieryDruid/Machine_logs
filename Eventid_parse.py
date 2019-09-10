import csv
import re
import sys

from tkinter import Tk
from tkinter.filedialog import askopenfilename
#Отрисовываем диалоговое окно выбора файла результатов алгоритма Drain (Templates)
default_methood = 1
if len(sys.argv)> 1:
	default_cols = int(sys.argv[2])
	print(f"[Окно по кол-ву событий] Выбран парсинг по {default_cols} событию(ям)")

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

file_path = askopenfilename()
filename = re.search(r'\/([\w\-]+)(\.\w+)', file_path).group(1) #Выделяем имя файла из пути


with open(file_path, 'r', encoding='utf-8', newline="") as csv_file:
    reader = csv.reader(csv_file)
    file = list(reader)
    row_count = len(file)
    print(row_count)

#Функция записи полученной таблицы в файл
def write(table):
    with open(f'{filename}_eventid.csv', 'w', newline="") as file:
        writer = csv.writer(file)
        writer.writerows(table)


start = 1
table=[]

#По одному событию
def datetime_eventid_list(file, start):
    global table
    for row in file[start:]:
        ids_row = []
        ids_row.append(row[6])
        table.append(ids_row)

#Функция, собирающая все EventID в строки по N элементов вида:
# 1, 2, 3, 4
# 2, 3, 4, 5
# 3, 4, 5, 6
# 4, 5, 6, 7
def eventid_list(file):
    global start, table
    id_rows = []
    for row in file[start:start+default_cols]:
        id_rows.append(row[6])
    table.append(id_rows)


if default_cols == 1:
    datetime_eventid_list(file, start)
else:
    while start+default_cols < row_count:
        eventid_list(file)
        start +=2 #Данный показатель отвечает за размер смещения

write(table)
