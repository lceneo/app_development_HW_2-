import json
from datetime import timedelta
from uuid import UUID

import redis
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
    def __init__(
        self, redis_client: redis.Redis, product_repository: ProductRepository
    ):
        self.product_repository = product_repository
        self.redis_client = redis_client

    async def get_by_id(self, product_id: UUID) -> Product | None:
        return await self._get_by_id_cached(product_id)

    async def _get_by_id_cached(self, product_id: UUID) -> Product | None:
        cache_key = f"product:{product_id}"
        cached_data = self.redis_client.get(cache_key)
        if cached_data:
            product_data = json.loads(cached_data)
            product = Product(**product_data)
            return product
        product = await self.product_repository.get_by_id(product_id)
        self.redis_client.setex(
            cache_key, timedelta(hours=1), json.dumps(product.to_dict())
        )
        return product

    async def get_all(self, page: int = 1, count: int = 10):
        return await self.product_repository.get_all(page, count)

    async def create(self, data: ProductCreate) -> Product:
        return await self.product_repository.create(data)

    async def update(self, product_id: UUID, data: ProductUpdate) -> Product:
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise NotFoundException(f"Product with ID {product_id} not found")
        updated_product = await self.product_repository.update(product_id, data)
        cache_key = f"product:{product_id}"
        cached_data = self.redis_client.get(cache_key)
        if cached_data:
            self.redis_client.setex(
                cache_key, timedelta(hours=1), json.dumps(updated_product.to_dict())
            )
        return updated_product

    async def delete(self, product_id: UUID) -> None:
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise NotFoundException(f"Product with ID {product_id} not found")

        await self.product_repository.delete(product_id)
