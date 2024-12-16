import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.admin import admin
from config import TG_TOKEN
from app.database.models import async_main

async def main():
    await async_main()
    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher()
    dp.include_routers(router, admin)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
