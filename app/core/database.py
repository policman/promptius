import os
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from collections.abc import AsyncGenerator

load_dotenv()  # загружаем .env до получения переменных
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL not set in .env file")

# Создаём асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True)

# Сессия
AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# Базовый класс моделей
Base = declarative_base()

# Функция получения сессии (для зависимостей FastAPI)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
