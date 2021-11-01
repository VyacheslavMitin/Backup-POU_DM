# Модуль резервного копирования баз ПО 'Участок инкассации'
# Python 3.8
__author__ = 'Vyacheslav Mitin <vyacheslav.mitin@gmail.com>'
__version__ = '1 - разработка'

# Импорты
import time
from datetime import datetime
import configparser
import os
import subprocess
import sys
import glob
import shutil


PC_LOGIN = os.getlogin()
mitin = 'Администратор'
borovikov = 'user'

if PC_LOGIN == mitin:
    CITY = 'ulyanovsk'
elif PC_LOGIN == borovikov:
    CITY = 'dimitrovgrad'
else:  # выход с ошибкой если не то имя логина в систему
    sys.exit("Не то имя логина в систему")

ARCH_EXT = 'SevenZ'
NOW_DATE = datetime.now().strftime('%d.%m.%Y')  # Текущая дата для работы с файлами и каталогами
NOW_TIME = datetime.now().strftime('%H-%M')  # Текущее время
NOW_WEEKDAY = datetime.now().strftime('%A')  # Текущий день недели

cfg = configparser.ConfigParser()
cfg.read('settings.ini')  # чтение локального конфига
TEMP_DIR = cfg.get('PATHS', 'temp_dir')
LOGS_DIR = cfg.get('PATHS', 'logs_dir')
SQL_SCRIPT = cfg.get('PATHS', 'sql_script')
EXE_7Z = cfg.get('PATHS', '7zip')
PASS_7Z = cfg.get('PATHS', 'pass_7z')
if CITY == 'ulyanovsk':
    BACKUP_DIR = cfg.get('PATHS', 'backup_dir_ul')
elif CITY == 'dimitrovgrad':
    BACKUP_DIR = cfg.get('PATHS', 'backup_dir_dm')


# Функции
def print_log(text, line_before=False, line_after=False):
    """Функция формирования читабельной записи текущего действия.
    Параметры line_before=False, line_after=False для необходимости новых линий ДО и ПОСЛЕ вывода."""

    def time_log():
        """Функция формирования читабельной записи текущего времени (без даты)."""
        log_time = time.strftime("%H:%M:%S")  # формат '10:10:10'
        return log_time

    if line_before:  # линия ДО вывода сообщения
        print()  # пустая строка

    print(f" {time_log()} | {text}")  # формат ' 13:05:02 | Текст'

    if line_after:  # линия ПОСЛЕ вывода сообщения
        print()  # пустая строка


def cleaning_temp():
    print_log("Очистка временной папки")
    for files in glob.glob(TEMP_DIR + '/' + '*'):
        os.remove(files)


def backuping():
    """Функция резервного копирования"""
    cleaning_temp()
    print_log("Старт резервного копирования базы 'ПО Участок инкассации'")

    subprocess.run([
        'sqlcmd', '-i', SQL_SCRIPT  # вызов программы со скриптом как параметр для выгрузки
    ], timeout=600)


def compressing(base=''):
    """Функция сжатия базы"""
    print_log("Сжатие баз 'ПО Участок инкассации'")
    if CITY == 'ulyanovsk':
        base = 'UL'
    elif CITY == 'dimitrovgrad':
        base = 'DM'

    for bases in glob.glob(TEMP_DIR + '/' + f'POU_{base}_*.bak'):
        print(bases)
        subprocess.run([
            EXE_7Z,
            "a", "-t7z", "-m0=LZMA2:mt=6", "-mx=0", "-ssw",  # параметры для работы 7Zip
            TEMP_DIR + '//' + f"POU_{base}_{NOW_DATE}_{NOW_WEEKDAY}_{NOW_TIME}.{ARCH_EXT}",  # итоговый файл
            bases,  # файл для архивирования
            "-p" + PASS_7Z
        ], timeout=600)


def moving_files():
    print("Перемещение сжатых баз 'ПО Участок инкассации'")
    for files in glob.glob(TEMP_DIR + '/' + f'*.{ARCH_EXT}'):
        shutil.move(files, BACKUP_DIR)
    cleaning_temp()


print("Начало работы скрипта по резеврному копированию баз 'ПО Участок инкассации'")
backuping()
compressing()
moving_files()
print("Окончание работы скрипта по резеврному копированию баз 'ПО Участок инкассации'")
