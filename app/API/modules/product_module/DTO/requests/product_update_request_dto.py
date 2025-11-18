from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None