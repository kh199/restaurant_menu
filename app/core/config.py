import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

DB_HOST = os.getenv('POSTGRES_HOST')
DB_NAME = os.getenv('POSTGRES_DB')
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}' \
               f'@{DB_HOST}:5432/{DB_NAME}'

TEST_DATABASE_URL = os.getenv('TEST_DATABASE_URL')
TEST_ASYNC_DATABASE_URL = os.getenv('TEST_ASYNC_DATABASE_URL')


class Settings(BaseSettings):
    app_title: str = 'Меню ресторана'
    database_url: str = DATABASE_URL


settings = Settings()
