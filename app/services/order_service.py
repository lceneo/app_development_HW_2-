from uuid import UUID

from litestar.exceptions import NotFoundException

from app.API.modules.order_module.DTO.requests.order_create_request_dto import (
    OrderCreate,
)
from app.API.modules.order_module.DTO.requests.order_update_request_dto import (
    OrderUpdate,
)
from app.repositories import ProductRepository, UserRepository
from app.repositories.order_repository import OrderRepository
from sql_schemas import Order


class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
        product_repository: ProductRepository,
        user_repository: UserRepository,
    ):
        self.order_repository = order_repository

    async def get_by_id(self, order_id: UUID) -> Order | None:
        return await self.order_repository.get_by_id(order_id)

    async def get_all(self, page: int = 1, count: int = 10) -> tuple[list[Order], int]:
        return await self.order_repository.get_all(page=page, count=count)

    async def create(self, order_data: OrderCreate) -> Order:
        return await self.order_repository.create(order_data)

    async def update(self, order_id: UUID, order_data: OrderUpdate) -> Order:
        order = await self.order_repository.get_by_id(order_id)
        if not order:
            raise NotFoundException(detail=f"Order with ID {order_id} not found")

        return await self.order_repository.update(order_id, order_data)

    async def delete(self, order_id: UUID) -> None:
        order = await self.order_repository.get_by_id(order_id)
        if not order:
            raise NotFoundException(detail=f"Order with ID {order_id} not found")

        await self.order_repository.delete(order_id)
