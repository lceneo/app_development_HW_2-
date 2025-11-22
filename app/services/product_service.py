from uuid import UUID

from litestar.exceptions import NotFoundException

from app.API.modules.product_module.DTO.requests.product_create_request_dto import (
    ProductCreate,
)
from app.API.modules.product_module.DTO.requests.product_update_request_dto import (
    ProductUpdate,
)
from app.repositories.product_repository import ProductRepository
from sql_schemas import Product


class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def get_by_id(self, product_id: UUID) -> Product | None:
        return await self.product_repository.get_by_id(product_id)

    async def get_all(self, page: int = 1, count: int = 10):
        return await self.product_repository.get_all(page, count)

    async def create(self, data: ProductCreate) -> Product:
        return await self.product_repository.create(data)

    async def update(self, product_id: UUID, data: ProductUpdate) -> Product:
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise NotFoundException(f"Product with ID {product_id} not found")

        return await self.product_repository.update(product_id, data)

    async def delete(self, product_id: UUID) -> None:
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise NotFoundException(f"Product with ID {product_id} not found")

        await self.product_repository.delete(product_id)
