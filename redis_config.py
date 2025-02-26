from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    """Redis connection settings with Pydantic"""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="REDIS_", extra="ignore")
    
    HOST: Annotated[str, Field(...)] = ""
    PORT: Annotated[int, Field(...)] = 0
    DB: Annotated[int, Field(...)] = 0
    PASS: Annotated[str, Field(...)] = ""
    USER: Annotated[str, Field(...)] = ""
    
    