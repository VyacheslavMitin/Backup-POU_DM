# Модуль резервного копирования в ПО 'Участок инкассации' в Димитровграде
# Python 3.8
__author__ = 'Vyacheslav Mitin <vyacheslav.mitin@gmail.com>'
__version__ = '1 - разработка'

# Импорты
import shutil
import glob
# Импорт моих модулей
from ROI_base import *  # мой модуль для вывода времени
import ROI_common  # мой модуль для создания папок, определения дат, запуска проводника

NOW_DATE_TIME_DIR = datetime.now().strftime('%d.%m.%Y')  # Текущая дата для работы с файлами и каталогами

cfg = configparser.ConfigParser()
cfg.read('settings.ini')  # чтение локального конфига
TIMEOUT = float(cfg.get('SETTINGS', 'timeout'))
DIR_REPORTS = cfg.get('SETTINGS', 'dir_reports')


# Функции
def start():
