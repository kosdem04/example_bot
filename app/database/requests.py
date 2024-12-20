from app.database.models import async_session
from app.database.models import Category, Item, User
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload


def connection(func):
    async def inner(*args, **kwargs):
        async with async_session() as session:
            return await func(session ,*args, *kwargs)
    return inner


@connection
async def get_user(session, tg_id):
   return await session.scalar(select(User).options(selectinload(User.language)).where(User.tg_id == tg_id))


@connection
async def get_categories(session):
   return await session.scalars(select(Category))


@connection
async def get_items_by_category(session, category_id):
   return await session.scalars(select(Item).where(Item.category_id == category_id))


@connection
async def get_item(session, item_id):
   return await session.scalar(select(Item).where(Item.id == item_id))


@connection
async def add_category(session, name):
    session.add(Category(name=name))
    await session.commit()


@connection
async def delete_category(session, category_id):
    await session.execute(delete(Category).where(Category.id == category_id))
    await session.commit()


@connection
async def add_item(session, name, description, price, category_id):
    session.add(Item(name=name, description=description, price=price, category_id=category_id))
    await session.commit()


@connection
async def edit_category(session, category_id, new_name):
    await session.execute(update(Category).where(Category.id == category_id).values(name=new_name))
    await session.commit()

