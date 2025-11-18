from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel


class OrderUpdate(BaseModel):
    user_id: Optional[UUID] = None
    address_id: Optional[UUID] = None
    status: Optional[str] = None
    product_ids: Optional[List[UUID]] = None