from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models import Menu, SubMenu


async def select_all_data(session):
    result = await session.scalars(
        select(Menu).options(joinedload(Menu.submenus).joinedload(SubMenu.dishes))
    )
    menus = result.unique().all()
    menu_data = jsonable_encoder(menus)
    return menu_data
