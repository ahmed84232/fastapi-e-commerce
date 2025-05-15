from typing import AsyncGenerator
from sqlmodel import Session, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from fastapi import Request


engine = create_async_engine('postgresql+asyncpg://postgres:postgres@localhost:5432/postgres')

async def get_session() -> AsyncGenerator[AsyncSession, None]:

    async with AsyncSession(engine) as session:
        try:
            yield session
        finally:
            await session.close()
