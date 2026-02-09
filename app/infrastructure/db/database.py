from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.core.config import settings

from app.infrastructure.db.base import Base
from app.infrastructure.models import user, post, comment

logger = logging.getLogger(__name__)

engine = create_async_engine(settings.db.DATABASE_URL, echo=False)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Database error occurred: {e}")
            raise
        finally:
            await session.close()


async def init_db():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
