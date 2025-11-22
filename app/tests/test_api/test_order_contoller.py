from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from litestar.di import Provide
from litestar.testing import create_test_client

from app.API.modules.order_module.DTO.responses.get_order_response_dto import (
    OrderResponse,
)
from app.API.modules.order_module.order_controller import OrderController
from app.services.order_service import OrderService


@pytest.fixture
def fake_order():
    return {
        "id": uuid4(),
        "user_id": uuid4(),
        "address_id": uuid4(),
        "total_amount": 100.0,
        "products": [],
        "status": "pending",
    }


def test_get_order_by_id(fake_order):
    mock_service = AsyncMock(spec=OrderService)
    mock_service.get_by_id.return_value = fake_order

    with create_test_client(
        route_handlers=[OrderController],
        dependencies={"order_service": Provide(lambda: mock_service)},
    ) as client:
        response = client.get(f"/orders/{fake_order['id']}")

    assert response.status_code == 200
    assert response.json() == OrderResponse.model_validate(fake_order).model_dump(
        mode="json"
    )
    mock_service.get_by_id.assert_called_once_with(fake_order["id"])


def test_create_order(fake_order):
    mock_service = AsyncMock(spec=OrderService)
    mock_service.create.return_value = fake_order

    dto = {"user_id": str(uuid4()), "product_ids": []}

    with create_test_client(
        route_handlers=[OrderController],
        dependencies={"order_service": Provide(lambda: mock_service)},
    ) as client:
        response = client.post("/orders", json=dto)

    assert response.status_code == 201
    assert response.json() == OrderResponse.model_validate(fake_order).model_dump(
        mode="json"
    )
    mock_service.create.assert_called_once()


def test_update_order(fake_order):
    mock_service = AsyncMock(spec=OrderService)
    mock_service.update.return_value = fake_order

    with create_test_client(
        route_handlers=[OrderController],
        dependencies={"order_service": Provide(lambda: mock_service)},
    ) as client:
        response = client.put(f"/orders/{fake_order['id']}", json={"product_ids": []})

    assert response.status_code == 200
    assert response.json() == OrderResponse.model_validate(fake_order).model_dump(
        mode="json"
    )
    mock_service.update.assert_called_once()


def test_delete_order(fake_order):
    mock_service = AsyncMock(spec=OrderService)
    mock_service.delete.return_value = None

    with create_test_client(
        route_handlers=[OrderController],
        dependencies={"order_service": Provide(lambda: mock_service)},
    ) as client:
        response = client.delete(f"/orders/{fake_order['id']}")

    assert response.status_code == 204
    mock_service.delete.assert_called_once_with(fake_order["id"])
