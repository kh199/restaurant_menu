from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SubMenu
from app.schemas.submenu import SubMenuCreate


async def read_all_submenus(
    menu_id: str,
    session: AsyncSession
) -> list[SubMenu]:
    all_submenus = await session.execute(
        select(SubMenu).where(SubMenu.menu_id == menu_id)
    )
    return all_submenus.scalars().all()


async def create_submenu(
    menu_id: str,
    submenu: SubMenuCreate,
    session: AsyncSession,
) -> SubMenu:
    new_submenu_data = submenu.dict()
    db_submenu = SubMenu(**new_submenu_data, menu_id=menu_id)
    session.add(db_submenu)
    await session.commit()
    await session.refresh(db_submenu)
    return db_submenu
