# Модуль для работы с файлами настроек

# Импорты
import configparser
import subprocess
import shutil
import sys
import os

# Переменные
if __name__ == '__main__':
    SETTINGS_DIR: str = os.path.join('..', 'Configs')  # путь до каталога с SQL скриптами
else:
    SETTINGS_DIR: str = os.path.join('Configs')  # путь до каталога с SQL скриптами если запускается основной модуль

settings: str = os.path.join(SETTINGS_DIR, 'settings.ini')
settings_template: str = os.path.join(SETTINGS_DIR, 'settings_template.ini')
security: str = os.path.join(SETTINGS_DIR, 'security.ini')
security_template: str = os.path.join(SETTINGS_DIR, 'security_template.ini')
subdivisions: str = os.path.join(SETTINGS_DIR, 'subdivisions.ini')
subdivisions_template: str = os.path.join(SETTINGS_DIR, 'subdivisions_template.ini')


# Функции
def checking_configs(*args: tuple) -> None:
    """Функция проверки существования файлов с настройками, копирование шаблонов, если необходимо"""
    if len(*args) != 2:
        sys.exit(f"Ошибка: кол-во аргументов функции 'checking_configs()' не равно '2'")
    for ini_file, ini_template_file in args:
        if os.path.isfile(ini_file) is not True:  # проверка существования основного файла настроек
            if os.path.isfile(ini_template_file):  # проверка существования шаблона
                shutil.copy(ini_template_file, ini_file)  # копирование шаблона
                if sys.platform == 'win32':  # проверка ОС Windows
                    subprocess.run(['notepad.exe', ini_file])  # запуск блокнота для редактирования файла
                elif sys.platform == 'darwin':  # проверка ОС Mac OS
                    pass
            else:
                sys.exit(f"Ошибка: нет файла с настройками '{ini_file}'")


checking_configs((subdivisions, subdivisions_template))  # проверка файла с настройками подразделений
checking_configs((settings, settings_template))  # проверка файла с настройками
checking_configs((security, security_template))  # проверка файла с настройками безопасности

# Чтение конфига с подразделениями
cfg_subdivisions = configparser.ConfigParser()
cfg_subdivisions.read(subdivisions)  # чтение конфига с настройками путей
ULYANOVSK = cfg_subdivisions.get('NAMES', 'ulyanovsk')  # имя на сервере 1С-V8
DIMITROVGRAD = cfg_subdivisions.get('NAMES', 'dimitrovgrad')  # имя у Боровикова
# Проверка подразделения
if os.getlogin() == ULYANOVSK:
    CITY = 'ulyanovsk'
elif os.getlogin() == DIMITROVGRAD:
    CITY = 'dimitrovgrad'
else:  # выход с ошибкой если не то имя логина в систему
    sys.exit("Ошибка: не подходящий логин в систему!")

# Чтение конфига с путями
cfg = configparser.ConfigParser()
cfg.read(settings)  # чтение конфига с настройками путей
TEMP_DIR = cfg.get('PATHS', 'temp_dir')  # временная папка
LOGS_DIR = cfg.get('PATHS', 'logs_dir')  # каталог для логов
EXE_7Z = cfg.get('PATHS', '7zip')  # путь до архиватора
SQL_SCRIPTS_DIR = cfg.get('PATHS', 'sql_scripts_dir')  # путь до каталога с SQL скриптами
# ветвление по подразделениям
if CITY == 'ulyanovsk':
    BACKUP_DIR_NAS = cfg.get('PATHS', 'backup_dir_ul_nas')  # путь до каталога с бекапами на NAS
    BACKUP_DIR_CLOUD = cfg.get('PATHS', 'backup_dir_ul_yandex')  # путь до каталога с бекапами на облаке
    SQL_SCRIPT = os.path.join(SQL_SCRIPTS_DIR, cfg.get('NAMES', 'sql_script_ul'))  # путь до скрипта SQL
elif CITY == 'dimitrovgrad':
    BACKUP_DIR_CLOUD = cfg.get('PATHS', 'backup_dir_dm_yandex')  # путь до каталога
    SQL_SCRIPT = os.path.join(SQL_SCRIPTS_DIR, cfg.get('NAMES', 'sql_script_dm'))  # путь до скрипта SQL

# Чтение конфига с безопасностью
cfg_security = configparser.ConfigParser()
cfg_security.read(security)  # чтение конфига с настройками безопасности
PASS_7Z = cfg_security.get('SECURITY', 'pass_7z')  # пароль для архива
