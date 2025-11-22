from uuid import UUID

from litestar import Controller, delete, get, post, put
from litestar.exceptions import NotFoundException
from litestar.params import Parameter

from app.API.modules.order_module.DTO.requests.order_create_request_dto import (
    OrderCreate,
)
from app.API.modules.order_module.DTO.requests.order_update_request_dto import (
    OrderUpdate,
)
from app.API.modules.order_module.DTO.responses.get_order_response_dto import (
    OrderResponse,
)
from app.services.order_service import OrderService


class OrderController(Controller):
    path = "/orders"
    tags = ["Orders"]

    @get("/{order_id:uuid}")
    async def get_order_by_id(
        self,
        order_service: OrderService,
        order_id: UUID,
    ) -> OrderResponse:
        order = await order_service.get_by_id(order_id)
        if not order:
            raise NotFoundException(detail=f"Order with ID {order_id} not found")
        return OrderResponse.model_validate(order)

    @get()
    async def get_all_orders(
        self,
        order_service: OrderService,
        page: int = Parameter(ge=1, default=1, description="Номер страницы"),
        count: int = Parameter(
            ge=1, le=100, default=10, description="Количество записей на странице"
        ),
    ) -> dict:
        orders, total_count = await order_service.get_all(page=page, count=count)
        return {
            "orders": [OrderResponse.model_validate(order) for order in orders],
            "total_count": total_count,
            "page": page,
            "count": count,
            "total_pages": (total_count + count - 1) // count,
        }

    @post()
    async def create_order(
        self,
        order_service: OrderService,
        data: OrderCreate,
    ) -> OrderResponse:
        order = await order_service.create(data)
        return OrderResponse.model_validate(order)

    @delete("/{order_id:uuid}")
    async def delete_order(
        self,
        order_service: OrderService,
        order_id: UUID,
    ) -> None:
        await order_service.delete(order_id)

    @put("/{order_id:uuid}")
    async def update_order(
        self,
        order_service: OrderService,
        order_id: UUID,
        data: OrderUpdate,
    ) -> OrderResponse:
        order = await order_service.update(order_id, data)
        return OrderResponse.model_validate(order)
