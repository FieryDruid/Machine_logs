from tkinter.filedialog import askopenfilename
from tkinter import Tk

from typing import Tuple, Optional
import time
from datetime import datetime, timedelta
import os
import csv

import time
import re

import sys

#type = 1 - фиксированное окно по времени
#type = 2 - скользящее окно по времени
type = 2
file_start = 1
if len(sys.argv)> 1:
    type = int(sys.argv[1])


first = True
if type == 1:
	print("Выбрано фиксированное окно по времени")

else:
	print("Выбрано скользящее окно по времени")


def parse_file(file_path: str) -> list:
	with open(file_path, 'r', encoding='utf-8', newline='') as file:
		reader = csv.reader(file)

		data = list(reader)
		print (len(data))
		return data

formatter = '%H:%M:%S'


def parse_data(data, window_duration, window_shift):
	logs = data[1:]  # -заголовки

	time_limit = timedelta(minutes=window_duration * 2)

	slice_from = 0
	time_pred = get_time(logs[0])
	result = []

	for i, event in enumerate(logs):
		time_next = get_time(event)
		# если следующая дата раньше предыдущей или разница между следующей и предыдущей больше какого-то лимита, то мы нашли разрыв
		if time_next < time_pred or time_next - time_pred > time_limit:
			result += get_sliding_windows(logs[slice_from:i], window_duration, window_shift)
			slice_from = i
		time_pred = time_next

	result += get_sliding_windows(logs[slice_from:], window_duration, window_shift)

	return result

def write_csv(dates: list, filename):
	with open(f'../{filename}_eventid.csv', 'w', encoding='utf-8', newline='') as file:
		writer = csv.writer(file)
		if filename == "data":
			writer.writerows(dates)
		else:
			for row in dates:
				writer.writerows(row)


def enter_shift() -> Optional[int]:
	try:
		shift = input("Enter a shift and window size: ")
		return int(shift) if shift.isdigit() else None
	except ValueError:
		print('Enter a num!')
		return enter_shift()


def enter_csv() -> str:
	dirs = os.listdir('C:/Diplom/programm/Logs')

	return dirs

def get_time(event_record):
	return datetime.strptime(event_record[1][:-4], "%d-%m-%Y %H:%M:%S")


def get_sliding_windows(events, window_duration, window_shift):
	duration = timedelta(minutes=window_duration)
	shift = timedelta(minutes=window_shift)

	start_time = get_time(events[0])
	end_time = start_time + duration
	windows = []

	while 1:
		# поиск первого элемента в окне
		for i, event in enumerate(events):
			if get_time(event) >= start_time:
				start_index = i
				break
		# если не нашли, лог обработан => выход из while
		else:
			break

		window = []
		for event in events[start_index:]:
			if get_time(event) <= end_time:
				window.append(event[6])
			else:
				break
		windows.append(window)

		start_time += shift
		end_time = start_time + duration
	return windows

if __name__ == '__main__':

	windows = []
	all_files=[]


	done = False
	shift = enter_shift()
	window_size = 45 #Можно вводить выводом enter_shift()

	dirs = enter_csv()
	for directory in dirs:
		if os.path.isdir(f"C:/Diplom/programm/Logs/{directory}"):
			files = os.listdir(f"C:/Diplom/programm/Logs/{directory}")
			for file in files:
				if ".csv_structured.csv" in f"C:/Diplom/programm/Logs/{directory}/{file}":
					file_path = f"C:/Diplom/programm/Logs/{directory}/{file}"
					filename = file

					data = parse_file(file_path)
					if filename == "data.csv_structured.csv":
						write_csv(parse_data(data, window_size, shift), "data")
						print("Файл data Добавлен!")
						break
					all_files.append(parse_data(data, window_size, shift))
					print(f"Файл {filename} обработан!")
	write_csv(all_files, "all_logs")
	print("Общий файл успешно склеен!")
