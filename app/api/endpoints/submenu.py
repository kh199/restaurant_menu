from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import submenu_validator
from app.core.db import get_async_session
from app.crud.submenu import submenu_crud
from app.schemas.submenu import SubMenuCreate, SubMenuOut, SubMenuUpdate

router = APIRouter()


@router.get(
    '/',
    response_model=list[SubMenuOut],
    status_code=HTTPStatus.OK,
    summary='Просмотр списка подменю',
)
async def get_all_submenus(
    menu_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Получение списка всех подменю для конкретного меню
    """
    return await submenu_crud.read_all_subobjects(menu_id, session)


@router.get(
    '/{submenu_id}',
    response_model=SubMenuOut,
    status_code=HTTPStatus.OK,
    summary='Просмотр конкретного подменю по id',
)
async def get_one_submenu(
    submenu_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    await submenu_validator.check_exists(submenu_id, session)
    return await submenu_crud.get_one(submenu_id, session)


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=SubMenuOut,
    summary='Создание подменю',
)
async def create_new_submenu(
    menu_id: str,
    submenu: SubMenuCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Создание подменю:

    - **title**: название (должно быть уникальным)
    - **description**: описание (опционально)
    """
    return await submenu_crud.create_subobject(menu_id, submenu, session)


@router.patch(
    '/{submenu_id}',
    response_model=SubMenuOut,
    status_code=HTTPStatus.OK,
    summary='Обновление подменю',
)
async def to_update_submenu(
        submenu_id: str,
        obj_in: SubMenuUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Обновление подменю:

    - **title**: обновленное название (должно быть уникальным)
    - **description**: обновленное описание (опционально)
    """
    submenu = await submenu_validator.check_exists(submenu_id, session)
    return await submenu_crud.update(submenu, obj_in, session)


@router.delete(
    '/{submenu_id}',
    status_code=HTTPStatus.OK,
    summary='Удаление подменю по id',
)
async def to_delete_submenu(
        submenu_id: str,
        session: AsyncSession = Depends(get_async_session),
):
    submenu = await submenu_crud.get_one(submenu_id, session)
    if submenu is not None:
        await submenu_crud.delete(submenu, session)
        return {'status': True, 'message': 'The submenu has been deleted'}
