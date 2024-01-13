import random
import string
from datetime import datetime, timedelta
import time
from concurrent.futures import ProcessPoolExecutor

# Константы для скрипта
MIN_POSITIVE_EVEN_INTEGER = 1
MAX_POSITIVE_EVEN_INTEGER = 100000000
POSITIVE_FLOAT_MIN = 1
POSITIVE_FLOAT_MAX = 20
STRING_LENGTH = 10
COUNT_FILES = 3
LINES_PER_FILE = 100000
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

if __name__ == '__main__':
    # Измерение времени выполнения
    start_time = time.time()

    # Генерация и сохранение ста файлов с 100000 строк каждый параллельно
    with ProcessPoolExecutor() as executor:
        executor.map(FileProcessor.generate_and_save_file, [f'file{i}.txt' for i in range(1, COUNT_FILES + 1)])

    # Объединение файлов и удаление строк с паттерном 'abc'
    FileProcessor.merge_and_remove_strings([f'file{i}.txt' for i in range(1, COUNT_FILES + 1)], PATTERN_TO_REMOVE, OUTPUT_FILE)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Время выполнения: {elapsed_time} секунд.")
