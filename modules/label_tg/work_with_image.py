from pdf2image import convert_from_bytes
import requests
from PIL import Image, ImageDraw, ImageFont

import config
from modules.label_tg import telegram_api_label_tg_module, yandex_api_label_tg_module


def convert_pdf_to_images(pdf_bytes):
    images = convert_from_bytes(pdf_bytes, fmt='jpeg')
    return images


def create_image_with_text(img, text_list, font_size=25):

    crop_box = (0, 39, img.width, img.height)
    cropped_img = img.crop(crop_box)
    new_height = img.height + 40
    new_img = Image.new("RGB", (img.width, new_height), (255, 255, 255))
    new_img.paste(cropped_img, (0, 0))
    new_img.paste(img.crop((0, 0, img.width, 50)), (0, new_height - 50))

    draw = ImageDraw.Draw(new_img)
    font_path = '/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf'
    font = ImageFont.truetype(font_path, font_size)
    text_color = (0, 0, 0)
    text_positions = [(30, 940), (30, 990), (315, 940), (315, 990)]

    for i, text in enumerate(text_list):
        draw.text(text_positions[i], text, font=font, fill=text_color)

    return new_img


async def create_image_with_text_and_pdf(campaign_id, order_id, api_key, text_list, font_size=25,
                                         bot_token=config.telegram_api_token,
                                         chat_id=None, telegram_text=None):
    images = []
    try:
        pdf_bytes = yandex_api_label_tg_module.get_pdf(campaign_id, order_id, api_key)
        images = convert_pdf_to_images(pdf_bytes)
        for i in range(len(images)):
            img = images[i] if images else Image.new('RGB', (500, 500), 'white')
            new_img = create_image_with_text(img, text_list, font_size)
            images[i] = new_img

        if bot_token and chat_id and telegram_text:
            await telegram_api_label_tg_module.send_combined_image_to_telegram(bot_token, chat_id,
                                                                               images, telegram_text)

    except requests.exceptions.RequestException as e:
        print(f"запрос: {e}")
    return images



