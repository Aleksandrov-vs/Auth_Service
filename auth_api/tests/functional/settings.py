from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()


class TestSettings(BaseSettings):
    pg_host: str = Field('localhost', env='POSTGRES_HOST')
    pg_port: int = Field(5432, env='POSTGRES_PORT')

    redis_host: str = Field('localhost', env='REDIS_HOST')
    redis_port: int = Field(6379, env='REDIS_PORT')

    service_url: str = Field('http://127.0.0.1:8000', env='SERVICE_URL')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


test_settings = TestSettings()