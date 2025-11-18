from typing import List
from uuid import UUID

from pydantic import BaseModel


class OrderCreate(BaseModel):
    user_id: UUID
    product_ids: List[UUID]