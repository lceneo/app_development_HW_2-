from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OrderProductResponse(BaseModel):
    id: UUID
    name: str
    price: float
    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: UUID
    user_id: UUID
    address_id: Optional[UUID]
    total_amount: float
    status: str
    products: List[OrderProductResponse]
    model_config = ConfigDict(from_attributes=True)
