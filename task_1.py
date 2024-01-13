import random
from datetime import datetime, timedelta
import time
from concurrent.futures import ProcessPoolExecutor

class DataGenerator:
    @staticmethod
    def generate_random_date():
        """Генерирует случайную дату за последние 5 лет."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1825)  # 5 years ago
        random_date = start_date + timedelta(days=random.randint(0, 1825))
        return random_date.strftime('%d.%m.%Y')

    @staticmethod
    def generate_random_string(length):
        """Генерирует случайную строку из латинских символов."""
        return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') for _ in range(length))

    @staticmethod
    def generate_random_russian_string(length):
        """Генерирует случайную строку из русских символов."""
        return ''.join(random.choice('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя') for _ in range(length))

    @staticmethod
    def generate_random_positive_even_integer():
        """Генерирует случайное положительное четное целочисленное число."""
        return random.randint(2, 50000000) * 2  # Generating positive even integers

    @staticmethod
    def generate_random_positive_float():
        """Генерирует случайное положительное число с 8 знаками после запятой."""
        return round(random.uniform(1, 20), 8)

    @classmethod
    def generate_random_line(cls):
        """Генерирует строку с случайными данными."""
        date = cls.generate_random_date()
        latin_chars = cls.generate_random_string(10)
        russian_chars = cls.generate_random_russian_string(10)
        even_integer = cls.generate_random_positive_even_integer()
        positive_float = cls.generate_random_positive_float()

        return f"{date}||{latin_chars}||{russian_chars}||{even_integer}||{positive_float}||"

class FileProcessor:
    @staticmethod
    def generate_and_save_file(file_path, num_lines=100000):
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
        executor.map(FileProcessor.generate_and_save_file, [f'file{i}.txt' for i in range(1, 101)])

    # Объединение файлов и удаление строк с паттерном 'abc'
    FileProcessor.merge_and_remove_strings([f'file{i}.txt' for i in range(1, 101)], 'abc', 'merged_output.txt')

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Время выполнения: {elapsed_time} секунд.")
