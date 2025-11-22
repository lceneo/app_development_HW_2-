from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    name: str
    price: float
    stock_quantity: int

    model_config = ConfigDict(from_attributes=True)
