from sqlalchemy import Column, ForeignKey, String

from app.models.base import BaseModel
from app.models.utils import generate_uuid


class Dish(BaseModel):
    id = Column(String, primary_key=True, default=generate_uuid)
    price = Column(String, nullable=False)
    parent_id = Column(String, ForeignKey("submenu.id"))
