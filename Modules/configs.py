# Модуль для работы с файлами настроек

# Импорты
from Modules.where_i import *
import configparser
import subprocess
import shutil
import sys
import os

# Переменные
SETTINGS_DIR = os.path.join('..', 'Configs')  # путь до каталога с SQL скриптами
settings = os.path.join(SETTINGS_DIR, 'settings.ini')
settings_template = os.path.join(SETTINGS_DIR, 'settings_template.ini')
security = os.path.join(SETTINGS_DIR, 'security.ini')
security_template = os.path.join(SETTINGS_DIR, 'security_template.ini')

# Проверка существования файлов с настройками, копирование шаблонов
if os.path.isfile(settings) is not True:
    if os.path.isfile(settings_template):
        shutil.copy(settings_template, settings)
    else:
        sys.exit("Ошибка - нет файла с настройками")

if os.path.isfile(security) is not True:
    if os.path.isfile(security_template):
        shutil.copy(security_template, security)
        subprocess.run(['notepad', security])  # запук блокнота для ввода пароля
    else:
        sys.exit("Ошибка - нет файла с настройками безопасности")


# Чтение конфигов
cfg = configparser.ConfigParser()
cfg.read(settings)  # чтение конфига с настройками путей
ULYANOVSK = cfg.get('NAMES', 'ulyanovsk')  # имя на сервере 1С-V8
DIMITROVGRAD = cfg.get('NAMES', 'dimitrovgrad')  # имя у Боровикова
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

# Работа с безопасностью
cfg_security = configparser.ConfigParser()
cfg_security.read(security)  # чтение конфига с настройками безопасности
PASS_7Z = cfg_security.get('SECURITY', 'pass_7z')  # пароль для архива
