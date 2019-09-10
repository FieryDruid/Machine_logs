import numpy as np
import csv
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import OneHotEncoder

from tkinter import Tk
from tkinter.filedialog import askopenfilename
import re

#Отображаем диалоговое окно выбора файла результатов сборки EventID_parse
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

file_path = askopenfilename()
filename = re.search(r'\/([\w\-]+)(\.\w+)', file_path).group(1)



#Функция записи в файл
def write(table):
    with open(f'{filename}_coder_res.csv', 'w', newline="") as file:
        writer = csv.writer(file)
        writer.writerows(table)

#открываем файл с EventID
event_array=[]

with open(file_path, 'r', encoding='utf-8', newline="") as file:
    file_name = csv.reader(file)
    file_list = list(file_name)
    print(len(file_list))
    for row in file_list:
        rows = ""
        for element in row:
            rows += " " + element
        event_array.append(rows)

print(len(event_array))

vectorizer = CountVectorizer()
result = vectorizer.fit_transform(event_array)

write(result.toarray())
