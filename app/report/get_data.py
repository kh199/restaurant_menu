from sqlalchemy import select, func
from app.models import Menu, SubMenu, Dish


async def select_all_data(session):

    all_data = select(
        Menu.title,
        Menu.description,
        func.array_agg(func.json_build_object(
                'title', SubMenu.title,
                'description', SubMenu.description,
                'dishes', select(func.array_agg(func.json_build_object(
                                'title', Dish.title,
                                'description', Dish.description,
                                'price', Dish.price))
                ).scalar_subquery().where(Dish.submenu_id == SubMenu.id)))
        ).join(Menu.submenus).group_by(Menu.id).order_by(Menu.id)

    result = await session.execute(all_data)
    return result.all()
