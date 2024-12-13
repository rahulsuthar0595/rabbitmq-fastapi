from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigSetting(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DEBUG: bool

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    LEADERBOARD_REDIS_CHANNEL: str


@lru_cache
def get_settings():
    return ConfigSetting()


settings = get_settings()
