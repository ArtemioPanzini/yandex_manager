import requests
import json
import config
import logging
import itertools
from modules.helpers import apply_function_to_list, group_by_warehouse, process_data
from retry import retry
from modules.helpers import take_today_plus_arg
from logs.logging_config import setup_logging  # Импорт функции setup_logging из logging_config.py

setup_logging()
#    logger.debug('Это сообщение уровня DEBUG')
#    logger.info('Это сообщение уровня INFO')
#    logger.warning('Это сообщение уровня WARNING')
#    logger.error('Это сообщение уровня ERROR')
#    logger.critical('Это сообщение уровня CRITICAL')
logger = logging.getLogger('yandex_api_module')
logger.info('Начало работы yandex api module')


@retry(exceptions=requests.exceptions.RequestException, tries=3, delay=2, backoff=2, max_delay=10)
def get_warehouses_response(business_id) -> json:
    url = f'https://api.partner.market.yandex.ru/businesses/{business_id}/warehouses'

    response = requests.get(url, headers=config.headers, timeout=10)
    if response.status_code == 200:
        logger.info('Успешно получили список складов')
        return response.json()
    else:
        logger.error(f'Не смогли получить список складов {response.status_code}')
        return None


def get_warehouses_list(response) -> list:
    campaign_ids = [warehouse['campaignId'] for warehouse in response['result']['warehouses']]
    return campaign_ids


def get_warehouses(business_id) -> list:
    warehouses_response = get_warehouses_response(business_id)
    list_warehouses = get_warehouses_list(warehouses_response)
    return list_warehouses


@retry(exceptions=requests.exceptions.RequestException, tries=3, delay=2, backoff=2, max_delay=10)
def get_orders_response(campaign_id, start=1, end=30) -> tuple:
    url = f'https://api.partner.market.yandex.ru/campaigns/{campaign_id}/orders'

    params = {
        "status": "PROCESSING",
        "supplierShipmentDateFrom": f"{take_today_plus_arg(start)}",
        "supplierShipmentDateTo": f"{take_today_plus_arg(end)}",

    }

    response = requests.get(url, params=params, headers=config.headers, timeout=10)

    if response.status_code == 200:
        logger.info(f'Успешно получили список заказов из склада {campaign_id}')
        return response.json(), campaign_id
    else:
        logger.error(f'Не смогли получить список ордеров {campaign_id} {response.status_code}')
        return None, campaign_id


def get_orders_json(data) -> list:
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
    return result


def take_orders(business_id, start=1, end=30) -> list:
    warehouse_list = get_warehouses(business_id)
    response = apply_function_to_list(warehouse_list, get_orders_response, start, end)
    orders = apply_function_to_list(response, get_orders_json)
    orders = list(itertools.chain.from_iterable(orders))
    return orders


def send_request(campaign_id, offer_ids):
    url = f'https://api.partner.market.yandex.ru/campaigns/{campaign_id}/offers/stocks'
    payload = {
        "offerIds": offer_ids
    }
    result = {}

    try:
        response = requests.post(url, json=payload, headers=config.headers)

        # Обработка ответа
        if response.status_code == 200:
            result['status'] = 'success'
            result['message'] = f"Запрос успешно выполнен для кампании {campaign_id}"
            result['response'] = response.json()  # Вывести ответ API
        else:
            result['status'] = 'error'
            result['message'] = f"Ошибка при выполнении запроса для кампании {campaign_id}"
            result['response'] = response.text  # Вывести текст ошибки
    except Exception as e:
        result['status'] = 'exception'
        result['message'] = f"Произошла ошибка: {str(e)}"
    return result


def take_request(data_dict):
    results = []
    for campaign_id, offer_ids in data_dict.items():
        result = send_request(campaign_id, offer_ids)
        results.append(result)
    return results


def process_stocks(response_list):
    result_list = []

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

    return result_list


def take_stocks_info(filtered_orders):
    processed_data_stocks = process_data(filtered_orders)
    take_request1 = take_request(processed_data_stocks)
    return take_request1