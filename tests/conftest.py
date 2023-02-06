import asyncio
from collections.abc import Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import TEST_ASYNC_DATABASE_URL, TEST_DATABASE_URL
from app.core.db import Base, get_async_session
from app.main import app
from app.models import Dish, Menu, SubMenu
from tests.test_data import dish_data, menu_data, submenu_data

async_engine = create_async_engine(TEST_ASYNC_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def override_db():
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    app.dependency_overrides[get_async_session] = override_db
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


engine = create_engine(TEST_DATABASE_URL)
Session = sessionmaker(bind=engine)


def override_get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()


db = next(override_get_db())


@pytest.fixture
def create_menu():
    new_menu = Menu(**menu_data)
    db.add(new_menu)
    db.commit()
    return new_menu


@pytest.fixture
def create_submenu(create_menu):
    new_submenu = SubMenu(**submenu_data, parent_id=create_menu.id)
    db.add(new_submenu)
    db.commit()
    return new_submenu


@pytest.fixture
def create_dish(create_submenu):
    new_dish = Dish(**dish_data, parent_id=create_submenu.id)
    db.add(new_dish)
    db.commit()
    return new_dish
