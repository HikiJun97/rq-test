# redis_service.py
from contextlib import contextmanager
from typing import Final

from fastapi import FastAPI
from redis import Redis

from redis_config import RedisSettings


class RedisService:
    _instance: Redis | None = None
    _settings: Final[RedisSettings] = RedisSettings()

    def __init__(self):
        self.redis_client: Redis | None = None
        self.settings = RedisSettings()

    @classmethod
    def init_redis_pool(cls) -> None:
        """Initialize Redis connection pool"""
        try:
            cls._instance = Redis(
                host=cls._settings.HOST,
                port=cls._settings.PORT,
                db=cls._settings.DB,
                password=cls._settings.PASS,
                username=cls._settings.USER,
                encoding="utf-8",
                decode_responses=True,
            )
            # Test the connection
            cls._instance.ping()
            print("Successfully connected to Redis")
        except Exception as e:
            print(f"Failed to connect to Redis: {str(e)}")
            raise

    @classmethod
    def close_redis_pool(cls) -> None:
        """Close Redis connection pool"""
        if cls._instance:
            cls._instance.close()
            print("Redis connection closed")

    def get_redis(self) -> Redis | None:
        """Get Redis client instance"""
        if not self.redis_client:
            self.init_redis_pool()
        return self.redis_client
        
    @classmethod
    def get_instance(cls) -> Redis:
        if not cls._instance:
            cls.init_redis_pool()
        return cls._instance