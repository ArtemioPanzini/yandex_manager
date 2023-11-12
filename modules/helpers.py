import logging
from datetime import date, timedelta
import time
from logs.logging_config import setup_logging  # Импорт функции setup_logging из logging_config.py
setup_logging()
#    logger.debug('Это сообщение уровня DEBUG')
#    logger.info('Это сообщение уровня INFO')
#    logger.warning('Это сообщение уровня WARNING')
#    logger.error('Это сообщение уровня ERROR')
#    logger.critical('Это сообщение уровня CRITICAL')
logger = logging.getLogger('helpers')
logger.info('Начало работы helpers')


def retry(func, max_retries=3):
    if not callable(func):
        logger.error('Аргумент func должен быть вызываемым объектом')

    def wrapper(*args, **kwargs):
        for _ in range(max_retries):
            result = func(*args, **kwargs)
            if result is not None:
                return result
            else:
                logger.error('Попытка не удалась, попробуем еще раз...')
                time.sleep(5)  # Вы можете настроить интервал ожидания по своему усмотрению

        logger.error('Все попытки завершились неудачно')
        return None
    return wrapper


def take_today_plus_arg(delta=1):
    # Получить текущую дату
    today = date.today()

    tomorrow = today + timedelta(days=delta)

    # Преобразовать tomorrow в строку в формате "год-месяц-день"
    formatted_tomorrow = tomorrow.strftime("%d-%m-%Y")
    return formatted_tomorrow


def apply_function_to_list(my_list, func, *args, **kwargs):
    return [func(item, *args, **kwargs) for item in my_list]


def filter_by_count(input_list, count=1) -> list:
    return [item for item in input_list if item.get('count', 0) > count]


def group_by_warehouse(data):
    result = {}
    for item in data:
        warehouse_id = item['warehouse_id']
        if warehouse_id not in result:
            result[warehouse_id] = []
        result[warehouse_id].append(item)
    return result


# Фильтрует большой словарь и получает точную дату {Склад: список артикулов}
def process_data(data) -> dict:
    result_dict = {}

    for entry in data:
        warehouse_key = entry["warehouse_id"]
        offer_id = entry['offer_id']

        if warehouse_key not in result_dict:
            result_dict[warehouse_key] = []

        result_dict[warehouse_key].append(offer_id)
    return result_dict


