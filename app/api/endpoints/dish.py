from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.base import dish_crud
from app.crud.dish import create_dish, read_all_dishes
from app.models import Dish
from app.schemas.dish import DishBase, DishCreate, DishOut

router = APIRouter()


@router.get('/', response_model=list[DishOut])
async def get_all_dishes(
    submenu_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    all_dishes = await read_all_dishes(submenu_id, session)
    return all_dishes


@router.get('/{dish_id}', response_model=DishOut)
async def get_one_dish(
    dish_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    dish = await check_dish_exists(dish_id, session)
    dish = await dish_crud.get_one(dish_id, session)
    return dish


@router.post('/', status_code=201, response_model=DishOut)
async def create_new_dish(
    submenu_id: str,
    dish: DishCreate,
    session: AsyncSession = Depends(get_async_session),
):
    new_dish = await create_dish(submenu_id, dish, session)
    return new_dish


@router.patch('/{dish_id}', response_model=DishOut)
async def to_update_dish(
        dish_id: str,
        obj_in: DishBase,
        session: AsyncSession = Depends(get_async_session),
):
    dish = await check_dish_exists(dish_id, session)
    dish = await dish_crud.update(dish, obj_in, session)
    return dish


@router.delete('/{dish_id}')
async def to_delete_dish(
        dish_id: str,
        session: AsyncSession = Depends(get_async_session),
):
    dish = await dish_crud.get_one(dish_id, session)
    if dish is not None:
        await dish_crud.delete(dish, session)
        return {'status': True, 'message': 'The dish has been deleted'}


async def check_dish_exists(
        dish_id: str,
        session: AsyncSession,
) -> Dish:
    dish = await dish_crud.get_one(dish_id, session)
    if dish is None:
        raise HTTPException(
            status_code=404,
            detail='dish not found'
        )
    return dish
