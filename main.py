# Модуль резервного копирования баз ПО 'Участок инкассации'
# Python 3.8
__author__ = 'Vyacheslav Mitin <vyacheslav.mitin@gmail.com>'
__version__ = '1 - разработка'

# Импорты
from datetime import datetime
import configparser
import os
import subprocess
import sys
import glob
import shutil
from print_log import *

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
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

cfg = configparser.ConfigParser()
cfg.read('settings.ini')  # чтение локального конфига
TEMP_DIR = cfg.get('PATHS', 'temp_dir')
LOGS_DIR = cfg.get('PATHS', 'logs_dir')
EXE_7Z = cfg.get('PATHS', '7zip')
PASS_7Z = cfg.get('PATHS', 'pass_7z')
if CITY == 'ulyanovsk':
    BACKUP_DIR_NAS = cfg.get('PATHS', 'backup_dir_ul_nas')
    BACKUP_DIR_CLOUD = cfg.get('PATHS', 'backup_dir_ul_yandex')
    SQL_SCRIPT = cfg.get('PATHS', 'sql_script_ul')
elif CITY == 'dimitrovgrad':
    BACKUP_DIR_CLOUD = cfg.get('PATHS', 'backup_dir_dm')
    SQL_SCRIPT = cfg.get('PATHS', 'sql_script_dm_yandex')


# Функции
def make_dirs():
    """Функция создания каталогов"""
    dirs = [TEMP_DIR, LOGS_DIR]
    for dir_ in dirs:
        os.makedirs(os.path.join(SCRIPT_DIR, dir_), exist_ok=True)


def logging():
    """Функция логирования"""
    pass  # TODO сделать логирование текстовым файлом


def cleaning_temp():
    print_log("Очистка временной папки")
    for files in glob.glob(TEMP_DIR + '//' + '*'):
        os.remove(files)


def backuping():
    """Функция резервного копирования баз 'ПО Участок инкассации'"""
    cleaning_temp()  # очистка временной папки
    print_log("Старт резервного копирования базы 'ПО Участок инкассации'")

    subprocess.run([
        'sqlcmd', '-i', SQL_SCRIPT  # вызов программы со скриптом как параметр для выгрузки
    ], timeout=600)  # , encoding='1251')

    print_log("Окончание резервного копирования базы 'ПО Участок инкассации'")


def compressing(base=''):
    """Функция сжатия баз 'ПО Участок инкассации'"""
    print_log("Старт компрессии баз 'ПО Участок инкассации'")

    if CITY == 'ulyanovsk':
        base = 'UL'
    elif CITY == 'dimitrovgrad':
        base = 'DM'

    os.chdir(TEMP_DIR)  # переход во временную папку для сжатия без каталога

    for bases in glob.glob(f'POU_{base}_*.bak'):  # архивация с паролем
        subprocess.run([
            EXE_7Z,
            "a", "-t7z", "-m0=LZMA2:mt=6", "-mx=0", "-ssw",  # параметры для работы 7Zip
            f"POU_{base}_{NOW_DATE}_{NOW_WEEKDAY}_{NOW_TIME}.{ARCH_EXT}",  # итоговый файл
            bases,  # файл для архивирования
            "-p" + PASS_7Z
        ], timeout=600)

    os.chdir(SCRIPT_DIR)  # возврат в папку скрипта

    print_log("Окончание компрессии баз 'ПО Участок инкассации'")


def moving_files():
    """Функция перемещения баз"""
    print("Копирование и перемещение сжатых баз 'ПО Участок инкассации'")

    def working_with_archives(mode=''):
        """Функция работы с файлами"""
        archives_list = []  # создание листа с объектами - сжатыми базами
        for archives in glob.glob(TEMP_DIR + '//' + f'*.{ARCH_EXT}'):
            archives_list.append(archives)

        if mode == 'copy':  # копия на NAS
            [shutil.copy(archives, BACKUP_DIR_NAS) for archives in archives_list]
        elif mode == 'move':  # перемещения в облако
            [shutil.move(archives, BACKUP_DIR_CLOUD) for archives in archives_list]

    if CITY == 'ulyanovsk':
        working_with_archives(mode='copy')
        working_with_archives(mode='move')
    elif CITY == 'dimitrovgrad':
        working_with_archives(mode='move')

    cleaning_temp()  # очистка временной папки


if __name__ == '__main__':  # Старт
    print("Начало работы скрипта по резеврному копированию баз 'ПО Участок инкассации'")
    make_dirs()
    backuping()
    compressing()
    moving_files()
    print("Окончание работы скрипта по резеврному копированию баз 'ПО Участок инкассации'")
