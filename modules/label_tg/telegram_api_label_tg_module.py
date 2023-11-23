from telegram import Bot, InputFile
from io import BytesIO
from telegram import Bot
from PyPDF2 import PdfMerger
from PIL import Image
import io


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
    width, height = images.size
    page_height = 1029
    num_pages = -(-height // page_height)  # Ceiling division to get the total number of pages

    pdf_merger = PdfMerger()

    for i in range(num_pages):
        start = i * page_height
        end = min((i + 1) * page_height, height)
        cropped_image = images.crop((0, start, width, end))

        pdf_bytes = io.BytesIO()
        cropped_image.save(pdf_bytes, format='PDF', quality=100)
        pdf_bytes.seek(0)

        pdf_merger.append(pdf_bytes)

    merged_pdf_bytes = io.BytesIO()
    pdf_merger.write(merged_pdf_bytes)
    merged_pdf_bytes.seek(0)

    for chat_id in chat_ids:
        await bot.send_document(chat_id=chat_id, document=merged_pdf_bytes, filename='НаклейкиДляОтгрузки.pdf')
