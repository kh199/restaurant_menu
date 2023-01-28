from sqlalchemy import Column, String, Text

from app.core.db import Base


class BaseModel(Base):
    __abstract__ = True
    title = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
