from tkinter.font import names

from app.database.models import async_session
from app.database.models import User, Category, Item, Basket
from sqlalchemy import select, update, delete




async def get_categories():
    async with async_session() as session:
       return await session.scalars(select(Category))


async def get_items_by_category(category_id):
    async with async_session() as session:
       return await session.scalars(select(Item).where(Item.category_id == category_id))


async def get_item(item_id):
    async with async_session() as session:
       return await session.scalar(select(Item).where(Item.id == item_id))


async def add_category(name):
    async with async_session() as session:
        session.add(Category(name=name))
        await session.commit()

async def delete_category(category_id):
    async with async_session() as session:
        await session.execute(delete(Category).where(Category.id == category_id))
        await session.commit()


async def add_item(name, description, price, category_id):
    async with async_session() as session:
        session.add(Item(name=name, description=description, price=price, category_id=category_id))
        await session.commit()


async def edit_category(category_id, new_name):
    async with async_session() as session:
        await session.execute(update(Category).where(Category.id == category_id).values(name=new_name))
        await session.commit()

