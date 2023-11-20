import requests
import json
import config
import logging
import itertools
from modules.helpers import apply_function_to_list, group_offers_by_warehouse
from retry import retry
from modules.helpers import take_today_plus_arg
from logs.logging_config import setup_logging
setup_logging()
#    logger.debug('Это сообщение уровня DEBUG')
#    logger.info('Это сообщение уровня INFO')
#    logger.warning('Это сообщение уровня WARNING')
#    logger.error('Это сообщение уровня ERROR')
#    logger.critical('Это сообщение уровня CRITICAL')

logger = logging.getLogger('yandex_api_module')
logger.info('Начало работы yandex api module')


# Функция для получения списка заказов для данного бизнес-идентификатора за определенные даты
def take_orders(business_id, start=1, end=30) -> list:
    logger.info('Начало работы функции take_orders')
    try:
        warehouse_list = get_warehouses(business_id)
        response = apply_function_to_list(warehouse_list, get_orders_response, start, end)
        orders = apply_function_to_list(response, get_orders_json)
        orders = list(itertools.chain.from_iterable(orders))
        logger.debug('Завершение работы функции get_orders_response')
        return orders
    except Exception as e:
        logger.critical('Функция take_orders не сработала')
        logger.error(f'Функция take_orders ошибка {e}')
        return []


def take_orders_combine(business_id, start=1, end=30) -> list:
    logger.info('Начало работы функции take_orders')
    try:
        warehouse_list = get_warehouses(business_id)
        response = apply_function_to_list(warehouse_list, get_orders_response, start, end)
        orders = apply_function_to_list(response, get_orders_json_combine)
        orders = [item for item in orders if item]
        logger.debug('Завершение работы функции get_orders_response')
        return orders
    except Exception as e:
        logger.critical('Функция take_orders не сработала')
        logger.error(f'Функция take_orders ошибка {e}')
        return []


# Функция для получения ответа от API складов
@retry(exceptions=requests.exceptions.RequestException, tries=3, delay=2, backoff=2, max_delay=10)
def get_warehouses_response(business_id) -> json:
    logger.info('Начало работы функции get_warehouses_response')
    url = f'https://api.partner.market.yandex.ru/businesses/{business_id}/warehouses'
    try:
        response = requests.get(url, headers=config.headers, timeout=10)
        if response.status_code == 200:
            logger.info('Функция get_warehouses_response успешно получили список складов')
            logger.debug('Завершение работы функции get_warehouses_list')
            return response.json()
        else:
            logger.error(f'Функция get_warehouses_response: Не смогли получить список складов {response.status_code}')
            logger.debug('Завершение работы функции get_warehouses_list')
            return None
    except Exception as e:
        logger.critical('Функция get_warehouses_response не сработала')
        logger.error(f'Функция get_warehouses_response ошибка {e}')
        return None


# Функция для получения списка идентификаторов кампаний из ответа API
def get_warehouses_list(response) -> list:
    logger.info('Начало работы функции get_warehouses_list')

    try:
        campaign_ids = []
        campaign_ids = [warehouse['campaignId'] for warehouse in response['result']['warehouses']]
        logger.debug('Завершение работы функции get_warehouses_list')
        return campaign_ids

    except Exception as e:
        logger.critical('Функция get_warehouses_list не сработала')
        logger.error(f'Функция get_warehouses_list ошибка {e}')
        return []


# Функция для получения списка идентификаторов кампаний для данного бизнес-идентификатора
def get_warehouses(business_id) -> list:
    logger.info('Начало работы функции get_warehouses')

    try:
        list_warehouses = []
        warehouses_response = get_warehouses_response(business_id)
        list_warehouses = get_warehouses_list(warehouses_response)
        logger.debug('Завершение работы функции get_warehouses')
        return list_warehouses

    except Exception as e:
        logger.critical('Функция get_warehouses не сработала')
        logger.error(f'Функция get_warehouses ошибка {e}')
        return []


# Функция для получения ответа от API заказов
@retry(exceptions=requests.exceptions.RequestException, tries=3, delay=2, backoff=2, max_delay=10)
def get_orders_response(campaign_id, start=1, end=30) -> tuple:
    logger.info('Начало работы функции get_orders_response')

    url = f'https://api.partner.market.yandex.ru/campaigns/{campaign_id}/orders'
    params = {
        "status": "PROCESSING",
        "supplierShipmentDateFrom": f"{take_today_plus_arg(start)}",
        "supplierShipmentDateTo": f"{take_today_plus_arg(end)}",
    }

    try:
        response = requests.get(url, params=params, headers=config.headers, timeout=10)

        if response.status_code == 200:
            logger.info(f'Успешно получили список заказов из склада {campaign_id}')
            logger.debug('Завершение работы функции get_orders_response')
            return response.json(), campaign_id
        else:
            logger.error(f'Функция get_orders_response не получили список ордеров {campaign_id} {response.status_code}')
            logger.debug('Завершение работы функции get_orders_response')
            return None, campaign_id

    except Exception as e:
        logger.critical('Функция get_orders_response не сработала')
        logger.error(f'Функция get_orders_response ошибка {e}')
        return ()


