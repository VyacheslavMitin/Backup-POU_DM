import time


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
