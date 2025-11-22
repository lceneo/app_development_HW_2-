from uuid import UUID

from litestar import Controller, delete, get, post, put
from litestar.exceptions import NotFoundException
from litestar.params import Parameter

from app.API.modules.user_module.DTO.requests.user_create_request_dto import UserCreate
from app.API.modules.user_module.DTO.responses.get_user_response_dto import UserResponse
from app.services.user_service import UserService


class UserController(Controller):
    path = "/users"
    tags = ["Users"]

    @get("/{user_id:uuid}")
    async def get_user_by_id(
        self,
        user_service: UserService,
        user_id: UUID,
    ) -> UserResponse:
        user = await user_service.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(user)

    @get()
    async def get_all_users(
        self,
        user_service: UserService,
        page: int = Parameter(ge=1, default=1, description="Номер страницы"),
        count: int = Parameter(
            ge=1, le=100, default=10, description="Количество записей на странице"
        ),
    ) -> dict:
        users, total_count = await user_service.get_all(page=page, count=count)
        return {
            "users": [UserResponse.model_validate(user) for user in users],
            "total_count": total_count,
            "page": page,
            "count": count,
            "total_pages": (total_count + count - 1) // count,
        }

    @post()
    async def create_user(
        self,
        user_service: UserService,
        data: UserCreate,
    ) -> UserResponse:
        user = await user_service.create(data)
        return UserResponse.model_validate(user)

    @delete("/{user_id:uuid}")
    async def delete_user(
        self,
        user_service: UserService,
        user_id: UUID,
    ) -> None:
        await user_service.delete(user_id)

    @put("/{user_id:uuid}")
    async def update_user(
        self,
        user_service: UserService,
        user_id: UUID,
        data: UserCreate,
    ) -> UserResponse:
        user = await user_service.update(user_id, data)
        return UserResponse.model_validate(user)
