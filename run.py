import asyncio, logging
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.admin import admin
from config import TG_TOKEN
from app.database.models import async_main
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.scheduler import items_in_categories
import datetime

async def main():
    await async_main()
    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher()
    dp.include_routers(router, admin)

    """

   Создаём ежедневно повторяющиеся действия
   ----------------------------------------------------------------------------------------------
   """

    # создаём объект расписания с установкой часового пояса (scheduler)
    #scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler = AsyncIOScheduler(timezone="Asia/Novosibirsk")

    # варианты добавления задач, которые сработают через минуту и 2 минуты соответсвенно

    scheduler.add_job(items_in_categories, trigger='cron',
                     hour=datetime.datetime.now().hour, minute=datetime.datetime.now().minute+1,
                     start_date=datetime.datetime.now(), kwargs={'bot': bot})
    # scheduler.add_job(check_subscription_end_date, trigger='cron', hour=16, minute=37, kwargs={'bot': bot})
    scheduler.start()  # запускаем планировщик

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # Логгирование
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
