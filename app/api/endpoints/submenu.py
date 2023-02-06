from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.services.submenu_service import submenu_service
from app.core.db import get_async_session
from app.schemas.status import StatusMessage
from app.schemas.submenu import SubMenuCreate, SubMenuOut, SubMenuUpdate

router = APIRouter(
    prefix="/menus/{menu_id}/submenus",
    tags=["Submenus"],
)


@router.get(
    "/",
    response_model=list[SubMenuOut],
    status_code=HTTPStatus.OK,
    summary="Просмотр списка подменю",
)
async def get_all_submenus(
    menu_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> list[SubMenuOut]:
    """
    Получение списка всех подменю для конкретного меню
    """
    return await submenu_service.get_submenu_list(menu_id, session)


@router.get(
    "/{submenu_id}",
    response_model=SubMenuOut,
    status_code=HTTPStatus.OK,
    summary="Просмотр конкретного подменю по id",
)
async def get_one_submenu(
    submenu_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> SubMenuOut:
    return await submenu_service.get_submenu(submenu_id, session)


@router.post(
    "/",
    status_code=HTTPStatus.CREATED,
    response_model=SubMenuOut,
    summary="Создание подменю",
)
async def create_new_submenu(
    menu_id: str,
    submenu: SubMenuCreate,
    session: AsyncSession = Depends(get_async_session),
) -> SubMenuOut:
    """
    Создание подменю:

    - **title**: название (должно быть уникальным)
    - **description**: описание (опционально)
    """
    return await submenu_service.create_submenu(menu_id, submenu, session)


@router.patch(
    "/{submenu_id}",
    response_model=SubMenuOut,
    status_code=HTTPStatus.OK,
    summary="Обновление подменю",
)
async def to_update_submenu(
    submenu_id: str,
    obj_in: SubMenuUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> SubMenuOut:
    """
    Обновление подменю:

    - **title**: обновленное название (должно быть уникальным)
    - **description**: обновленное описание (опционально)
    """
    return await submenu_service.update_submenu(submenu_id, obj_in, session)


@router.delete(
    "/{submenu_id}",
    response_model=StatusMessage,
    status_code=HTTPStatus.OK,
    summary="Удаление подменю по id",
)
async def to_delete_submenu(
    submenu_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> StatusMessage:
    return await submenu_service.delete_submenu(submenu_id, session)
