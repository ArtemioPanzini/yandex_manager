#!/bin/bash
export PATH=/home/scrapping/yandex_manager/bin:$PATH
export VIRTUAL_ENV=/home/scrapping/yandex_manager
# Путь к активации виртуальной среды
path_to_activate="/home/scrapping/yandex_manager/venv/bin/activate"

# Активировать виртуальную среду
source "$path_to_activate"
echo "all good"
# Путь к вашему основному скрипту
path_to_script="/home/scrapping/yandex_manager/main.py"

# Запустить ваш основной скрипт
python "$path_to_script"
