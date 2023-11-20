import config
import asyncio
from modules.yandex_api_module import take_orders_combine
from take_orders_data import process_orders
from work_with_image import create_image_with_text_and_pdf
from modules.telegram_api_module import send_messages_to_users


async def main_label_tg():
    order_data = take_orders_combine(business_id=config.business_id, start=0, end=0)
    try:
        i = 0
        for order in order_data:
            print(order)
            results = process_orders(order)  # results is a tuple of tuples
            for warehouse_id, order_id, message_telegram, text_list in results:  # iterate over each tuple in results
                i += 1
                await create_image_with_text_and_pdf(campaign_id=warehouse_id, order_id=order_id,
                                                     api_key=config.yandex_api_token, text_list=text_list,
                                                     chat_id=config.telegram_chat_id_client,
                                                     telegram_text=message_telegram)

        await send_messages_to_users({config.telegram_chat_id_admin: f'{i} Картинок отправлено'})
    except Exception as e:
        await send_messages_to_users({config.telegram_chat_id_admin: f'Label не отправлены {e}'})

if __name__ == "__main__":
    asyncio.run(main_label_tg())
