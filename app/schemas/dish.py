from pydantic import BaseModel, validator


class DishBase(BaseModel):
    title: str
    description: str
    price: str

    @validator('price')
    def check_price(cls, value: str):
        if not float(value):
            raise ValueError('price must be a number')
        value = format(float(value), '.2f')
        return value


class DishCreate(DishBase):
    submenu_id = str


class DishOut(DishBase):
    id: str

    class Config:
        orm_mode = True
