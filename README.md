# Тестовое задание на позицию Python Web developer

## Задание 1
В файле task_1.py находится скрипт который:
- Сгенерирует 100 текстовых файлов со следующей структурой, каждый из которых содержит
100 000 строк:
случайная дата за последние 5 лет || случайный набор 10 латинских символов ||
случайный набор 10 русских символов || случайное положительное четное
целочисленное число в диапазоне от 1 до 100 000 000 || случайное положительное
число с 8 знаками после запятой в диапазоне от 1 до 20
Пример вывода:
03.03.2019||ZAwRbpGUiK||мДМЮаНкуКД||14152932||7,87742021||
23.01.2021||vgHKThbgrP||ЛДКХысХшЗЦ||35085588||8,49822372||
17.10.2023||AuTVNvaGRB||мЧепрИецрА||34259646||17,7248118||
24.09.2014||ArIAASwOnE||ЧпЙМдШлыфУ||23252734||14,6239438||
16.10.2020||eUkiAhUWmZ||ЗэЖЫзЯШАэШ||27831190||8,10838026||

- Объединяет все файлы в один. При объединении удаляет из всех файлов строки с сочетанием символов «abc» с выводом
информации о количестве удаленных строк

- Создает процедуру импорта файлов с таким набором полей в таблицу в СУБД PostgreSQL. При импорте
выводится ход процесса (сколько строк импортировано, сколько осталось)

- Cчитает сумму всех целых чисел и медиану всех дробных чисел

## Задание 2
в папке task_2 находится web-приложение, которое:

- Позволяет создавать/редактировать/удалять вручную Оборотные ведомости по балансовым счетам банков в админ панели Django

- Импортирует excel файлы в СУБД SQLite

- Визуализирует созданную/импортированную Оборотную ведомость по визуальной аналогии с exсel-файлом для каждого
из загруженных файлов

- Все поля которые вычисляются путем математических операций над другими полями определяются самостоятельно и вносятся в соответсвующие ячейки

#### Технологии

- Python 3.10
- Django 5.0.1
- numpy
- openpyxl
- PostgreSQL
- SQLite
- python-dotenv

### Скринкасты с демонстрацией работы скрипта и web приложения находятся в папке screencasts

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:OlegMusatov3000/test-task.git
```

Перейдите в основную директорию проекта 

```
cd test-task
```
В файле .env_copy находится инструкция по заполнению секретных данных для скрипта из 1 задания. Необходимо подключение к базе данных postgres

Cоздать виртуальное окружение:

- Команда для Windows

```
python -m venv venv
```

- Для Linux и macOS:

```
python3.10 -m venv venv
```

Активировать виртуальное окружение:

- Команда для Windows:

```
source venv/Scripts/activate
```

- Для Linux и macOS:

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Запустить скрипт для 1 задания:

```
python task_1.py
```

Перейти в папку c web-приложением для 2 задания:

```
cd task_2
```

Выполнить миграции:

```
python manage.py migrate
```

Создать суперпользователя:

```
python manage.py createsuperuser
```

Запустить проект:

```
python manage.py runserver
```

**_Ссылка на [админ-зону](http://127.0.0.1:8000/admin/ "Гиперссылка к админке.")_**

### Небольшое примечание

Если в процессе запуска и тестирования возникли проблемы, пожалуйста свяжитесь со мной (контакты ниже) для устранения ошибок и решения проблем с запуском

### Автор проекта 
- Олег Мусатов
- Tg: @OlegMusatov