import config
import logging
from telegram import Bot
from logs.logging_config import setup_logging  # Импорт функции setup_logging из logging_config.py
setup_logging()
#    logger.debug('Это сообщение уровня DEBUG')
#    logger.info('Это сообщение уровня INFO')
#    logger.warning('Это сообщение уровня WARNING')
#    logger.error('Это сообщение уровня ERROR')
#    logger.critical('Это сообщение уровня CRITICAL')
logger = logging.getLogger('telegram_api_module')  # Получение логгера для модуля telegram_api_module
logger.info('Начало работы telegram')  # Запись информационного сообщения в лог


# Функция для создания сообщения для Telegram
def create_telegram_messages_from_orders(orders) -> list:
    logger.info('Начало работы функции process_orders_to_tg')
    list_messages = []
    try:
        for order in orders:
            offer_id = order['offerId']
            freeze_count = order['freezeCount']
            available_count = order['availableCount']
            list_messages.append(f"Большой заказ. Артикул: {offer_id} заказано {freeze_count} доступно {available_count}")

    except Exception as e:
        logger.critical('Функция create_telegram_messages_from_orders не сработала')
        logger.error(f'Функция create_telegram_messages_from_orders ошибка {e}')

    logger.debug('Завершение работы функции process_orders_to_tg')
    return list_messages


# Асинхронная функция для отправки сообщений в Telegram
async def send_telegram_messages_async(token=config.telegram_api_token, chat_ids=config.telegram_chat_id_moderator, messages=None):
    try:
        if messages:
            bot = Bot(token=token)
            for chat_id in chat_ids:
                for message in messages:
                    await bot.send_message(chat_id=chat_id, text=message)
            logger.info('Функция send_telegram_messages_async отправили сообщения в телеграмм')
            logger.debug('Функции send_telegram_messages_async завершение работы ')
            return True
        else:
            logger.info('Функция send_telegram_messages_async не отправили сообщения в телеграмм, нечего отправлять')
            logger.debug('Функции send_telegram_messages_async завершение работы ')
            return False

    except Exception as e:
        logger.error(f'Функция send_telegram_messages_async ошибка {e}')
        return None
