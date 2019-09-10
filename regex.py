import re
import csv
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Диалоговое окно выбора файла
Tk().withdraw()  # не отрисовываем окно

file_path = askopenfilename()
filename = re.search(r'\/([\w\-]+)(\.\w+)', file_path).group(1)  # Выделяем имя файла из общего пути

# Открытие файла и отправка его в регулярное выражение
print("Открываю файл...")
file = open(file_path, 'r', newline='')
text = file.read()

csv_filename = f"{filename}.csv"

print("Создаю csv файл...")
with open(csv_filename, 'w', newline='') as file:
    writer = csv.writer(file)
    print("Отправляю текст в регулярное выражение...")
    for entry in re.findall(r"(.*)\s\[(.*)\,.*\,.*\]\s(DEBUG|INFO|WARN|ERROR)\s+(.*)\s\-\s(.*)", text, re.MULTILINE):
        writer.writerow(entry)
    print("Успешно")
