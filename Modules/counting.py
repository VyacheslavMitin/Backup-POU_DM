# Модуль создания папок и счета запуска

# Импорты
import os
import sys
from configs import LOGS_DIR, COUNT


# if __name__ == '__main__':
#     LOGS_DIR: str = os.path.join('..', LOGS_DIR)  # путь до каталога с логами
# else:
#     LOGS_DIR: str = os.path.join(LOGS_DIR)  # путь до каталога с логами, если запускается основной модуль

# if not os.path.isdir(LOGS_DIR):
#     import main
#     main.make_dirs()

FILE_COUNT = os.path.join(LOGS_DIR, COUNT)
if not os.path.isfile(FILE_COUNT):
    with open(FILE_COUNT, 'w') as file:
        file.write(str(0))


def read_count() -> int:
    """Функция чтения файла-счетчика или его создания"""
    if os.path.isfile(FILE_COUNT):
        with open(FILE_COUNT, 'r') as file_count:
            count: int = int(file_count.read())
            return count
    else:
        sys.exit("Ошибка: нет файла-счетчика")


def write_count() -> None:
    """Функция записи файла-счетчика"""
    count: int = read_count()
    count += 1
    with open(FILE_COUNT, 'w') as file_count:
        file_count.write(str(count))


write_count()
