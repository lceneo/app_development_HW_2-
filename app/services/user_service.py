import json
from datetime import timedelta
from uuid import UUID

import redis
from litestar.exceptions import NotFoundException

from app.API.modules.user_module.DTO.requests.user_create_request_dto import UserCreate
from app.API.modules.user_module.DTO.requests.user_update_request_dto import UserUpdate
from app.repositories.user_repository import UserRepository
from sql_schemas import User


class UserService:
    def __init__(self, redis_client: redis.Redis, user_repository: UserRepository):
        self.user_repository = user_repository
        self.redis_client = redis_client

    async def get_by_id(self, user_id: UUID) -> User | None:
        return await self._get_by_id_cached(user_id)

    async def _get_by_id_cached(self, user_id: UUID) -> User | None:
        cache_key = f"user:{user_id}"
        cached_data = self.redis_client.get(cache_key)
        if cached_data:
            user_data = json.loads(cached_data)
            user = User(**user_data)
            return user
        user = await self.user_repository.get_by_id(user_id)
        self.redis_client.setex(
            cache_key, timedelta(hours=1), json.dumps(user.to_dict())
        )
        return user

    async def get_all(self, page: int = 1, count: int = 10) -> tuple[list[User], int]:
        return await self.user_repository.get_all(page=page, count=count)

    async def create(self, user_data: UserCreate) -> User:
        return await self.user_repository.create(user_data)

    async def update(self, user_id: UUID, user_data: UserUpdate) -> User:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        cache_key = f"user:{user_id}"
        cached_data = self.redis_client.get(cache_key)
        if cached_data:
            self.redis_client.delete(cache_key)
        return await self.user_repository.update(user_id, user_data)

    async def delete(self, user_id: UUID) -> None:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        await self.user_repository.delete(user_id)
