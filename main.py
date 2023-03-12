import asyncio
import logging
import os

from aiogram import Bot, Dispatcher

from handlers import settings, common

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=os.environ['bot_token'])
    dp = Dispatcher()
    dp.include_router(settings.router)
    dp.include_router(common.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
