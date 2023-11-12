import logging
import time
from logs.logging_config import setup_logging  # Импорт функции setup_logging из logging_config.py
setup_logging()
#    logger.debug('Это сообщение уровня DEBUG')
#    logger.info('Это сообщение уровня INFO')
#    logger.warning('Это сообщение уровня WARNING')
#    logger.error('Это сообщение уровня ERROR')
#    logger.critical('Это сообщение уровня CRITICAL')

logger = logging.getLogger('helpers')
logger.info('Начало работы helpers')  # Запись информационного сообщения в лог


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
