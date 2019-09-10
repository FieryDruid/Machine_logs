import csv
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import re
import numpy as np
import sys

anomalies_file = 1
if len(sys.argv)> 1:
    anomalies_file = int(sys.argv[1])
    print(f"Выбран файл с аномалиями: {anomalies_file}")

#Диалоговое окно для открытия файла с закодированными результатами
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

file_path = askopenfilename()
filename = re.search(r'\/([\w\-]+)(\.\w+)', file_path).group(1)


if anomalies_file == 1:
    anomalies_id = "out_all.csv_templates_labeled.csv" #Файл с пометками о всех аномальных записях
else:
    anomalies_id = "out_all.csv_templates_labeled_2.csv"

table=[]

#Открываем файл кодера
with open(file_path, 'r', encoding='utf-8', newline="") as eventid_file:
    reader = csv.reader(eventid_file)
    eventid = list(reader)


#Открываем файл аномалий и выписываем список аномальных EventID
with open(anomalies_id, 'r', encoding='utf-8', newline="") as anomalies_file:
    reader = csv.reader(anomalies_file)
    anomalies_list=[]
    for row in reader:
        if row[3] == '1':
            anomalies_list.append(row[0])


print(anomalies_list)

#Запись в файл
def write(table):
    with open(f'{filename}_anomalies.csv', 'w', newline="") as file:
        writer = csv.writer(file)
        writer.writerows(table)

#Образование таблицы для записи, если EventID аномальный - нулевым элементом добавляем 1, если нет - 0
def eventid_list(eventid, anomalies_list):
    global table
    for element in eventid:
        for anomaly in anomalies_list:
            if anomaly in element:
                #table.append(1)
                element.insert(0,1)
                print(f"Найдена аномалия {anomaly} in {element}")
                break
        else:
            element.insert(0,0)


eventid_list(eventid, anomalies_list)
write(eventid)
