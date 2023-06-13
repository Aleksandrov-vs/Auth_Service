from logging import config as logging_config

from pydantic import BaseSettings, Field

from src.core.logger import LOGGING
from dotenv import load_dotenv


load_dotenv()
logging_config.dictConfig(LOGGING)


class PostgresSettings(BaseSettings):
    dbname: str = Field(..., env='POSTGRES_DB')
    user: str = Field(..., env='POSTGRES_USER')
    password: str = Field(..., env="POSTGRES_PASSWORD")
    host: str = Field('localhost', env='POSTGRES_HOST')
    port: int = Field(5432, env='POSTGRES_PORT')


class RedisSettings(BaseSettings):
    host: str = Field('localhost', env='REDIS_HOST')
    port: int = Field(6379, env='REDIS_PORT')


class Settings(BaseSettings):
    secret_key: str = Field(..., env='SECRET_KEY')
    debug: bool = Field(..., env='DEBUG')
    postgres: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()

    default_rate_limit: int = Field(10, env='DEFAULT_RATE_LIMIT')
    default_rate_period: int = Field(60, env='DEFAULT_RATE_PERIOD')
    max_rate_penalty: int = Field(1800, env='MAX_RATE_PENALTY')

    tracer_enabled: bool = Field(True, env='TRACER_ENABLED')
    console_tracer_enabled: bool = Field(False, env='CONSOLE_TRACING_ENABLED')
    tracer_host: str = Field('localhost', env='TRACER_HOST')
    tracer_port: int = Field(6831, env='TRACER_PORT')


settings = Settings()
