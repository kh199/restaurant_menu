from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.base import menu_crud
from app.models.menu import Menu
from app.schemas.menu import MenuCreateUpdate

router = APIRouter()


@router.post('/', status_code=201)
async def create_new_menu(
    menu: MenuCreateUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    new_menu = await menu_crud.create(menu, session)
    return new_menu


@router.get('/{menu_id}')
async def get_one_menu(
    menu_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    menu = await check_menu_exists(menu_id, session)
    menu = await menu_crud.get_one(menu_id, session)
    return menu


@router.get('/')
async def get_all_menus(
    session: AsyncSession = Depends(get_async_session),
):
    all_menus = await menu_crud.get_many(session)
    return all_menus


@router.patch('/{menu_id}')
async def to_update_menu(
        menu_id: str,
        obj_in: MenuCreateUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    menu = await check_menu_exists(menu_id, session)
    menu = await menu_crud.update(menu, obj_in, session)
    return menu


@router.delete('/{menu_id}')
async def to_delete_menu(
        menu_id: str,
        session: AsyncSession = Depends(get_async_session),
):
    menu = await menu_crud.get_one(menu_id, session)
    if menu is not None:
        await menu_crud.delete(menu, session)
        return {'status': True, 'message': 'The menu has been deleted'}


async def check_menu_exists(
        menu_id: str,
        session: AsyncSession,
) -> Menu:
    menu = await menu_crud.get_one(menu_id, session)
    if menu is None:
        raise HTTPException(
            status_code=404,
            detail='menu not found'
        )
    return menu
