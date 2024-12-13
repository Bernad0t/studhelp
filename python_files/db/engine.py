# import asyncio
# from asyncio import WindowsSelectorEventLoopPolicy
from typing import Annotated
from sqlalchemy import String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing_extensions import AsyncGenerator

from db.config import settings

# Загружаем информацию о бд из config.py

# asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

# Создаем асинхронный движок для подключения к postgres
async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
    pool_size=5,
    max_overflow=10
)

str_256 = Annotated[str, 256]
class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }


# Session нужна для транзакций
async_session_factory = async_sessionmaker(async_engine)


# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async_session = async_session_factory()
#
#     async with async_session:
#         try:
#             yield async_session
#             await async_session.commit()
#         except SQLAlchemyError as exc:
#             await async_session.rollback()
#             raise exc
#         finally:
#             await async_session.close()