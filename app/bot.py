import os
import asyncio

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers import router

from database.db import init_db


async def start_bot():
    load_dotenv()  # Загружаем .env в начале
    bot_token = os.getenv('BOT_TOKEN')

    if not bot_token:
        raise ValueError("Переменная окружения BOT_TOKEN не найдена!")
    
    await init_db() # Инициализация базы

    bot = Bot(token=bot_token)
    dp = Dispatcher()
    
    dp.include_router(router)
    
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(start_bot())