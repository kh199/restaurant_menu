from app.api.validators import dish_validator
from app.cache.cache_utils import clear_cache, get_cache, set_cache
from app.crud.dish import dish_crud
from app.schemas.status import StatusMessage


class DishCache:

    @staticmethod
    async def get_dish_list(submenu_id, session):
        cached = await get_cache(submenu_id, 'dish')
        if cached:
            return cached
        dish_list = await dish_crud.read_all_subobjects(submenu_id, session)
        await set_cache(submenu_id, 'dish', dish_list)
        return dish_list

    @staticmethod
    async def get_dish(dish_id, session):
        cached = await get_cache('dish', dish_id)
        if cached:
            return cached
        await dish_validator.check_exists(dish_id, session)
        dish = await dish_crud.get_one(dish_id, session)
        await set_cache('dish', dish_id, dish)
        return dish

    @staticmethod
    async def create_dish(submenu_id, dish, session):
        dish = await dish_crud.create_subobject(submenu_id, dish, session)
        await set_cache('dish', dish.id, dish)
        await clear_cache(submenu_id, 'dish')
        await clear_cache('submenu', submenu_id)
        await clear_cache('menu', 'list')
        return dish

    @staticmethod
    async def update_dish(dish_id, obj_in, session):
        dish = await dish_validator.check_exists(dish_id, session)
        dish = await dish_crud.update(dish, obj_in, session)
        await set_cache('dish', dish_id, dish)
        await clear_cache(dish.parent_id, 'dish')
        await clear_cache('submenu', dish.parent_id)
        await clear_cache('menu', 'list')
        return dish

    @staticmethod
    async def delete_dish(dish_id, session):
        dish = await dish_validator.check_exists(dish_id, session)
        await dish_crud.delete(dish, session)
        await clear_cache('dish', dish_id)
        await clear_cache(dish.parent_id, 'dish')
        await clear_cache('menu', 'list')
        return StatusMessage(
            status=True, message='The dish has been deleted',
        )


dish_service = DishCache()
