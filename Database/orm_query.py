from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from Database.models import ShoppingCenter


async def get_center_by_name(session: AsyncSession, center_name:str):
    query = select(ShoppingCenter).where(ShoppingCenter.name == center_name)
    result = await session.execute(query)
    return result.scalar()

async def get_center(session: AsyncSession, center_id:str):
    query = select(ShoppingCenter).where(ShoppingCenter.id == center_id)
    result = await session.execute(query)
    return result.scalar()


async def get_all_centers(session: AsyncSession):
    query = select(ShoppingCenter)
    result = await session.execute(query)
    return result.scalars().all()

async def get_centers_in_city(session: AsyncSession, name_city:str):
    query = select(ShoppingCenter).where(ShoppingCenter.city == name_city)
    result = await session.execute(query)
    return result.scalars().all()

async def async_add_center(session: AsyncSession, data:dict):
    obj = ShoppingCenter(
        id = data["id"],
        name = data["name"],
        city = data["city"],
        description = data["description"],
        contacts = data["contacts"],
        location = data["adress"],
    )
    session.add(obj)
    await session.commit()
    