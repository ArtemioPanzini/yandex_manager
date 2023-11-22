from telegram import Bot, InputFile
from io import BytesIO
from PIL import Image
import io
from telegram import Bot

def combine_images(images):
    widths, heights = zip(*(i.size for i in images))
    total_width = max(widths)
    max_height = sum(heights)
    new_img = Image.new('RGB', (total_width, max_height))

    y_offset = 0
    for img in images:
        new_img.paste(img, (0, y_offset))
        y_offset += img.height

    return new_img


async def send_combined_image_to_telegram(bot_token, chat_ids: list, images, text):
    combined_image = combine_images(images)
    bot = Bot(token=bot_token)
    bio = BytesIO()
    combined_image.save(bio, 'JPEG')
    bio.seek(0)
    for chat_id in chat_ids:
        await bot.send_photo(chat_id=chat_id, photo=InputFile(bio), caption=text)


async def send_document_to_telegram(bot_token, chat_ids: list, images, text):
    bot = Bot(token=bot_token)
    pdf_bytes = io.BytesIO()
    images.save(pdf_bytes, format='PDF')
    pdf_bytes.seek(0)
    for chat_id in chat_ids:
        await bot.send_document(chat_id=chat_id, document=pdf_bytes, filename='combined_image.pdf')
