import random
import string
from datetime import datetime, timedelta
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import psycopg2
from psycopg2 import sql
import numpy as np

# Константы для скрипта
MIN_POSITIVE_EVEN_INTEGER = 1
MAX_POSITIVE_EVEN_INTEGER = 100000000
POSITIVE_FLOAT_MIN = 1
POSITIVE_FLOAT_MAX = 20
STRING_LENGTH = 10
COUNT_FILES = 1
LINES_PER_FILE = 1000
PATTERN_TO_REMOVE = 'abc'
YEARS_AGO = 5
DAYS_AGO = 365 * YEARS_AGO
OUTPUT_FILE = 'merged_output.txt'


class DataGenerator:
    @staticmethod
    def generate_random_date():
        """Генерирует случайную дату за последние 5 лет."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=DAYS_AGO)
        random_date = start_date + timedelta(days=random.randint(0, DAYS_AGO))
        return random_date.strftime('%d.%m.%Y')

    @staticmethod
    def generate_random_string(length):
        """Генерирует случайную строку из латинских символов."""
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    @staticmethod
    def generate_random_russian_string(length):
        """Генерирует случайную строку из русских символов."""
        return ''.join(chr(random.randint(0x0410, 0x44F)) for _ in range(length))

    @staticmethod
    def generate_random_positive_even_integer():
        """Генерирует случайное положительное четное целочисленное число."""
        return random.randint(MIN_POSITIVE_EVEN_INTEGER, MAX_POSITIVE_EVEN_INTEGER) * 2

    @staticmethod
    def generate_random_positive_float():
        """Генерирует случайное положительное число с 8 знаками после запятой."""
        return round(random.uniform(POSITIVE_FLOAT_MIN, POSITIVE_FLOAT_MAX), 8)

    @classmethod
    def generate_random_line(cls):
        """Генерирует строку с случайными данными."""
        date = cls.generate_random_date()
        latin_chars = cls.generate_random_string(STRING_LENGTH)
        russian_chars = cls.generate_random_russian_string(STRING_LENGTH)
        even_integer = cls.generate_random_positive_even_integer()
        positive_float = cls.generate_random_positive_float()

        return f"{date}||{latin_chars}||{russian_chars}||{even_integer}||{positive_float}||"


class FileProcessor:
    @staticmethod
    def generate_and_save_file(file_path, num_lines=LINES_PER_FILE):
        """Генерирует и сохраняет файл с указанным количеством строк."""
        with open(file_path, 'w', encoding='utf-8') as file:
            for _ in range(num_lines):
                line = DataGenerator.generate_random_line()
                file.write(line + '\n')

    @staticmethod
    def merge_and_remove_strings(file_paths, pattern_to_remove, output_file):
        """Объединяет файлы и удаляет строки с заданным паттерном."""
        total_removed_lines = 0

        with open(output_file, 'w', encoding='utf-8') as output_file:
            for file_path in file_paths:
                with open(file_path, 'r', encoding='utf-8') as input_file:
                    lines = input_file.readlines()

                    # Удаление строк с заданным паттерном
                    removed_lines = [line for line in lines if pattern_to_remove not in line]
                    total_removed_lines += len(lines) - len(removed_lines)

                    # Запись оставшихся строк в объединенный файл
                    output_file.writelines(removed_lines)

        print(f"Объединение завершено. Удалено {total_removed_lines} строк.")


class DatabaseManager:
    @staticmethod
    def create_connection():
        """Создает соединение с базой данных."""
        return psycopg2.connect(
            database="my_db",
            user="postgres",
            password="admin",
            host="localhost",
            port="5432"
        )

    @staticmethod
    def create_table(connection):
        """Создает таблицу в базе данных."""
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS my_table (
                          date TEXT,
                          latin_chars TEXT,
                          russian_chars TEXT,
                          even_integer INTEGER,
                          positive_float REAL)''')
        connection.commit()

    @staticmethod
    def get_data_from_file():
        """Импортирует данные из файла"""

        with open(OUTPUT_FILE, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            data = [tuple(line.strip().split('||'))[:-1] for line in lines]

        return data

    @staticmethod
    def insert_data(cls, data):
        """Вставляет данные в таблицу."""
        connection = cls.create_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO my_table VALUES (%s, %s, %s, %s, %s)",
            data
        )
        connection.commit()

    @staticmethod
    def sum_of_integers(connection):
        """Считает сумму всех целых чисел."""
        cursor = connection.cursor()
        cursor.execute("SELECT SUM(even_integer) FROM my_table")
        result = cursor.fetchone()[0]
        return result if result else 0

    @staticmethod
    def median_of_floats(connection):
        """Вычисляет медиану всех дробных чисел."""
        cursor = connection.cursor()
        cursor.execute("SELECT positive_float FROM my_table")
        floats = [row[0] for row in cursor.fetchall()]
        median = np.median(floats)
        return median if not np.isnan(median) else 0


if __name__ == '__main__':
    # Измерение времени выполнения
    start_program = time.time()

    # Генерация и сохранение ста файлов с 100000 строк каждый параллельно
    with ProcessPoolExecutor() as executor:
        executor.map(FileProcessor.generate_and_save_file, [f'file{i}.txt' for i in range(1, COUNT_FILES + 1)])

    # Объединение файлов и удаление строк с паттерном 'abc'
    FileProcessor.merge_and_remove_strings([f'file{i}.txt' for i in range(1, COUNT_FILES + 1)], PATTERN_TO_REMOVE, OUTPUT_FILE)

    # Импорт данных в базу данных
    data = DatabaseManager.get_data_from_file()
    connection = DatabaseManager.create_connection()
    DatabaseManager.create_table(connection)

    start_time = time.time()

    with ThreadPoolExecutor() as executor:
        futures_to_data = {executor.submit(DatabaseManager.insert_data, DatabaseManager, d): d for d in data}
        total_lines = len(data)
        processed_lines = 0
        for future in as_completed(futures_to_data):
            processed_lines += 1
            data = futures_to_data[future]
            try:
                future.result()
            except Exception as e:
                print(f"Ошибка при вставке данных: {e}")
            print(f"Строк импортировано: {processed_lines}. Строк осталось:{total_lines - processed_lines}.")

    print(f"Время вставки данных в таблицу: {time.time() - start_time} секунд.")

    # Считаем сумму всех целых чисел
    start_time = time.time()

    integer_sum = DatabaseManager.sum_of_integers(connection)
    print(f"Сумма всех целых чисел: {integer_sum}")

    # Вычисляем медиану всех дробных чисел
    float_median = DatabaseManager.median_of_floats(connection)
    print(f"Медиана всех дробных чисел: {float_median}")
    print(f"Время выполнения подсчетов: {time.time() - start_time} секунд.")
    connection.close()

    print(f"Время выполнения: {time.time() - start_program} секунд.")
