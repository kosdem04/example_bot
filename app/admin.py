from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter, CommandStart, Command
from sqlalchemy.util import await_only
from app.keyboards import categories
from config import ADMINS
import app.states as st
import app.keyboards as kb
import app.database.requests as db
from aiogram.fsm.context import FSMContext

admin = Router()


class Admin(Filter):
    def __init__(self):
        self.admins = ADMINS

    async def __call__(self, message: Message):
        return message.from_user.id in self.admins


@admin.message(Admin(), F.text == 'Отмена', st.AddItem.price)
@admin.message(Admin(), F.text == 'Отмена', st.AddItem.description)
@admin.message(Admin(), F.text == 'Отмена', st.AddItem.name)
@admin.message(Admin(), F.text == 'Отмена', st.AddItem.category)
@admin.message(Admin(), F.text == 'Отмена', st.EditCategory.new_name)
@admin.message(Admin(), F.text == 'Отмена', st.EditCategory.select)
@admin.message(Admin(), F.text == 'Отмена', st.DeleteCategory.select)
@admin.message(Admin(), F.text == 'Отмена', st.AddCategory.name)
@admin.callback_query(Admin(), F.data == 'cancel-sure', st.AddItem.sure)
@admin.callback_query(Admin(), F.data == 'cancel-sure', st.AddCategory.sure)
async def main_menu(callback, state: FSMContext):
    if isinstance(callback, CallbackQuery):
        await callback.answer()
        await callback.message.answer('Главное меню',
                             reply_markup=kb.main)
        await state.clear()
    else:
        await callback.answer('Главное меню',
                             reply_markup=kb.main)
        await state.clear()


'''--------------------------------------- Добавление категории ---------------------------------------------------'''
@admin.message(Admin(), Command('add_category'))
async def add_category_name(message: Message, state: FSMContext):
    await state.set_state(st.AddCategory.name)
    await message.answer('Введите имя новой категории',
                         reply_markup=kb.cancel)


@admin.message(Admin(), st.AddCategory.name)
async def add_category_sure(message: Message, state: FSMContext):
    await state.set_state(st.AddCategory.sure)
    await state.update_data(name=message.text)
    await message.answer(f'Вы действительно хотите создать новую категорию - {message.text}',
                         reply_markup=kb.sure)


@admin.callback_query(Admin(), F.data == 'ok-sure', st.AddCategory.sure,)
async def add_category_sure_ok(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    await db.add_category(data['name'])
    await callback.message.answer('Новая категория добавлена успешно!',
                         reply_markup=kb.main)
    await state.clear()



'''--------------------------------------- Удаление категории ---------------------------------------------------'''
@admin.message(Admin(), Command('delete_category'))
async def delete_category_select(message: Message, state: FSMContext):
    await state.set_state(st.DeleteCategory.select)
    await message.answer('Выберите, какую категорию необходимо удалить',
                         reply_markup=await kb.admin_categories())
    await message.answer('Нажмите на кнопку ниже, чтобы отменить операцию',
                         reply_markup=kb.cancel)


@admin.callback_query(Admin(), F.data.startswith('admin-category_'), st.DeleteCategory.select)
async def delete_category_ok(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await db.delete_category(callback.data.split('_')[1])
    await callback.message.answer('Категория удалена успешно!',
                                  reply_markup=kb.main)
    await state.clear()


'''------------------------------------------Изменение категории-------------------------------------'''
@admin.message(Admin(), Command('edit_category'))
async def edit_category_select(message: Message, state: FSMContext):
    await state.set_state(st.EditCategory.select)
    await message.answer('Выберите, какую категорию необходимо изменить',
                         reply_markup=await kb.admin_categories())
    await message.answer('Нажмите на кнопку ниже, чтобы отменить операцию',
                         reply_markup=kb.cancel)


@admin.callback_query(Admin(), F.data.startswith('admin-category_'), st.EditCategory.select)
async def edit_category_new_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(category=callback.data.split('_')[1])
    await state.set_state(st.EditCategory.new_name)
    await callback.message.answer('Напишите новое название для категории')


@admin.message(Admin(), st.EditCategory.new_name)
async def edit_category_sure(message: Message, state: FSMContext):
    data = await state.get_data()
    await db.edit_category(data['category'], message.text)
    await message.answer(f'Категория успешно изменена',
                         reply_markup=kb.main)
    await state.clear()


'''--------------------------------------- Добавление товара ---------------------------------------------------'''
@admin.message(Admin(), Command('add_item'))
async def add_item_category(message: Message, state: FSMContext):
    await state.set_state(st.AddItem.category)
    await message.answer('Выберите категорию для нового товара',
                         reply_markup=await kb.admin_categories())
    await message.answer('Нажмите на кнопку ниже, чтобы отменить операцию',
                         reply_markup=kb.cancel)


@admin.callback_query(Admin(), F.data.startswith('admin-category_'), st.AddItem.category)
async def add_item_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(category=callback.data.split('_')[1])
    await state.set_state(st.AddItem.name)
    await callback.message.answer('Введите название для нового товара')


@admin.message(Admin(), st.AddItem.name)
async def add_item_description(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(st.AddItem.description)
    await message.answer('Напишите описание для нового товара')


@admin.message(Admin(), st.AddItem.description)
async def add_item_price(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(st.AddItem.price)
    await message.answer('Напишите цену для нового товара в $')


@admin.message(Admin(), st.AddItem.price)
async def add_item_sure(message: Message, state: FSMContext):
    await state.set_state(st.AddItem.sure)
    await state.update_data(price=message.text)
    data = await state.get_data()
    await message.answer(f'Вы действительно хотите создать новый товар со следующими характеристиками\n'
                         f'{data['name']}\n'
                         f'{data['description']}\n'
                         f'{data['price']}\n',
                         reply_markup=kb.sure)


@admin.callback_query(Admin(), F.data == 'ok-sure', st.AddItem.sure)
async def add_item_sure_ok(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    await db.add_item(data['name'], data['description'], data['price'], data['category'])
    await callback.message.answer('Новый товар добавлен успешно!',
                         reply_markup=kb.main)
    await state.clear()


