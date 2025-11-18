import pytest

from app.API.modules.product_module.DTO.requests.product_create_request_dto import ProductCreate
from app.API.modules.product_module.DTO.requests.product_update_request_dto import ProductUpdate
from app.repositories.product_repository import ProductRepository


class TestProductRepository:

    @pytest.mark.asyncio
    async def test_create_product(self, product_repository: ProductRepository):
        product = await product_repository.create(
            ProductCreate(
                name="Protein",
                price=12.5,
                stock_quantity=100,
            )
        )

        assert product.id is not None
        assert product.name == "Protein"
        assert product.price == 12.5
        assert product.stock_quantity == 100

    @pytest.mark.asyncio
    async def test_update_product(self, product_repository: ProductRepository):
        p = await product_repository.create(
            ProductCreate(
                name="Creatine",
                price=20.0,
                stock_quantity=50
            )
        )

        updated_p = await product_repository.update(
            p.id,
            ProductUpdate(
                price=25.0,
                stock_quantity=60
            )
        )

        assert updated_p.name == "Creatine"
        assert updated_p.price == 25.0
        assert updated_p.stock_quantity == 60

    @pytest.mark.asyncio
    async def test_delete_product(self, product_repository: ProductRepository):
        p = await product_repository.create(
            ProductCreate(
                name="BCAA",
                price=15.0,
                stock_quantity=75
            )
        )

        exists_before = await product_repository.get_by_id(p.id)
        assert exists_before is not None

        await product_repository.delete(p.id)
        exists_after = await product_repository.get_by_id(p.id)

        assert exists_after is None

    @pytest.mark.asyncio
    async def test_get_all_products_with_pagination(self, product_repository: ProductRepository):
        for i in range(15):
            await product_repository.create(
                ProductCreate(
                    name=f"Product{i}",
                    price=i + 1,
                    stock_quantity=10 + i,
                )
            )

        page1, total = await product_repository.get_all(page=1, count=10)
        assert total == 15
        assert len(page1) == 10
        assert page1[0].name == "Product0"
        assert page1[-1].name == "Product9"

        page2, total2 = await product_repository.get_all(page=2, count=10)
        assert total2 == 15
        assert len(page2) == 5
        assert page2[0].name == "Product10"
        assert page2[-1].name == "Product14"
