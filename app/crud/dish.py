from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Dish


class DishCrud(CRUDBase):
    async def create_dish_from_dict(
        self,
        parent_id: str,
        id: str,
        title: str,
        description: str,
        price: str,
        session: AsyncSession,
    ):
        dish = self.model(
            id=id,
            title=title,
            description=description,
            price=price,
            parent_id=parent_id,
        )
        session.add(dish)
        await session.commit()
        await session.refresh(dish)
        return dish


dish_crud = DishCrud(Dish)
