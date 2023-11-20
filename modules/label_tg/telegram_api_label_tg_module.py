from telegram import Bot, InputFile
from io import BytesIO
import config


# Принимаем картинку base64, отправляем вместе с комментом
# Баг: отправится только для первого чата
async def send_image_to_telegram(bot_token, chat_ids: list, img, text):
    bot = Bot(token=bot_token)
    bio = BytesIO()
    img.save(bio, 'JPEG')
    bio.seek(0)
    for chat_id in chat_ids:
        await bot.send_photo(chat_id=chat_id, photo=InputFile(bio), caption=text)


async def send_messages_to_users(message_dict):
    bot = Bot(token=config.telegram_api_token)
    for user_id, message in message_dict.items():
        try:
            await bot.send_message(chat_id=user_id, text=message)
            print(f"Сообщение отправлено пользователю с ID {user_id}")
        except Exception as e:
            print(f"Ошибка при отправке сообщения пользователю с ID {user_id}: {e}")
