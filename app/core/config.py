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

# RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST", "localhost")
# RABBITMQ_USER: str = os.getenv("RABBITMQ_USER", "admin")
# RABBITMQ_PASS: str = os.getenv("RABBITMQ_PASS", "mypass")

# RABBITMQ_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:5672"


class Settings(BaseSettings):
    app_title: str = 'Меню ресторана'
    database_url: str = DATABASE_URL


settings = Settings()
