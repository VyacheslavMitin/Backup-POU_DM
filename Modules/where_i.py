# Модуль определения местоположения

# Импорты
import os
import sys
import Modules.configs

ULYANOVSK = 'Администратор'
DIMITROVGRAD = 'user'


# Проверка подразделения
if os.getlogin() == ULYANOVSK:
    CITY = 'ulyanovsk'
elif os.getlogin() == DIMITROVGRAD:
    CITY = 'dimitrovgrad'
else:  # выход с ошибкой если не то имя логина в систему
    sys.exit("Не подходящий логин в систему!")
