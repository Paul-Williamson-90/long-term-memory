from contextlib import contextmanager, asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

from src.settings import settings


engine = create_engine(settings.pg_url, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


sync_engine = create_engine(settings.pg_url, echo=True)
SyncSessionLocal = sessionmaker(bind=sync_engine, autocommit=False, autoflush=False)

async_engine = create_async_engine(settings.async_pg_url, echo=True)
AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, autocommit=False, autoflush=False)


@contextmanager
def get_session():
    session = SyncSessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@asynccontextmanager
async def aget_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise