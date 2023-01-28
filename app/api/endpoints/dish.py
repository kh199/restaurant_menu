from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import dish_validator
from app.core.db import get_async_session
from app.crud.dish import dish_crud
from app.schemas.dish import DishCreate, DishOut, DishUpdate

router = APIRouter()


@router.get(
    '/',
    response_model=list[DishOut],
    status_code=HTTPStatus.OK,
    summary='Просмотр списка блюд',
)
async def get_all_dishes(
    submenu_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Получение списка всех блюд для конкретного подменю
    """
    return await dish_crud.read_all_subobjects(submenu_id, session)


@router.get(
    '/{dish_id}',
    response_model=DishOut,
    status_code=HTTPStatus.OK,
    summary='Просмотр блюда по id',
)
async def get_one_dish(
    dish_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    await dish_validator.check_exists(dish_id, session)
    return await dish_crud.get_one(dish_id, session)


@router.post(
    '/',
    response_model=DishOut,
    status_code=HTTPStatus.CREATED,
    summary='Создание блюда',
)
async def create_new_dish(
    submenu_id: str,
    dish: DishCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Создание блюда:

    - **title**: название (должно быть уникальным)
    - **description**: описание (опционально)
    - **price**: цена (обязательно), должна быть строкой,
                 округляется до двух знаков после запятой
    """
    return await dish_crud.create_subobject(submenu_id, dish, session)


@router.patch(
    '/{dish_id}',
    response_model=DishOut,
    status_code=HTTPStatus.OK,
    summary='Обновление блюда',
)
async def to_update_dish(
        dish_id: str,
        obj_in: DishUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Обновление блюда:

    - **title**: обновленное название (должно быть уникальным)
    - **description**: обновленное описание (опционально)
    - **price**: обновленная цена (обязательно), должна быть строкой,
                 округляется до двух знаков после запятой
    """
    dish = await dish_validator.check_exists(dish_id, session)
    return await dish_crud.update(dish, obj_in, session)


@router.delete(
    '/{dish_id}',
    status_code=HTTPStatus.OK,
    summary='Удаление блюда по id',
)
async def to_delete_dish(
        dish_id: str,
        session: AsyncSession = Depends(get_async_session),
):
    dish = await dish_crud.get_one(dish_id, session)
    if dish is not None:
        await dish_crud.delete(dish, session)
        return {'status': True, 'message': 'The dish has been deleted'}
