from sqlalchemy import Column, ForeignKey, String, func, select
from sqlalchemy.orm import column_property, relationship

from app.models.base import BaseModel
from app.models.dish import Dish
from app.models.utils import generate_uuid


class SubMenu(BaseModel):
    id = Column(String, primary_key=True, default=generate_uuid)
    parent_id = Column(String, ForeignKey("menu.id"))
    dishes = relationship("Dish", cascade="delete", backref="submenu", lazy="selectin")
    dishes_count = column_property(
        select(func.count(Dish.id)).where(Dish.parent_id == id).scalar_subquery(),
    )
