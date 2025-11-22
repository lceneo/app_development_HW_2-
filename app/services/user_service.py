from uuid import UUID

from litestar.exceptions import NotFoundException

from app.API.modules.user_module.DTO.requests.user_create_request_dto import UserCreate
from app.API.modules.user_module.DTO.requests.user_update_request_dto import UserUpdate
from app.repositories.user_repository import UserRepository
from sql_schemas import User


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_by_id(self, user_id: UUID) -> User | None:
        return await self.user_repository.get_by_id(user_id)

    async def get_all(self, page: int = 1, count: int = 10) -> tuple[list[User], int]:
        return await self.user_repository.get_all(page=page, count=count)

    async def create(self, user_data: UserCreate) -> User:
        return await self.user_repository.create(user_data)

    async def update(self, user_id: UUID, user_data: UserUpdate) -> User:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return await self.user_repository.update(user_id, user_data)

    async def delete(self, user_id: UUID) -> None:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        await self.user_repository.delete(user_id)
