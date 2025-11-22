from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from litestar.di import Provide
from litestar.testing import create_test_client

from app.API.modules.user_module.DTO.requests.user_create_request_dto import UserCreate
from app.API.modules.user_module.DTO.responses.get_user_response_dto import UserResponse
from app.API.modules.user_module.user_controller import UserController
from app.services.user_service import UserService


@pytest.fixture
def fake_user():
    return {
        "id": uuid4(),
        "email": "a@b.com",
        "username": "test_user",
        "first_name": "A",
        "last_name": "B",
        "created_at": "2024-01-01T00:00:00",
    }


def test_get_user_by_id(fake_user):
    mock_user_service = AsyncMock(spec=UserService)
    mock_user_service.get_by_id.return_value = fake_user

    with create_test_client(
        route_handlers=[UserController],
        dependencies={"user_service": Provide(lambda: mock_user_service)},
    ) as client:
        response = client.get(f"/users/{fake_user['id']}")

    assert response.status_code == 200
    assert response.json() == UserResponse.model_validate(fake_user).model_dump(
        mode="json"
    )
    mock_user_service.get_by_id.assert_called_once_with(fake_user["id"])


def test_create_user(fake_user):
    mock_user_service = AsyncMock(spec=UserService)
    mock_user_service.create.return_value = fake_user

    payload = {
        "email": "x@y.com",
        "username": "userx",
        "first_name": "X",
        "last_name": "Y",
    }

    with create_test_client(
        route_handlers=[UserController],
        dependencies={"user_service": Provide(lambda: mock_user_service)},
    ) as client:
        response = client.post("/users", json=payload)

    assert response.status_code == 201
    assert response.json() == UserResponse.model_validate(fake_user).model_dump(
        mode="json"
    )

    mock_user_service.create.assert_called_once()
    called_arg = mock_user_service.create.call_args.args[0]
    assert isinstance(called_arg, UserCreate)
    assert called_arg.email == payload["email"]


def test_update_user(fake_user):
    mock_user_service = AsyncMock(spec=UserService)
    mock_user_service.update.return_value = fake_user

    payload = {
        "email": "new@a.com",
        "username": "new_u",
        "first_name": "N",
        "last_name": "K",
    }

    uid = fake_user["id"]

    with create_test_client(
        route_handlers=[UserController],
        dependencies={"user_service": Provide(lambda: mock_user_service)},
    ) as client:
        response = client.put(f"/users/{uid}", json=payload)

    assert response.status_code == 200

    mock_user_service.update.assert_called_once()
    called_user_id, called_update_dto = mock_user_service.update.call_args.args

    assert called_user_id == uid
    assert called_update_dto.email == payload["email"]


def test_delete_user(fake_user):
    mock_user_service = AsyncMock(spec=UserService)
    mock_user_service.delete.return_value = None

    uid = fake_user["id"]

    with create_test_client(
        route_handlers=[UserController],
        dependencies={"user_service": Provide(lambda: mock_user_service)},
    ) as client:
        response = client.delete(f"/users/{uid}")

    assert response.status_code == 204
    mock_user_service.delete.assert_called_once_with(uid)
