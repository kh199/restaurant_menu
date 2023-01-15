from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Меню ресторана'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'


settings = Settings()
