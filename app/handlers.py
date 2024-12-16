from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
import random
import geopy

from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.states as st
import app.database.requests as db

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать в магазин кроссовок!',
                         reply_markup=kb.main)


@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите категорию товара',
                         reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def catalog_items(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('Товары по выбранной категории',
                                  reply_markup=await kb.category_items(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item_'))
async def item_info(callback: CallbackQuery):
    await callback.answer()
    item = await db.get_item(callback.data.split('_')[1])
    await callback.message.answer(f'{item.name}\n\n{item.description}\n\n{item.price}')

