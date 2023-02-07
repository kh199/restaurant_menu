from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import menu_validator
from app.cache.cache_utils import clear_cache, get_cache, set_cache
from app.core.db import get_async_session
from app.crud.menu import menu_crud
from app.schemas.status import StatusMessage


class MenuCache:
    def __init__(self, session):
        self.session = session

    async def create_menu(self, menu):
        await menu_validator.check_title(menu.title, self.session)
        menu = await menu_crud.create(menu, self.session)
        await set_cache("menu", menu.id, menu)
        await clear_cache("menu", "list")
        return menu

    async def get_menu(self, menu_id):
        cached = await get_cache("menu", menu_id)
        if cached:
            return cached
        await menu_validator.check_exists(menu_id, self.session)
        menu = await menu_crud.get_one(menu_id, self.session)
        await set_cache("menu", menu_id, menu)
        return menu

    async def get_menu_list(self):
        cached = await get_cache("menu", "list")
        if cached:
            return cached
        menu_list = await menu_crud.get_many(self.session)
        await set_cache("menu", "list", menu_list)
        return menu_list

    async def update_menu(self, menu_id, obj_in):
        menu = await menu_validator.check_exists(menu_id, self.session)
        menu = await menu_crud.update(menu, obj_in, self.session)
        await set_cache("menu", menu.id, menu)
        await clear_cache("menu", "list")
        return menu

    async def delete_menu(self, menu_id):
        menu = await menu_validator.check_exists(menu_id, self.session)
        await menu_crud.delete(menu, self.session)
        await clear_cache("menu", menu_id)
        await clear_cache("menu", "list")
        return StatusMessage(
            status=True,
            message="The menu has been deleted",
        )

    async def get_all_data(self):
        return await menu_crud.select_all_data(self.session)


async def menu_service(session: AsyncSession = Depends(get_async_session)):
    return MenuCache(session=session)
