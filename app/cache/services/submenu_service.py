from app.api.validators import submenu_validator
from app.cache.cache_utils import clear_cache, get_cache, set_cache
from app.crud.submenu import submenu_crud
from app.schemas.status import StatusMessage


class SubMenuCache:

    @staticmethod
    async def get_submenu_list(menu_id, session):
        cached = await get_cache(menu_id, 'submenu')
        if cached:
            return cached
        submenu_list = await submenu_crud.read_all_subobjects(menu_id, session)
        await set_cache(menu_id, 'submenu', submenu_list)
        return submenu_list

    @staticmethod
    async def get_submenu(submenu_id, session):
        cached = await get_cache('submenu', submenu_id)
        if cached:
            return cached
        await submenu_validator.check_exists(submenu_id, session)
        submenu = await submenu_crud.get_one(submenu_id, session)
        await set_cache('submenu', submenu_id, submenu)
        return submenu

    @staticmethod
    async def create_submenu(menu_id, submenu, session):
        submenu = await submenu_crud.create_subobject(
            menu_id, submenu, session,
        )
        await set_cache('submenu', submenu.id, submenu)
        await clear_cache('menu', menu_id)
        await clear_cache('menu', 'list')
        return submenu

    @staticmethod
    async def update_submenu(submenu_id, obj_in, session):
        submenu = await submenu_validator.check_exists(submenu_id, session)
        submenu = await submenu_crud.update(submenu, obj_in, session)
        await set_cache('submenu', submenu_id, submenu)
        await clear_cache(submenu.parent_id, 'submenu')
        await clear_cache('menu', submenu.parent_id)
        await clear_cache('menu', 'list')
        return submenu

    @staticmethod
    async def delete_submenu(submenu_id, session):
        submenu = await submenu_validator.check_exists(submenu_id, session)
        await submenu_crud.delete(submenu, session)
        await clear_cache('submenu', submenu_id)
        await clear_cache(submenu.parent_id, 'submenu')
        await clear_cache('menu', submenu.parent_id)
        await clear_cache('menu', 'list')
        return StatusMessage(
            status=True, message='The submenu has been deleted',
        )


submenu_service = SubMenuCache()
