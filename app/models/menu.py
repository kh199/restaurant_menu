from sqlalchemy import Column, String, Text, func, select
from sqlalchemy.orm import column_property, relationship

from app.core.db import Base
from app.models.dish import Dish
from app.models.submenu import SubMenu

from .utils import generate_uuid


class Menu(Base):
    __tablename__ = "menu"
    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    submenus = relationship('SubMenu', cascade='delete')
    submenus_count = column_property(
        select(func.count(SubMenu.id))
        .where(SubMenu.menu_id == id)
        .scalar_subquery()
    )
    dishes_count = column_property(
        select(func.count(Dish.id)).
        where(Dish.submenu_id == select(SubMenu.id).
              where(SubMenu.menu_id == id).scalar_subquery())
        .scalar_subquery()
    )
