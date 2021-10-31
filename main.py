# Модуль резервного копирования баз ПО 'Участок инкассации'
# Python 3.8
__author__ = 'Vyacheslav Mitin <vyacheslav.mitin@gmail.com>'
__version__ = '1 - разработка'

# Импорты
import subprocess
import shutil
import glob
# Импорт моих модулей
from ROI_base import *  # мой модуль для вывода времени
import ROI_common  # мой модуль для создания папок, определения дат, запуска проводника


PC_LOGIN = ROI_common.PC_LOGIN  # определение имени пользователя для понимания Ульяновск или Димитровград
mitin = 'Администратор'
borovikov = ROI_common.borovikov

if PC_LOGIN == mitin:
    CITY = 'ulyanovsk'
elif PC_LOGIN == borovikov:
    CITY = 'dimitrovgrad'
else:  # выход с ошибкой если не то имя логина в систему
    sys.exit("Не то имя логина в систему")

ARCH_EXT = 'SEVENZ'
NOW_DATE_TIME_DIR = datetime.now().strftime('%d.%m.%Y')  # Текущая дата для работы с файлами и каталогами

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
def cleaning_temp():
    print_log("Очистка временной папки")
    for files in glob.glob(TEMP_DIR + '/' + '*'):
        os.remove(files)


def backuping():
    """Функция резервного копирования"""
    cleaning_temp()
    print_log("Старт резервного копирования базы Димитровградского 'ПО Участок инкассации'")

    subprocess.run([
        'sqlcmd', '-i', 'SQL_POU.sql'  # вызов программы со скриптом как параметр для выгрузки
    ], timeout=600)


def compressing(base='UL'):
    """Функция сжатия базы"""
    print_log("Сжатие баз 'ПО Участок инкассации'")

    for bases in glob.glob(TEMP_DIR + '/' + f'POU_{base}_*.bak'):
        print(bases)
        subprocess.run([
            EXE_7Z,
            "a", "-t7z", "-m0=LZMA2:mt=6", "-mx=0", "-ssw",  # параметры для работы 7Zip
            f"POU_{base}_{NOW_DATE_TIME_DIR}.{ARCH_EXT}",  # итоговый файл
            bases,  # файл для архивирования
            "-p" + PASS_7Z
        ], timeout=600)


def moving_files():
    print("Перемещение сжатых баз 'ПО Участок инкассации'")
    for files in glob.glob(TEMP_DIR + '/' + f'*.{ARCH_EXT}'):
        shutil.move(files, BACKUP_DIR)
    cleaning_temp()


if __name__ == 'main':  # старт
    print("Начало работы скрипта по резеврному копированию баз 'ПО Участок инкассации'")
    backuping()
    compressing(base='DM')
    moving_files()
    print("Окончание работы скрипта по резеврному копированию баз 'ПО Участок инкассации'")
