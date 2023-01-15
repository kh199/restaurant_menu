from pydantic import BaseModel


class MenuCreateUpdate(BaseModel):
    title: str
    description: str
