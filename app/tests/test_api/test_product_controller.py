import pytest
from uuid import uuid4
from unittest.mock import AsyncMock
from litestar.testing import create_test_client
from litestar.di import Provide
from app.API.modules.product_module.product_controller import ProductController
from app.API.modules.product_module.DTO.responses.get_product_response_dto import ProductResponse
from app.services.product_service import ProductService


@pytest.fixture
def fake_product():
    return {
        "id": uuid4(),
        "name": "Test Product",
        "price": 10.0,
        "stock_quantity": 5,
    }


def test_get_product_by_id(fake_product):
    mock_product_service = AsyncMock(spec=ProductService)
    mock_product_service.get_by_id.return_value = fake_product

    with create_test_client(
            route_handlers=[ProductController],
            dependencies={"product_service": Provide(lambda: mock_product_service)}
    ) as client:
        response = client.get(f"/products/{fake_product['id']}")

    assert response.status_code == 200
    assert response.json() == ProductResponse.model_validate(fake_product).model_dump(mode="json")
    mock_product_service.get_by_id.assert_called_once_with(fake_product["id"])


def test_create_product(fake_product):
    mock_service = AsyncMock(spec=ProductService)
    mock_service.create.return_value = fake_product

    dto = {"name": "X", "price": 10.5, "stock_quantity": 3}

    with create_test_client(
            route_handlers=[ProductController],
            dependencies={"product_service": Provide(lambda: mock_service)}
    ) as client:
        response = client.post("/products", json=dto)

    assert response.status_code == 201
    assert response.json() == ProductResponse.model_validate(fake_product).model_dump(mode="json")
    mock_service.create.assert_called_once()


def test_update_product(fake_product):
    mock_service = AsyncMock(spec=ProductService)
    mock_service.update.return_value = fake_product

    with create_test_client(
            route_handlers=[ProductController],
            dependencies={"product_service": Provide(lambda: mock_service)}
    ) as client:
        response = client.put(
            f"/products/{fake_product['id']}",
            json={"name": "New", "price": 20.0, "stock_quantity": 99}
        )

    assert response.status_code == 200
    assert response.json() == ProductResponse.model_validate(fake_product).model_dump(mode="json")
    mock_service.update.assert_called_once()


def test_delete_product(fake_product):
    mock_service = AsyncMock(spec=ProductService)
    mock_service.delete.return_value = None

    with create_test_client(
            route_handlers=[ProductController],
            dependencies={"product_service": Provide(lambda: mock_service)}
    ) as client:
        response = client.delete(f"/products/{fake_product['id']}")

    assert response.status_code == 204
    mock_service.delete.assert_called_once_with(fake_product["id"])
