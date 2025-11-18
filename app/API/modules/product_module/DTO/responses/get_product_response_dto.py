from uuid import UUID
from pydantic import BaseModel, ConfigDict

class ProductResponse(BaseModel):
    id: UUID
    name: str
    price: float
    stock_quantity: int

    model_config = ConfigDict(from_attributes=True)
