from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigSetting(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DEBUG: bool

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    LEADERBOARD_REDIS_CHANNEL: str

    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBIT_MQ_ORDER_QUEUE: str

    KAFKA_SERVER_URL: str
    KAFKA_TOPIC_NAME: str
    KAFKA_GROUP_NAME: str


@lru_cache
def get_settings():
    return ConfigSetting()


settings = get_settings()
