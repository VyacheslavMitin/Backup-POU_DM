# Модуль резервного копирования баз ПО 'Участок инкассации'
# Python 3.8
__author__ = 'Vyacheslav Mitin <vyacheslav.mitin@gmail.com>'
__version__ = '3'

# Импорты
from datetime import datetime
import configparser
import os
import subprocess
import sys
import glob
import shutil
from print_log import *

ULYANOVSK = 'Администратор'  # имя на сервере 1С-V8
DIMITROVGRAD = 'user'  # имя у Боровикова

if os.getlogin() == ULYANOVSK:
    CITY = 'ulyanovsk'
elif os.getlogin() == DIMITROVGRAD:
    CITY = 'dimitrovgrad'
else:  # выход с ошибкой если не то имя логина в систему
    sys.exit("Не подходящий логин в систему!")

ARCH_EXT = 'SevenZ'
NOW_DATE = datetime.now().strftime('%d.%m.%Y')  # Текущая дата для работы с файлами и каталогами в формате 01.01.2021
NOW_TIME = datetime.now().strftime('%H-%M')  # Текущее время в формате 15-00
NOW_WEEKDAY = datetime.now().strftime('%A')  # Текущий день недели в формате Monday
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # путь к папке с модулем

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
    BACKUP_DIR_CLOUD = cfg.get('PATHS', 'backup_dir_dm_yandex')
    SQL_SCRIPT = cfg.get('PATHS', 'sql_script_dm')


# Функции
def make_dirs():
    """Функция создания каталогов для работы модуля"""
    dirs = [TEMP_DIR, LOGS_DIR]
    [os.makedirs(os.path.join(SCRIPT_DIR, dir_), exist_ok=True) for dir_ in dirs]


def logging():
    """Функция логирования действий модуля"""
    pass  # TODO сделать логирование текстовым файлом


def cleaning_temp():
    """Функция очистки временной папки"""
    print_log("Очистка временной папки")

    [os.remove(files) for files in glob.glob(TEMP_DIR + '//' + '*')]


def backuping():
    """Функция выгрузки баз 'ПО Участок инкассации'"""
    print_log("Старт резервного копирования базы 'ПО Участок инкассации'")

    print_log("Работа SQL, начало:", line_before=True)
    subprocess.run([
        'sqlcmd', '-i', SQL_SCRIPT  # вызов программы со скриптом как параметр для выгрузки
    ], timeout=600)
    print_log("Работа SQL, конец", line_after=True)

    print_log("Окончание резервного копирования базы 'ПО Участок инкассации'")


def compressing(base=''):
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


def moving_files():
    """Функция перемещения баз 'ПО Участок инкассации'"""
    print_log("Копирование и перемещение сжатых баз 'ПО Участок инкассации'")

    def working_with_archives(mode=''):
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
    print_log("Начало работы скрипта по резервному копированию баз 'ПО Участок инкассации'",
              line_before=True, line_after=True)
    cleaning_temp()  # очистка временной папки
    make_dirs()  # создание каталогов для работы модуля
    backuping()  # резервная копия SQL базы через 'SQLCMD' в 'POU*.bak' файл
    compressing()  # сжатие файла 'POU*.bak' в архив 7zip
    moving_files()  # копирование и перемещение файлов
    cleaning_temp()  # очистка временной папки
    print_log("Окончание работы скрипта по резервному копированию баз 'ПО Участок инкассации'",
              line_before=True, line_after=True)
