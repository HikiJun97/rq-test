# database_engine.py
from typing import Final

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import SQLModel

from database_config import DatabaseSettings


class DatabaseEngine:
    """Database engine manager"""

    _instance: AsyncEngine | None = None
    _settings: Final[DatabaseSettings] = DatabaseSettings()

    @classmethod
    def get_engine(cls) -> AsyncEngine:
        """Get or create SQLAlchemy async engine instance"""
        if cls._instance is None:
            cls._instance = create_async_engine(
                cls._settings.url,
                echo=cls._settings.ECHO,
                pool_size=cls._settings.POOL_SIZE,
                max_overflow=cls._settings.MAX_OVERFLOW,
                pool_recycle=cls._settings.POOL_RECYCLE,
                pool_pre_ping=cls._settings.POOL_PRE_PING,
            )
            print("Successfully connected to MariaDB")
        return cls._instance

    @classmethod
    async def dispose_engine(cls) -> None:
        """Dispose the database engine"""
        if cls._instance is not None:
            await cls._instance.dispose()
            cls._instance = None

    @classmethod
    async def init_tables(cls) -> None:
        """Initialize database tables"""
        async with cls.get_engine().begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
