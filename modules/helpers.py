import logging
from datetime import date, timedelta
from logs.logging_config import setup_logging  # Импорт функции setup_logging из logging_config.py
setup_logging()
#    logger.debug('Это сообщение уровня DEBUG')
#    logger.info('Это сообщение уровня INFO')
#    logger.warning('Это сообщение уровня WARNING')
#    logger.error('Это сообщение уровня ERROR')
#    logger.critical('Это сообщение уровня CRITICAL')


logger = logging.getLogger('helpers')
logger.info('Начало работы helpers')  # Запись информационного сообщения в лог


# Функция для получения даты через заданное количество дней, изначально берёт разницу 1 день (завтра)
def take_today_plus_arg(delta=1):
    logger.info('Начало работы функции take_today_plus_arg')
    try:
        # Получить текущую дату
        today = date.today()

        tomorrow = today + timedelta(days=delta)

        # Преобразовать tomorrow в строку в формате "год-месяц-день"
        formatted_tomorrow = tomorrow.strftime("%d-%m-%Y")
        logger.debug('Завершение работы функции take_today_plus_arg')
        return formatted_tomorrow

    except Exception as e:
        logger.critical('Функция take_today_plus_arg не сработала')
        logger.error(f'Функция take_today_plus_arg ошибка {e}')
        return None


# Функция для применения заданной функции к каждому элементу списка
def apply_function_to_list(my_list, func, *args, **kwargs) -> list:
    logger.info('Начало работы функции apply_function_to_list')
    try:
        result = []
        result = [func(item, *args, **kwargs) for item in my_list]
        logger.debug('Завершение работы функции apply_function_to_list')
        return result

    except Exception as e:
        logger.critical('Функция apply_function_to_list не сработала')
        logger.error(f'Функция apply_function_to_list ошибка {e}')
        return []


# Функция для фильтрации списка по количеству
def filter_by_count(input_list, count=1) -> list:
    logger.info('Начало работы функции filter_by_count')
    try:
        result = []
        result = [item for item in input_list if item.get('count', 0) > count]
        logger.debug('Завершение работы функции apply_function_to_list')
        return result

    except Exception as e:
        logger.critical('Функция filter_by_count не сработала')
        logger.error(f'Функция filter_by_count ошибка {e}')
        return []


# Функция для группировки данных по складу
def group_by_warehouse(data) -> dict:
    logger.info('Начало работы функции group_by_warehouse')

    try:
        result = {}
        for item in data:
            warehouse_id = item['warehouse_id']
            if warehouse_id not in result:
                result[warehouse_id] = []
            result[warehouse_id].append(item)
        logger.debug('Завершение работы функции group_by_warehouse')
        return result

    except Exception as e:
        logger.critical('Функция group_by_warehouse не сработала')
        logger.error(f'Функция group_by_warehouse ошибка {e}')
        return {}


# Функция для обработки данных и получения словаря {Склад: список артикулов}
def group_offers_by_warehouse(data) -> dict:
    logger.info('Начало работы функции group_offers_by_warehouse')

    try:
        result_dict = {}
        for entry in data:
            warehouse_key = entry["warehouse_id"]
            offer_id = entry['offer_id']

            if warehouse_key not in result_dict:
                result_dict[warehouse_key] = []

            result_dict[warehouse_key].append(offer_id)
        logger.debug('Завершение работы функции group_offers_by_warehouse')
        return result_dict

    except Exception as e:
        logger.critical('Функция group_offers_by_warehouse не сработала')
        logger.error(f'Функция group_offers_by_warehouse ошибка {e}')
        return {}
