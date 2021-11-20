# Модуль резервного копирования баз ПО 'Участок инкассации'
# Python 3.8
MODULE = "Резервное копирование баз ПО 'Участок инкассации'"
__author__ = 'Vyacheslav Mitin <vyacheslav.mitin@gmail.com>'
__version__ = '5'

# Импорты
from datetime import datetime
import glob
from Modules.print_log import *
from Modules.configs import *
from Modules.counting import *
from Modules.logging import *

# Переменные
ARCH_EXT: str = 'SevenZ'
NOW_DATE: str = datetime.now().strftime('%d.%m.%Y')  # Текущая дата в формате 01.01.2021
NOW_TIME: str = datetime.now().strftime('%H-%M')  # Текущее время в формате 15-00
NOW_WEEKDAY: str = datetime.now().strftime('%A')  # Текущий день недели в формате Monday
SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))  # путь к папке с модулем


# Функции
def welcome(name_: str, author_: str, version_: str) -> None:
    print(f"МОДУЛЬ РАБОТЫ С '{name_}'")
    print(f"Автор модуля: '{author_}'")
    print(f"Версия модуля: '{version_}\n'")


def make_dirs() -> None:
    """Функция создания каталогов для работы модуля"""
    dirs = [TEMP_DIR, LOGS_DIR]  # список с каталогами для создания
    [os.makedirs(os.path.join(SCRIPT_DIR, dir_), exist_ok=True) for dir_ in dirs]  # создание каталогов по списку


def cleaning_temp() -> None:
    """Функция очистки временной папки"""
    print_log("Очистка временной папки")

    [os.remove(files) for files in glob.glob(TEMP_DIR + '//' + '*')]  # удаление всех файлов во временном каталоге


def backuping() -> None:
    """Функция выгрузки баз 'ПО Участок инкассации'"""
    print_log("Старт резервного копирования базы 'ПО Участок инкассации'")

    print_log("Работа SQL, начало:", line_before=True)
    subprocess.run([
        'sqlcmd', '-i', SQL_SCRIPT  # вызов программы со скриптом как параметр для выгрузки
    ], timeout=600)
    print_log("Работа SQL, конец", line_after=True)

    print_log("Окончание резервного копирования базы 'ПО Участок инкассации'")


def compressing(base: str = '') -> None:
    """Функция сжатия баз 'ПО Участок инкассации' архиватором"""
    print_log("Старт компрессии баз 'ПО Участок инкассации'")

    if CITY == 'ulyanovsk':
        base = 'UL'
    elif CITY == 'dimitrovgrad':
        base = 'DM'

    os.chdir(TEMP_DIR)  # переход во временную папку для сжатия без каталога

    print_log("Работа архиватора, начало:", line_before=True)
    for bases in glob.glob(f'POU_{base}_*.bak'):  # архивация с паролем
        subprocess.run([  # вызов архиватора 7zip с параметрами
            EXE_7Z,  # путь к архиватору
            "a", "-t7z", "-m0=LZMA2:mt=6", "-mx=0", "-ssw",  # параметры для работы 7Zip
            f"POU_{base}_{NOW_DATE}_{NOW_WEEKDAY}_{NOW_TIME}.{ARCH_EXT}",  # итоговый файл
            bases,  # файл для архивирования
            "-p" + PASS_7Z  # пароль
        ], timeout=600)
    print_log("Работа архиватора, конец", line_after=True)

    os.chdir(SCRIPT_DIR)  # возврат в папку модуля

    print_log("Окончание компрессии баз 'ПО Участок инкассации'")


def moving_files() -> None:
    """Функция перемещения баз 'ПО Участок инкассации'"""
    print_log("Копирование и перемещение сжатых баз 'ПО Участок инкассации'")

    def working_with_archives(mode: str = '') -> None:
        """Функция работы с архивами баз"""
        archives_list = []  # создание листа с объектами - сжатыми базами
        [archives_list.append(archives) for archives in glob.glob(TEMP_DIR + '//' + f'*.{ARCH_EXT}')]

        if mode == 'copy':  # копия на NAS
            [shutil.copy(archives, BACKUP_DIR_NAS) for archives in archives_list]
        elif mode == 'move':  # перемещения в облако
            [shutil.move(archives, BACKUP_DIR_CLOUD) for archives in archives_list]

    if CITY == 'ulyanovsk':  # работа и с NAS и с облаком
        working_with_archives(mode='copy')  # копия на NAS
        working_with_archives(mode='move')  # перемещение в облако
    elif CITY == 'dimitrovgrad':  # только перемещения в облако
        working_with_archives(mode='move')


if __name__ == '__main__':  # старт
    welcome(MODULE, __author__, __version__)
    cleaning_temp()  # очистка временной папки
    make_dirs()  # создание каталогов для работы модуля
    backuping()  # резервная копия SQL базы через 'SQLCMD' в 'POU*.bak' файл
    compressing()  # сжатие файла 'POU*.bak' в архив 7zip
    moving_files()  # копирование и перемещение файлов
    cleaning_temp()  # очистка временной папки
    print_log("Окончание работы скрипта по резервному копированию баз 'ПО Участок инкассации'",
              line_before=True, line_after=True)
