import requests
import json
import config
import logging
import asyncio
from telegram import Bot
from logs.logging_config import setup_logging  # Импорт функции setup_logging из logging_config.py
setup_logging()
#    logger.debug('Это сообщение уровня DEBUG')
#    logger.info('Это сообщение уровня INFO')
#    logger.warning('Это сообщение уровня WARNING')
#    logger.error('Это сообщение уровня ERROR')
#    logger.critical('Это сообщение уровня CRITICAL')
logger = logging.getLogger('telegram_api_module')


def process_orders_from_tg(orders):
    list_messages = []
    for order in orders:
        offer_id = order['offerId']
        freeze_count = order['freezeCount']
        available_count = order['availableCount']
        list_messages.append(f"Большой заказ. Артикул: {offer_id} заказано {freeze_count} доступно {available_count}")
    return list_messages


# Логи + док
async def send_messages(token=config.telegram_api_token, chat_ids=config.telegram_chat_id_moderator, messages=None):
    if messages:
        bot = Bot(token=token)
        for chat_id in chat_ids:
            for message in messages:
                await bot.send_message(chat_id=chat_id, text=message)
        return
    else:
        return
