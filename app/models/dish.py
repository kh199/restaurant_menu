from sqlalchemy import Column, ForeignKey, String, Text

from app.core.db import Base

from .utils import generate_uuid


class Dish(Base):
    __tablename__ = "dish"
    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(String, nullable=False)
    submenu_id = Column(String, ForeignKey("submenu.id"))
