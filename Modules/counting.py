# Модуль создания папок и счета запуска

# Импорты
import os
import sys
from Modules.configs import LOGS_DIR, COUNT

# Константы
FILE_COUNT = os.path.join(LOGS_DIR, COUNT)  # путь к файлу счетчика


def check_count() -> bool:
    """Функция проверки файла-счетчика или его создания"""

    if not os.path.isfile(FILE_COUNT):  # если файла нет - создать его
        with open(FILE_COUNT, 'w') as file:
            file.write(str(0))

    if os.path.isfile(FILE_COUNT):
        return True
    else:
        sys.exit("Ошибка: нет файла-счетчика")


def read_count() -> int:
    """Функция чтения файла-счетчика"""

    if check_count():
        with open(FILE_COUNT, 'r') as file_count:  # чтение файла
            count: int = int(file_count.read())
            return count
    else:
        sys.exit("Ошибка: нет файла-счетчика")


def write_count() -> int:
    """Функция записи файла-счетчика, а так же вывода значения нового счетчика"""

    count: int = read_count()
    count += 1
    with open(FILE_COUNT, 'w') as file_count:  # перезапись файла
        file_count.write(str(count))

    return count
