# Модуль работы с логами

# Импорты
import os
import time
from Modules.print_log import *
from datetime import datetime
import scratch

# Переменные
NOW_DATE: str = datetime.now().strftime('%d.%m.%Y')  # Текущая дата в формате 01.01.2021
NOW_TIME: str = datetime.now().strftime('%H-%M')  # Текущее время в формате 15-00
NOW_WEEKDAY: str = datetime.now().strftime('%A')  # Текущий день недели в формате Monday

LOGS_DIR = os.path.join('..', '+LOGS')
LOG_FILE = os.path.join(LOGS_DIR, f'Log_SQL_{NOW_DATE}_{NOW_WEEKDAY}_{NOW_TIME}.txt')


print(__name__)
print(os.path.dirname(os.path.abspath(__file__)))

# Функции
def alignmenting(text, alignment):
    if alignment == 'centered':
        text = f"{text:=^80}\n"
    elif alignment == 'left':
        text = f"{text:=<80}\n"
    elif alignment == 'right':
        text = f"{text:=>80}\n"
    return text


def logging_new() -> None:
    """Функция создания нового лог-файла"""
    with open(LOG_FILE, 'w') as log_file:
        t = "Лог действий модуля резервного копирования SQL-базы 'ПО Участок инкассации'"
        log_file.write(alignmenting(t, alignment='centered'))
        t = f"Запущено в '{scratch.write_count()}-й' раз"
        log_file.write(alignmenting(t, alignment='right'))


def logging(logging_text: str) -> None:
    """Функция логирования действий модулей"""
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(alignmenting(logging_text, alignment='centered'))


logging_new()
logging("test")
# time.sleep(31)
logging("test2")
# time.sleep(31)
logging("test3")
