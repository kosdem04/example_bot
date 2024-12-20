from cgitb import reset

from app.database.models import async_session
from aiogram import Bot
import app.database.requests as db
from config import ADMINS
import datetime

# Ищем всех пользователей, у номеров которых заканчивается срок аренды и уведомляем их
async def items_in_categories(bot: Bot):
    async with async_session() as session:
        categories = await db.get_categories()
        data = {}
        for category in categories:
            items = await db.get_items_by_category(category.id)
            data.update({category.name: sum(1 for item in items)})
        result = ''
        for category, items in data.items():
            result = result + f'{category} - {items} товаров\n'
        # отправляем всем администраторам отчёт о выполненной работе
        for admin in ADMINS:
            await bot.send_message(admin, result)
