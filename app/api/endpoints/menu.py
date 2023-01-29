from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.services.menu_service import menu_service
from app.core.db import get_async_session
from app.schemas.menu import MenuCreate, MenuOut, MenuUpdate
from app.schemas.status import StatusMessage

router = APIRouter(
    prefix='/menus',
    tags=['Menus'],
)


@router.post(
    '/',
    response_model=MenuOut,
    status_code=HTTPStatus.CREATED,
    summary='Создание меню',
)
async def create_new_menu(
    menu: MenuCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Создание меню:

    - **title**: название (должно быть уникальным)
    - **description**: описание (опционально)
    """
    return await menu_service.create_menu(menu, session)


@router.get(
    '/{menu_id}',
    response_model=MenuOut,
    status_code=HTTPStatus.OK,
    summary='Просмотр меню по id',
)
async def get_one_menu(
    menu_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    return await menu_service.get_menu(menu_id, session)


@router.get(
    '/',
    response_model=list[MenuOut],
    status_code=HTTPStatus.OK,
    summary='Просмотр списка всех меню',
)
async def get_all_menus(
    session: AsyncSession = Depends(get_async_session),
):
    return await menu_service.get_menu_list(session)


@router.patch(
    '/{menu_id}',
    response_model=MenuOut,
    status_code=HTTPStatus.OK,
    summary='Обновление меню',
)
async def to_update_menu(
        menu_id: str,
        obj_in: MenuUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Обновление меню:

    - **title**: обновленное название (должно быть уникальным)
    - **description**: обновленное описание (опционально)
    """
    return await menu_service.update_menu(menu_id, obj_in, session)


@router.delete(
    '/{menu_id}',
    response_model=StatusMessage,
    status_code=HTTPStatus.OK,
    summary='Удаление меню по id',
)
async def to_delete_menu(
        menu_id: str,
        session: AsyncSession = Depends(get_async_session),
):
    return await menu_service.delete_menu(menu_id, session)
