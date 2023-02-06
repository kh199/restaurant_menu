from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import SubMenu


class SubMenuCrud(CRUDBase):
    async def create_submenu_from_dict(
        self,
        parent_id: str,
        id: str,
        title: str,
        description: str,
        session: AsyncSession,
    ):
        submenu = self.model(
            id=id, title=title, description=description, parent_id=parent_id
        )
        session.add(submenu)
        await session.commit()
        await session.refresh(submenu)
        return submenu


submenu_crud = SubMenuCrud(SubMenu)
