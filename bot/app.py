from aiogram import Bot, Dispatcher
from config import BOT_TOKEN, DB_PASS, DB_USER
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import logging
import asyncio
from bot import handlers
from sqlalchemy.orm import sessionmaker
from bot import bot
from db.models import Base
from config import DB_PORT, DB_NAME


async def start_bot():

    logging.basicConfig(
        level=logging.INFO,
    )

    engine = create_async_engine(
        f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@db:{DB_PORT}/{DB_NAME}")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_sessionmaker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    bot["db"] = async_sessionmaker

    await handlers()

try:
    asyncio.run(start_bot())
except (KeyboardInterrupt, SystemExit):
    logging.error("Bot stopped!")
