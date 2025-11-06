from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import ConfigDict

from app.API.modules.user_module.DTO.user_base import UserBase


class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
