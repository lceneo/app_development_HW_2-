from uuid import uuid4

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.API.modules.order_module.DTO.requests.order_create_request_dto import (
    OrderCreate,
)
from app.API.modules.order_module.DTO.requests.order_update_request_dto import (
    OrderUpdate,
)
from sql_schemas import Order, OrderProduct


class OrderRepository:
    def __init__(self, db_session: AsyncSession, user_repository, product_repository):
        self.session = db_session
        self.user_repository = user_repository
        self.product_repository = product_repository

    async def create(self, order_data: OrderCreate) -> Order:
        # --- получаем пользователя через user_repo (как в тестах с моками)
        user = await self.user_repository.get_by_id(order_data.user_id)
        if not user:
            raise ValueError("User does not exist")

        # --- получаем продукты через product_repo (замена SELECT Product)
        products = []
        for pid in order_data.product_ids:
            p = await self.product_repository.get_by_id(pid)
            if not p:
                raise ValueError("Some product_ids do not exist")
            products.append(p)

        order = Order(
            id=uuid4(),
            user_id=order_data.user_id,
            total_amount=sum(p.price for p in products),
        )
        self.session.add(order)

        # --- сохраняем связи заказ–товары
        for product in products:
            op = OrderProduct(order_id=order.id, product_id=product.id)
            self.session.add(op)

        await self.session.commit()
        await self.session.refresh(order)
        await self.session.refresh(order, attribute_names=["products"])
        return order

    async def get_by_id(self, order_id):
        stmt = (
            select(Order)
            .where(Order.id == order_id)
            .options(selectinload(Order.products))
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all(self, page: int = 1, count: int = 10):
        offset = (page - 1) * count

        orders_result = await self.session.execute(
            select(Order)
            .offset(offset)
            .limit(count)
            .options(selectinload(Order.products))
        )
        orders = orders_result.scalars().all()

        total_count_result = await self.session.execute(select(func.count(Order.id)))
        total_count = total_count_result.scalar_one()

        return orders, total_count

    async def update(self, order_id, order_data: OrderUpdate):
        stmt_order = select(Order).where(Order.id == order_id)
        order = (await self.session.execute(stmt_order)).scalar_one_or_none()

        if not order:
            return None

        # --- получаем продукты не через SELECT, а через product_repo
        products = []
        for pid in order_data.product_ids:
            p = await self.product_repository.get_by_id(pid)
            if not p:
                raise ValueError("Some product_ids do not exist")
            products.append(p)

        # очищаем связи
        await self.session.execute(
            delete(OrderProduct).where(OrderProduct.order_id == order_id)
        )

        # создаём новые связи
        for p in products:
            self.session.add(OrderProduct(order_id=order_id, product_id=p.id))

        order.total_amount = sum(p.price for p in products)

        await self.session.commit()
        await self.session.refresh(order, attribute_names=["products"])

        return order

    async def delete(self, order_id):
        order = await self.get_by_id(order_id)
        if not order:
            return False

        await self.session.delete(order)
        await self.session.commit()
        return True
