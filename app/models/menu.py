from sqlalchemy import Column, String, func, select
from sqlalchemy.orm import column_property, relationship

from app.models.base import BaseModel
from app.models.dish import Dish
from app.models.submenu import SubMenu
from app.models.utils import generate_uuid


class Menu(BaseModel):
    id = Column(String, primary_key=True, default=generate_uuid)
    submenus = relationship('SubMenu', cascade='delete')
    submenus_count = column_property(
        select(func.count(SubMenu.id))
        .where(SubMenu.parent_id == id)
        .scalar_subquery(),
    )
    dishes_count = column_property(
        select(func.count(Dish.id)).
        where(
            Dish.parent_id == select(SubMenu.id).
            where(SubMenu.parent_id == id).scalar_subquery(),
        )
        .scalar_subquery(),
    )
