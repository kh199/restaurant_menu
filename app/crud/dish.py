from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Dish
from app.schemas.dish import DishCreate


async def read_all_dishes(
    submenu_id: str,
    session: AsyncSession
) -> list[Dish]:
    all_dishes = await session.execute(
        select(Dish).where(Dish.submenu_id == submenu_id)
    )
    return all_dishes.scalars().all()


async def create_dish(
    submenu_id: str,
    dish: DishCreate,
    session: AsyncSession,
) -> Dish:
    new_dish_data = dish.dict()
    db_dish = Dish(**new_dish_data, submenu_id=submenu_id)
    session.add(db_dish)
    await session.commit()
    await session.refresh(db_dish)
    return db_dish
