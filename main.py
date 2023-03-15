import asyncio
import logging
import os

from aiogram import Bot, Dispatcher

from handlers import settings, common, create_images

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=os.environ['telegram_chatgpt_bot_token'])
    dp = Dispatcher()
    dp.include_router(settings.router)
    dp.include_router(common.router)
    dp.include_router(create_images.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
