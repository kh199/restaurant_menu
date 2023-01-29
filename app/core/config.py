from pydantic import BaseSettings

DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@db:5432/postgres'


class Settings(BaseSettings):
    app_title: str = 'Меню ресторана'
    database_url: str = DATABASE_URL


settings = Settings()
