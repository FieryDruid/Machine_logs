# Machine_logs

**Обратите внимание, что данный проект предназначен для бинарной классификации**. Аномальная запись либо есть (1), либо ее нет (0). 

# 1. Подготовка данных.

Изначальный лог-файл в формате **.log** подается на вход модуля **regex.py** для структурирования.

Результат работы модуля regex отправляется на вход модуля **Drain_demo.py**. Результатом его работы являются два файла: ***.structured.csv** и ***.templates.scv**.

Файл шаблонов **(*.templates.csv)** содержит в себе каждый тип события с его уникальным идентификатором. Мы можем использовать для отметки аномальных событий (Вручную, экспертным методом. Для первичного обучения моделей. Смотри пункт 1.3).

## 1.1 Выделение признаков методом фиксированного окна по количеству событий

Структурированный файл **(*.structured.csv)** подается на вход модуля **Eventid_parse.py**. В параметрах запуска вторым элементом после названия файла указывается количество событий в окне.

Например, **"python Eventid_parse.py 7"** - установит размер окна в 7 событий. За размер смещения овтечает переменная **"start"** (61 строка).

На выходе получаем файл ***_eventid.csv**

## 1.2 Выделение признаков методом фиксированного/скользящего окна по времени

### 1.2.1 Если изначальный лог-файл является склейкой нескольких более мелких

В таком случае, желательно повторить пункт 1 для каждого более мелкого файла из составных во избежание ошибок. Модуль перебирает папки, по-очереди парсит каждый и склеивает в общий.

Дальнейшее описание смотри в пункте 1.2.2

### 1.2.2 Если изначальный лог-файл является цельным и записанным за один определенный промежуток времени

Структурированный файл **(*.structured.csv)** подается на вход модуля **time_windows_logs.py**. В параметрах запуска вторым элементом после названия файла указывается тип окна.

Например, при **"python time_windows_logs.py 1"** - будет выбрано фиксированное окно по времени (2 для скользящего).

Переменные **"shift"** (128 строка) и **"window_size"** (129 строка) отвечают за размер сдвига и размер окна. Учтите, что время указывается в минутах!

На выходе получаем файл ***_eventid.csv**.


## 1.3 Поиск аномальных записей в тренировочном наборе

Предполагается, что у Вас уже есть файл шаблонов с отмеченными аномальными записями.
В переменной **"anomalies_id"** хранится имя файла с метками.

При запуске программы выберите файл, полученный в результате пункта 1.2 **(*_eventid.csv)**

Результаторм работы модуля будет точно такой же файл, но с добавлением столбца с пометками аномалий - ***_anomalies.csv**.

## 1.4 Кодирование строковых признаков

Поскольку алгоритмы машинного обучения могут плохо работать с текстовыми данными, их необходимо закодировать.

Для этого, результат пункта 1.2 **(*_eventid.csv)** подается на вход модуля **coder.py**

На выходе получаем файл ***_coder_res.csv**

## 1.5 Обучение модели и поиск аномалий

При запуске модуля **app.py** выберите файл, полученный в результате работы пункта 1.4 **(*_coder_res.py)**

В строке 44 данного модуля первым параметром указывается название файла результата пункта 1.3 **(*_anomalies.csv)**
В строках 49 и 50 указываются названия файлов для поиска аномалий


#Результат

В результате работы модуля **app.py** мы получаем текстовый файл **results.txt** и видим ROC кривые для каждого классификатора.
Все эти данные нам необходимы для оценки эффективности классификации разными методами и окончательного выбора.
