from aiogram.fsm.state import State, StatesGroup


class AddCategory(StatesGroup):
    name = State()
    sure = State()


class DeleteCategory(StatesGroup):
    select = State()
    sure = State()


class AddItem(StatesGroup):
    category = State()
    name = State()
    description = State()
    price = State()
    sure = State()


class EditCategory(StatesGroup):
    select = State()
    new_name = State()