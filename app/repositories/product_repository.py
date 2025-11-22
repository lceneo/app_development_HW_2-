from uuid import uuid4

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.API.modules.product_module.DTO.requests.product_update_request_dto import (
    ProductUpdate,
)
from sql_schemas import Product


class ProductRepository:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def get_by_id(self, product_id):
        stmt = select(Product).where(Product.id == product_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, page: int = 1, count: int = 10):
        # Вычисляем offset
        offset = (page - 1) * count

        products_result = await self.session.execute(
            select(Product).offset(offset).limit(count)
        )
        products = products_result.scalars().all()

        total_count_result = await self.session.execute(select(func.count(Product.id)))
        total_count = total_count_result.scalar_one()

        return products, total_count

    async def create(self, data):
        product = Product(
            id=uuid4(),
            name=data.name,
            price=data.price,
            stock_quantity=data.stock_quantity,
        )
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def update(self, product_id, update_data: ProductUpdate):
        product = await self.get_by_id(product_id)
        if not product:
            return None

        if update_data.name is not None:
            product.name = update_data.name
        if update_data.price is not None:
            product.price = update_data.price
        if update_data.stock_quantity is not None:
            product.stock_quantity = update_data.stock_quantity
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete(self, product_id):
        product = await self.get_by_id(product_id)
        if not product:
            return False

        await self.session.delete(product)
        await self.session.commit()
        return True
