import config
import asyncio
from modules.yandex_api_module import take_orders_combine
from modules.label_tg.take_orders_data import process_orders
from modules.label_tg.work_with_image import create_image_with_text_and_pdf
from modules.telegram_api_module import send_messages_to_users
from modules.label_tg.telegram_api_label_tg_module import send_document_to_telegram
import numpy as np
from PIL import Image


async def main_label_tg():
    global message_telegram
    order_data = take_orders_combine(business_id=config.business_id, start=0, end=0)
    try:
        i = 0
        images = []
        for order in order_data:
            print(order)
            results = process_orders(order)  # results is a tuple of tuples
            for warehouse_id, order_id, message_telegram, text_list in results:  # iterate over each tuple in results
                i += 1
                images.append(await create_image_with_text_and_pdf(campaign_id=warehouse_id, order_id=order_id,
                                                                   api_key=config.yandex_api_token,
                                                                   text_list=text_list))
        print(images)
        images = [img for sublist in images for img in sublist]

        # преобразуем каждое изображение в массив numpy
        np_images = [np.array(img) for img in images]

        # объединяем изображения по вертикали
        combined = np.vstack(np_images)

        # преобразуем обратно в изображение PIL и сохраняем
        images = Image.fromarray(combined)

        if images:
            await send_document_to_telegram(bot_token=config.telegram_api_token,
                                            chat_ids=config.telegram_chat_id_admin_list,
                                            images=images, text=message_telegram)

        await send_messages_to_users({config.telegram_chat_id_admin: f'Pdf из {i} картинок отправлено'})
    except Exception as e:
        await send_messages_to_users({config.telegram_chat_id_admin: f'Pdf не отправлены {e}'})


if __name__ == "__main__":
    asyncio.run(main_label_tg())
