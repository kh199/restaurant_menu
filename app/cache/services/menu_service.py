from app.api.validators import menu_validator
from app.cache.cache_utils import clear_cache, get_cache, set_cache
from app.crud.menu import menu_crud
from app.schemas.status import StatusMessage


class MenuCache:

    @staticmethod
    async def create_menu(menu, session):
        menu = await menu_crud.create(menu, session)
        await set_cache('menu', menu.id, menu)
        await clear_cache('menu', 'list')
        return menu

    @staticmethod
    async def get_menu(menu_id, session):
        cached = await get_cache('menu', menu_id)
        if cached:
            return cached
        await menu_validator.check_exists(menu_id, session)
        menu = await menu_crud.get_one(menu_id, session)
        await set_cache('menu', menu_id, menu)
        return menu

    @staticmethod
    async def get_menu_list(session):
        cached = await get_cache('menu', 'list')
        if cached:
            return cached
        menu_list = await menu_crud.get_many(session)
        await set_cache('menu', 'list', menu_list)
        return menu_list

    @staticmethod
    async def update_menu(menu_id, obj_in, session):
        menu = await menu_validator.check_exists(menu_id, session)
        menu = await menu_crud.update(menu, obj_in, session)
        await set_cache('menu', menu.id, menu)
        await clear_cache('menu', 'list')
        return menu

    @staticmethod
    async def delete_menu(menu_id, session):
        menu = await menu_validator.check_exists(menu_id, session)
        await menu_crud.delete(menu, session)
        await clear_cache('menu', menu_id)
        await clear_cache('menu', 'list')
        return StatusMessage(
            status=True, message='The menu has been deleted',
        )


menu_service = MenuCache()
