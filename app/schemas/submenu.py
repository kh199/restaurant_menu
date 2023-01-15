from pydantic import BaseModel


class SubMenuBase(BaseModel):
    title: str
    description: str


class SubMenuCreate(SubMenuBase):
    menu_id = str


class SubMenuOut(SubMenuBase):
    id: str
    dishes_count: int

    class Config:
        orm_mode = True
