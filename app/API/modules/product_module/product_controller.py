from uuid import UUID
from litestar import Controller, get, post, put, delete
from litestar.exceptions import NotFoundException
from litestar.params import Parameter
from app.API.modules.product_module.DTO.requests.product_create_request_dto import ProductCreate
from app.API.modules.product_module.DTO.requests.product_update_request_dto import ProductUpdate
from app.API.modules.product_module.DTO.responses.get_product_response_dto import ProductResponse
from app.services.product_service import ProductService


class ProductController(Controller):
    path = "/products"
    tags = ["Products"]

    @get("/{product_id:uuid}")
    async def get_product_by_id(
        self,
        product_service: ProductService,
        product_id: UUID,
    ) -> ProductResponse:
        product = await product_service.get_by_id(product_id)
        if not product:
            raise NotFoundException(f"Product with ID {product_id} not found")
        return ProductResponse.model_validate(product)

    @get()
    async def get_all_products(
        self,
        product_service: ProductService,
        page: int = Parameter(ge=1, default=1),
        count: int = Parameter(ge=1, le=100, default=10),
    ) -> dict:
        products, total_count = await product_service.get_all(page, count)
        return {
            "products": [ProductResponse.model_validate(p) for p in products],
            "total_count": total_count,
            "page": page,
            "count": count,
            "total_pages": (total_count + count - 1) // count,
        }

    @post()
    async def create_product(
        self,
        product_service: ProductService,
        data: ProductCreate,
    ) -> ProductResponse:
        product = await product_service.create(data)
        return ProductResponse.model_validate(product)

    @put("/{product_id:uuid}")
    async def update_product(
        self,
        product_service: ProductService,
        product_id: UUID,
        data: ProductUpdate,
    ) -> ProductResponse:
        product = await product_service.update(product_id, data)
        return ProductResponse.model_validate(product)

    @delete("/{product_id:uuid}")
    async def delete_product(
        self,
        product_service: ProductService,
        product_id: UUID,
    ) -> None:
        await product_service.delete(product_id)
