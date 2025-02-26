# fastapi_lifespan.py
from contextlib import asynccontextmanager

from fastapi import FastAPI

from redis_service import RedisService
from database_engine import DatabaseEngine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and close Redis connection pool"""
    RedisService.init_redis_pool()
    await DatabaseEngine.init_tables()

    yield
    
    RedisService.close_redis_pool()
    await DatabaseEngine.dispose_engine()
