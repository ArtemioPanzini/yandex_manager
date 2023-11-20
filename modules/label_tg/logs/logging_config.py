import logging


def setup_logging():
    # Настройка логгера для main.py
    main_logger = logging.getLogger('main')
    main_logger.setLevel(logging.DEBUG)
    main_handler = logging.FileHandler('logs/main/main.log')
    main_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    main_logger.addHandler(main_handler)

    # Настройка логгера для yandex_api_module.py
    yandex_logger = logging.getLogger('yandex_api_module')
    yandex_logger.setLevel(logging.DEBUG)
    yandex_handler = logging.FileHandler('logs/yandex_api_module/yandex_api_module.log')
    yandex_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    yandex_logger.addHandler(yandex_handler)

    # Настройка логгера для telegram_api_module.py
    telegram_logger = logging.getLogger('telegram_api_module')
    telegram_logger.setLevel(logging.DEBUG)
    telegram_handler = logging.FileHandler('logs/telegram_api_module/telegram_api_module.log')
    telegram_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    telegram_logger.addHandler(telegram_handler)

    # Настройка логгера для helpers.py
    telegram_logger = logging.getLogger('helpers')
    telegram_logger.setLevel(logging.DEBUG)
    telegram_handler = logging.FileHandler('logs/helpers/helpers.log')
    telegram_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    telegram_logger.addHandler(telegram_handler)


if __name__ == "__main__":
    setup_logging()
