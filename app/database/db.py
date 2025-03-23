from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

from database.config import DATABASE_URL

# Создаём движок для работы с PostgreSQL
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаём фабрику сессий
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Создаём таблицы в БД (если их нет)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
