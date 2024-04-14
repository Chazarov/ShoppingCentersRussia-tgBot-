import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker

from Database.models import Base
from Database.models import ShoppingCenter


c = 0
async_engine = create_async_engine(os.getenv("DB_ASYNC_URL"))
sync_engine = create_engine(os.getenv("DB_SYNC_URL"))

session_maker = async_sessionmaker(bind = async_engine, class_ = AsyncSession, expire_on_commit = False)
sync_session_maker = sessionmaker(sync_engine)

def add_record(data:dict):
    obj = ShoppingCenter(
        id = data["id"],
        image = data["image"],
        name = data["name"],
        city = data["city"],
        description = data["description"],
        contacts = data["contacts"],
        location = data["adress"],
    )
    with sync_session_maker() as session:
        session.add(obj)
        session.commit()
    
def sin_create_db():
    with sync_engine.begin() as conn:
        conn.run_sync(Base.metadata.create_all)

def sin_drop_db():
    with sync_engine.begin() as conn:
        conn.run_sync(Base.metadata.drop_all)

async def as_create_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def as_drop_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
