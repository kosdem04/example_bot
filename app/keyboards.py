from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
# from app.database.requests import get_categories
import app.database.requests as db


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Каталог')],
    [KeyboardButton(text='Корзина')],
], resize_keyboard=True)


async def categories():
    all_categories = await db.get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f'category_{category.id}'))
    return keyboard.adjust(2).as_markup()


async def category_items(category_id):
    all_items = await db.get_items_by_category(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:

        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f'item_{item.id}'))
    return keyboard.adjust(2).as_markup()

sure = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='ok-sure')],
    [InlineKeyboardButton(text='Нет', callback_data='cancel-sure')],
], resize_keyboard=True)


async def admin_categories():
    all_categories = await db.get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f'admin-category_{category.id}'))
    return keyboard.adjust(2).as_markup()