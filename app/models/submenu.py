from sqlalchemy import Column, ForeignKey, String, Text, func, select
from sqlalchemy.orm import column_property, relationship

from app.core.db import Base
from app.models.dish import Dish

from .utils import generate_uuid


class SubMenu(Base):
    __tablename__ = "submenu"
    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    menu_id = Column(String, ForeignKey("menu.id"))
    dishes = relationship('Dish', cascade='delete')
    dishes_count = column_property(
        select(func.count(Dish.id))
        .where(Dish.submenu_id == id)
        .scalar_subquery()
    )
