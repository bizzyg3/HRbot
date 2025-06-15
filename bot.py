import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import Message
from aiogram.dispatcher.filters import CommandStart

# Получаем переменные окружения
API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Словарь: текст -> user_id
user_map = {}

@dp.message_handler(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        "👋 Привет!\n\nПо какому поводу вы пишете?\nПросто напишите сюда, и мы вам ответим как можно скорее."
    )

@dp.message_handler()
async def handle_message(message: types.Message):
    if message.chat.id == ADMIN_ID and message.reply_to_message:
        replied_text = message.reply_to_message.text
        user_id = user_map.get(replied_text)
        if user_id:
            await bot.send_message(user_id, message.text)
        else:
            await message.reply("❌ Не могу найти пользователя.")
    elif message.chat.type == "private":
        # Сохраняем user_id по тексту
        user_map[message.text] = message.chat.id
        forward = (
            f"📨 Сообщение от @{message.from_user.username or 'без username'}:\n\n{message.text}"
        )
        await bot.send_message(ADMIN_ID, forward)