import logging
import config
import asyncio
from modules.yandex_api_module import take_orders, process_stocks, retrieve_stock_info_from_orders
from modules.helpers import filter_by_count
from tests import test_config_data
from logs.logging_config import setup_logging  # Импорт функции setup_logging из logging_config.py
from modules.telegram_api_module import create_telegram_messages_from_orders, send_telegram_messages_async
setup_logging()
#    logger.debug('Это сообщение уровня DEBUG')
#    logger.info('Это сообщение уровня INFO')
#    logger.warning('Это сообщение уровня WARNING')
#    logger.error('Это сообщение уровня ERROR')
#    logger.critical('Это сообщение уровня CRITICAL')

logger = logging.getLogger('main')
logger.info('Начало работы main')


def main():
    logger.info('Начало работы функции main')
    try:
        # Получаем с Яндекса список словарей с заказами
        orders = take_orders(config.business_id)

        # Фильтруем, если надо по минимальному количеству в заказе
        filtered_orders = (filter_by_count(orders, 0))

        # Получаем остатки с яндекса
        data_stocks = retrieve_stock_info_from_orders(filtered_orders)

        # Обрабатываем дату заказов
        processed_stock_data = process_stocks(data_stocks)  # test_config_data.response_data / data_stocks

        # Получаем сообщение для отсылки
        messages_big_orders = create_telegram_messages_from_orders(processed_stock_data)

        # Отсылаем сообщение
        asyncio.run(send_telegram_messages_async(messages=messages_big_orders))
        logger.debug('Завершение работы функции main')
        print("success")

    except Exception as e:
        logger.critical('Функция main не сработала')
        logger.error(f'Функция main ошибка {e}')
        print(e)
        return None


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
