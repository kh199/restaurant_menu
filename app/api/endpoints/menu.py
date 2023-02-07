from http import HTTPStatus

from fastapi import APIRouter, Depends

from app.cache.services.menu_service import MenuCache, menu_service
from app.schemas.menu import MenuCreate, MenuOut, MenuUpdate
from app.schemas.status import StatusMessage

router = APIRouter(
    prefix="/menus",
    tags=["Menus"],
)


@router.post(
    "/",
    response_model=MenuOut,
    status_code=HTTPStatus.CREATED,
    summary="Создание меню",
)
async def create_new_menu(
    menu: MenuCreate, service: MenuCache = Depends(menu_service)
) -> MenuOut:
    """
    Создание меню:

    - **title**: название (должно быть уникальным)
    - **description**: описание (опционально)
    """
    return await service.create_menu(menu)


@router.get(
    "/{menu_id}",
    response_model=MenuOut,
    status_code=HTTPStatus.OK,
    summary="Просмотр меню по id",
)
async def get_one_menu(
    menu_id: str, service: MenuCache = Depends(menu_service)
) -> MenuOut:
    return await service.get_menu(menu_id)


@router.get(
    "/",
    response_model=list[MenuOut],
    status_code=HTTPStatus.OK,
    summary="Просмотр списка всех меню",
)
async def get_all_menus(service: MenuCache = Depends(menu_service)) -> list[MenuOut]:
    return await service.get_menu_list()


@router.patch(
    "/{menu_id}",
    response_model=MenuOut,
    status_code=HTTPStatus.OK,
    summary="Обновление меню",
)
async def to_update_menu(
    menu_id: str, obj_in: MenuUpdate, service: MenuCache = Depends(menu_service)
) -> MenuOut:
    """
    Обновление меню:

    - **title**: обновленное название (должно быть уникальным)
    - **description**: обновленное описание (опционально)
    """
    return await service.update_menu(menu_id, obj_in)


@router.delete(
    "/{menu_id}",
    response_model=StatusMessage,
    status_code=HTTPStatus.OK,
    summary="Удаление меню по id",
)
async def to_delete_menu(
    menu_id: str, service: MenuCache = Depends(menu_service)
) -> StatusMessage:
    return await service.delete_menu(menu_id)
