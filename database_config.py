# database_config.py
from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Database specific settings"""

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="DATABASE_", extra="ignore"
    )

    HOST: Annotated[str, Field(...)] = ""
    USER: Annotated[str, Field(...)] = ""
    PASS: Annotated[str, Field(...)] = ""
    PORT: Annotated[int, Field(...)] = 0
    NAME: Annotated[str, Field(...)] = ""
    ECHO: Annotated[bool, Field(...)] = False
    POOL_SIZE: Annotated[int, Field(...)] = 20
    MAX_OVERFLOW: Annotated[int, Field(...)] = 20
    POOL_RECYCLE: Annotated[int, Field(...)] = 500
    POOL_PRE_PING: Annotated[bool, Field(...)] = True

    @property
    def url(self) -> str:
        """Generate database URL based on configuration"""
        if self.HOST == "localhost":
            return f"mysql+aiomysql://{self.USER}:{self.PASS}@{self.HOST}/{self.NAME}"
        return f"mysql+aiomysql://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"
