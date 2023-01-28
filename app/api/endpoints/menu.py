from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import menu_validator
from app.core.db import get_async_session
from app.crud.menu import menu_crud
from app.schemas.menu import MenuCreate, MenuOut, MenuUpdate

router = APIRouter()


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
    return await menu_crud.create(menu, session)


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
    await menu_validator.check_exists(menu_id, session)
    return await menu_crud.get_one(menu_id, session)


@router.get(
    '/',
    response_model=list[MenuOut],
    status_code=HTTPStatus.OK,
    summary='Просмотр списка всех меню',
)
async def get_all_menus(
    session: AsyncSession = Depends(get_async_session),
):
    return await menu_crud.get_many(session)


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
    menu = await menu_validator.check_exists(menu_id, session)
    return await menu_crud.update(menu, obj_in, session)


@router.delete(
    '/{menu_id}',
    status_code=HTTPStatus.OK,
    summary='Удаление меню по id',
)
async def to_delete_menu(
        menu_id: str,
        session: AsyncSession = Depends(get_async_session),
):
    menu = await menu_crud.get_one(menu_id, session)
    if menu is not None:
        await menu_crud.delete(menu, session)
        return {'status': True, 'message': 'The menu has been deleted'}