# Функция для преобразования ответа API в список словарей
def get_orders_json(data) -> list:
    logger.info('Начало работы функции get_orders_json')

    try:
        order, warehouse_id = data
        orders = order.get("orders", [])
        result = []
        for order in orders:
            order_id = order.get("id")
            items = order.get("items", [])
            for item in items:
                offer_id = item.get("offerId")
                count = item.get("count")
                result.append({"warehouse_id": warehouse_id, "order_id": order_id, "offer_id": offer_id, "count": count})
        logger.debug('Завершение работы функции get_orders_json')
        return result

    except Exception as e:
        logger.critical('Функция get_orders_json не сработала')
        logger.error(f'Функция get_orders_json ошибка {e}')
        return []


def get_orders_json_combine(data) -> dict:
    logger.info('Начало работы функции get_orders_json')

    try:
        order, warehouse_id = data
        orders = order.get("orders", [])
        result = {}

        for order in orders:
            order_id = order.get("id")
            items = order.get("items", [])

            # Initialize the result dictionary for the warehouse and order if not present
            if warehouse_id not in result:
                result[warehouse_id] = {}

            if order_id not in result[warehouse_id]:
                result[warehouse_id][order_id] = {"items": []}

            # Append items to the items list
            for item in items:
                offer_id = item.get("offerId")
                count = item.get("count")
                result[warehouse_id][order_id]["items"].append({"offer_id": offer_id, "count": count})

        logger.debug('Завершение работы функции get_orders_json')
        return result

    except Exception as e:
        logger.critical('Функция get_orders_json не сработала')
        logger.error(f'Функция get_orders_json ошибка {e}')
        return {}


# Функция для отправки запроса на обновление запасов
def send_request(campaign_id, offer_ids) -> dict:
    logger.info('Начало работы функции send_request')
    url = f'https://api.partner.market.yandex.ru/campaigns/{campaign_id}/offers/stocks'
    payload = {
        "offerIds": offer_ids
    }
    result = {}

    try:
        response = requests.post(url, json=payload, headers=config.headers)

        # Обработка ответа
        if response.status_code == 200:
            logger.debug(f'Функция get_orders_response запрос успешно выполнен для кампании {campaign_id}')
            result['response'] = response.json()  # Вывести ответ API
            return result

        else:
            logger.error(f'Функция send_request для кампании {campaign_id} ошибка {response.text}')
            logger.debug('Завершение работы функции get_orders_response')
            return {}

    except Exception as e:
        logger.critical('Функция send_request не сработала')
        logger.error(f'Функция send_request ошибка {e}')


# Функция для выполнения запросов для каждой кампании
def execute_campaign_requests(data_dict) -> list:
    logger.info('Начало работы функции execute_campaign_requests')
    results = []
    try:
        for campaign_id, offer_ids in data_dict.items():
            result = send_request(campaign_id, offer_ids)
            results.append(result)
        logger.debug('Завершение работы функции get_orders_response')
        return results

    except Exception as e:
        logger.critical('Функция execute_campaign_requests не сработала')
        logger.error(f'Функция process_stocks ошибка {e}')
        return []


# Функция для обработки ответов на запросы обновления запасов
def process_stocks(response_list) -> list:
    logger.info('Начало работы функции process_stocks')
    result_list = []

    try:
        for response_entry in response_list:
            campaign_id = response_entry.get('response', {}).get('result', {}).get('warehouses', [{}])[0].get('warehouseId')

            for warehouse in response_entry.get('response', {}).get('result', {}).get('warehouses', []):
                for offer in warehouse.get('offers', []):
                    available_count = next((s['count'] for s in offer['stocks'] if s['type'] == 'AVAILABLE'), 0)
                    freeze_count = next((s['count'] for s in offer['stocks'] if s['type'] == 'FREEZE'), 0)

                    if available_count < (2 * freeze_count):
                        result_list.append({
                            'campaignId': campaign_id,
                            'offerId': offer['offerId'],
                            'warehouseId': warehouse['warehouseId'],
                            'availableCount': available_count,
                            'freezeCount': freeze_count
                        })
        logger.debug('Завершение работы функции process_stocks')
        return result_list

    except Exception as e:
        logger.critical('Функция process_stocks не сработала')
        logger.error(f'Функция process_stocks ошибка {e}')
        return []


# Извлекаем информацию о запасах из заказов
def retrieve_stock_info_from_orders(filtered_orders) -> list:
    logger.info('Начало работы функции retrieve_stock_info_from_orders')
    try:
        processed_data_stocks = group_offers_by_warehouse(filtered_orders)
        execute_data = execute_campaign_requests(processed_data_stocks)
        logger.debug('Завершение работы функции retrieve_stock_info_from_orders')
        return execute_data

    except Exception as e:
        logger.critical('Функция retrieve_stock_info_from_orders не сработала')
        logger.error(f'Функция retrieve_stock_info_from_orders ошибка {e}')
        return []
