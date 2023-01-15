from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.base import submenu_crud
from app.crud.submenu import create_submenu, read_all_submenus
from app.models import SubMenu
from app.schemas.submenu import SubMenuBase, SubMenuCreate, SubMenuOut

router = APIRouter()


@router.get('/', response_model=list[SubMenuOut])
async def get_all_submenus(
    menu_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    all_submenus = await read_all_submenus(menu_id, session)
    return all_submenus


@router.get('/{submenu_id}', response_model=SubMenuOut)
async def get_one_submenu(
    submenu_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    submenu = await check_submenu_exists(submenu_id, session)
    submenu = await submenu_crud.get_one(submenu_id, session)
    return submenu


@router.post('/', status_code=201, response_model=SubMenuOut)
async def create_new_submenu(
    menu_id: str,
    submenu: SubMenuCreate,
    session: AsyncSession = Depends(get_async_session),
):
    new_submenu = await create_submenu(menu_id, submenu, session)
    return new_submenu


@router.patch('/{submenu_id}', response_model=SubMenuOut)
async def to_update_submenu(
        submenu_id: str,
        obj_in: SubMenuBase,
        session: AsyncSession = Depends(get_async_session),
):
    submenu = await check_submenu_exists(submenu_id, session)
    submenu = await submenu_crud.update(submenu, obj_in, session)
    return submenu


@router.delete('/{submenu_id}')
async def to_delete_submenu(
        submenu_id: str,
        session: AsyncSession = Depends(get_async_session),
):
    submenu = await submenu_crud.get_one(submenu_id, session)
    if submenu is not None:
        await submenu_crud.delete(submenu, session)
        return {'status': True, 'message': 'The submenu has been deleted'}


async def check_submenu_exists(
        submenu_id: str,
        session: AsyncSession,
) -> SubMenu:
    submenu = await submenu_crud.get_one(submenu_id, session)
    if submenu is None:
        raise HTTPException(
            status_code=404,
            detail='submenu not found'
        )
    return submenu
