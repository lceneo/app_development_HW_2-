from uuid import uuid4

import pytest

from app.API.modules.order_module.DTO.requests.order_create_request_dto import (
    OrderCreate,
)
from app.API.modules.order_module.DTO.requests.order_update_request_dto import (
    OrderUpdate,
)
from app.API.modules.product_module.DTO.requests.product_create_request_dto import (
    ProductCreate,
)
from app.API.modules.user_module.DTO.requests.user_create_request_dto import UserCreate
from app.repositories.order_repository import OrderRepository


class TestOrderRepository:

    @pytest.mark.asyncio
    async def test_create_order(
        self, order_repository: OrderRepository, product_repository, user_repository
    ):
        # Создаём пользователя
        user = await user_repository.create(
            UserCreate(
                email="buyer@example.com",
                username="buyer",
                first_name="Buyer",
                last_name="Test",
            )
        )

        # Создаём 2 товара
        p1 = await product_repository.create(
            ProductCreate(name="P1", price=10.0, stock_quantity=5)
        )
        p2 = await product_repository.create(
            ProductCreate(name="P2", price=20.0, stock_quantity=3)
        )

        order = await order_repository.create(
            OrderCreate(
                user_id=user.id,
                product_ids=[p1.id, p2.id],
            )
        )

        assert order.id is not None
        assert order.user_id == user.id
        assert order.total_amount == 30.0  # 10 + 20

        # Проверяем связи
        assert len(order.products) == 2

    @pytest.mark.asyncio
    async def test_update_order(
        self, order_repository, product_repository, user_repository
    ):
        user = await user_repository.create(
            UserCreate(
                email="update_o@example.com",
                username="upd_order",
                first_name="Ord",
                last_name="Upd",
            )
        )

        p1 = await product_repository.create(
            ProductCreate(name="X", price=5.0, stock_quantity=10)
        )
        p2 = await product_repository.create(
            ProductCreate(name="Y", price=7.0, stock_quantity=10)
        )

        order = await order_repository.create(
            OrderCreate(
                user_id=user.id,
                product_ids=[p1.id],
            )
        )

        updated_order = await order_repository.update(
            order.id, OrderUpdate(product_ids=[p1.id, p2.id])
        )

        assert updated_order.total_amount == 12.0
        assert len(updated_order.products) == 2

    @pytest.mark.asyncio
    async def test_get_order_by_id(
        self, order_repository, product_repository, user_repository
    ):
        user = await user_repository.create(
            UserCreate(
                email="one@example.com",
                username="one_user",
                first_name="One",
                last_name="U",
            )
        )

        p = await product_repository.create(
            ProductCreate(name="Z", price=99.0, stock_quantity=1)
        )

        order = await order_repository.create(
            OrderCreate(user_id=user.id, product_ids=[p.id])
        )

        fetched = await order_repository.get_by_id(order.id)

        assert fetched is not None
        assert fetched.id == order.id
        assert fetched.total_amount == 99.0
        assert len(fetched.products) == 1

    @pytest.mark.asyncio
    async def test_delete_order(
        self, order_repository, product_repository, user_repository
    ):
        user = await user_repository.create(
            UserCreate(
                email="del@example.com",
                username="delete_user",
                first_name="Del",
                last_name="U",
            )
        )

        p = await product_repository.create(
            ProductCreate(name="DEL", price=50.0, stock_quantity=1)
        )

        order = await order_repository.create(
            OrderCreate(user_id=user.id, product_ids=[p.id])
        )

        exists_before = await order_repository.get_by_id(order.id)
        assert exists_before is not None

        await order_repository.delete(order.id)

        exists_after = await order_repository.get_by_id(order.id)
        assert exists_after is None

    @pytest.mark.asyncio
    async def test_get_all_orders(
        self, order_repository, product_repository, user_repository
    ):
        user = await user_repository.create(
            UserCreate(
                email="list@example.com",
                username="list_user",
                first_name="List",
                last_name="U",
            )
        )

        p = await product_repository.create(
            ProductCreate(name="ITEM", price=5.0, stock_quantity=10)
        )

        for _ in range(12):
            await order_repository.create(
                OrderCreate(user_id=user.id, product_ids=[p.id])
            )

        page1, total = await order_repository.get_all(page=1, count=10)

        assert total == 12
        assert len(page1) == 10

        page2, total2 = await order_repository.get_all(page=2, count=10)
        assert total2 == 12
        assert len(page2) == 2
