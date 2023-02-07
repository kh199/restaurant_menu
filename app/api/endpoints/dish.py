from http import HTTPStatus

from fastapi import APIRouter, Depends

from app.cache.services.dish_service import DishCache, dish_service
from app.schemas.dish import DishCreate, DishOut, DishUpdate
from app.schemas.status import StatusMessage

router = APIRouter(
    prefix="/menus/{menu_id}/submenus/{submenu_id}/dishes",
    tags=["Dishes"],
)


@router.get(
    "/",
    response_model=list[DishOut],
    status_code=HTTPStatus.OK,
    summary="Просмотр списка блюд",
)
async def get_all_dishes(
    submenu_id: str, service: DishCache = Depends(dish_service)
) -> list[DishOut]:
    """
    Получение списка всех блюд для конкретного подменю
    """
    return await service.get_dish_list(submenu_id)


@router.get(
    "/{dish_id}",
    response_model=DishOut,
    status_code=HTTPStatus.OK,
    summary="Просмотр блюда по id",
)
async def get_one_dish(
    dish_id: str, service: DishCache = Depends(dish_service)
) -> DishOut:
    return await service.get_dish(dish_id)


@router.post(
    "/",
    response_model=DishOut,
    status_code=HTTPStatus.CREATED,
    summary="Создание блюда",
)
async def create_new_dish(
    submenu_id: str, dish: DishCreate, service: DishCache = Depends(dish_service)
) -> DishOut:
    """
    Создание блюда:

    - **title**: название (должно быть уникальным)
    - **description**: описание (опционально)
    - **price**: цена (обязательно), должна быть строкой,
                 округляется до двух знаков после запятой
    """
    return await service.create_dish(submenu_id, dish)


@router.patch(
    "/{dish_id}",
    response_model=DishOut,
    status_code=HTTPStatus.OK,
    summary="Обновление блюда",
)
async def to_update_dish(
    dish_id: str, obj_in: DishUpdate, service: DishCache = Depends(dish_service)
) -> DishOut:
    """
    Обновление блюда:

    - **title**: обновленное название (должно быть уникальным)
    - **description**: обновленное описание (опционально)
    - **price**: обновленная цена (обязательно), должна быть строкой,
                 округляется до двух знаков после запятой
    """
    return await service.update_dish(dish_id, obj_in)


@router.delete(
    "/{dish_id}",
    response_model=StatusMessage,
    status_code=HTTPStatus.OK,
    summary="Удаление блюда по id",
)
async def to_delete_dish(
    dish_id: str, service: DishCache = Depends(dish_service)
) -> StatusMessage:
    return await service.delete_dish(dish_id)
