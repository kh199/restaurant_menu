from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import dish_validator
from app.cache.cache_utils import clear_cache, get_cache, set_cache
from app.core.db import get_async_session
from app.crud.dish import dish_crud
from app.schemas.status import StatusMessage


class DishCache:
    def __init__(self, session):
        self.session = session

    async def get_dish_list(self, submenu_id):
        cached = await get_cache(submenu_id, "dish")
        if cached:
            return cached
        dish_list = await dish_crud.read_all_subobjects(submenu_id, self.session)
        await set_cache(submenu_id, "dish", dish_list)
        return dish_list

    async def get_dish(self, dish_id):
        cached = await get_cache("dish", dish_id)
        if cached:
            return cached
        await dish_validator.check_exists(dish_id, self.session)
        dish = await dish_crud.get_one(dish_id, self.session)
        await set_cache("dish", dish_id, dish)
        return dish

    async def create_dish(self, submenu_id, dish):
        await dish_validator.check_title(dish.title, self.session)
        dish = await dish_crud.create_subobject(submenu_id, dish, self.session)
        await set_cache("dish", dish.id, dish)
        await clear_cache(submenu_id, "dish")
        await clear_cache("submenu", submenu_id)
        await clear_cache("menu", "list")
        return dish

    async def update_dish(self, dish_id, obj_in):
        dish = await dish_validator.check_exists(dish_id, self.session)
        dish = await dish_crud.update(dish, obj_in, self.session)
        await set_cache("dish", dish_id, dish)
        await clear_cache(dish.parent_id, "dish")
        await clear_cache("submenu", dish.parent_id)
        await clear_cache("menu", "list")
        return dish

    async def delete_dish(self, dish_id):
        dish = await dish_validator.check_exists(dish_id, self.session)
        await dish_crud.delete(dish, self.session)
        await clear_cache("dish", dish_id)
        await clear_cache(dish.parent_id, "dish")
        await clear_cache("menu", "list")
        return StatusMessage(
            status=True,
            message="The dish has been deleted",
        )


async def dish_service(session: AsyncSession = Depends(get_async_session)):
    return DishCache(session=session)
