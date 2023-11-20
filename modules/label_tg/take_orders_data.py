from modules.yandex_api_module import take_orders, take_orders_combine
import config

data = take_orders_combine(business_id=config.business_id, start=1, end=1)


def process_orders(data_):
    results = []  # Create a list to store results for each order

    for warehouse_id, order in data_.items():
        for order_id, order_details in order.items():
            items = order_details.get("items", [])
            message_telegram, text_list = make_telegram_message(order_id, items)

            # Store results in a tuple and append it to the results list
            result_tuple = (warehouse_id, order_id, message_telegram, text_list)
            results.append(result_tuple)

    return tuple(results)


# Example process function
def make_telegram_message(order_id, items):
    message_telegram = ""
    text_list = []
    for item in items:
        offer_id = item['offer_id']
        count = item['count']
        message_telegram += f"{order_id}: {offer_id} - {count}шт\n"

        text_list.append(f'{offer_id} - {count}шт')
    return message_telegram, text_list
