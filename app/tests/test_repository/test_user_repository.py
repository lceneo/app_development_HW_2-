import pytest

from app.API.modules.user_module.DTO.requests.user_create_request_dto import UserCreate
from app.API.modules.user_module.DTO.requests.user_update_request_dto import UserUpdate
from app.repositories.user_repository import UserRepository


class TestUserRepository:
    @pytest.mark.asyncio
    async def test_create_user(self, user_repository: UserRepository):
        """Тест создания пользователя в репозитории"""
        user_data = UserCreate(
            email="test@example.com",
            username="john_doe",
            first_name="John",
            last_name="Doe",
        )
        user = await user_repository.create(user_data)

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.username == "john_doe"

    @pytest.mark.asyncio
    async def test_update_user(self, user_repository: UserRepository):
        """Тест обновления пользователя"""
        user = await user_repository.create(
            UserCreate(
                email="update@example.com",
                username="test",
                first_name="Original",
                last_name="Name",
            )
        )

        updated_user = await user_repository.update(
            user.id, UserUpdate(first_name="Updated")
        )

        assert updated_user.username == "test"
        assert updated_user.first_name == "Updated"
        assert updated_user.last_name == "Name"

    @pytest.mark.asyncio
    async def test_delete_user(self, user_repository: UserRepository):
        """Тест обновления пользователя"""
        user = await user_repository.create(
            UserCreate(
                email="user_to_delete@example.com",
                username="test",
                first_name="Original",
                last_name="Name",
            )
        )
        created_user = await user_repository.get_by_id(user.id)
        assert created_user is not None
        await user_repository.delete(user.id)
        deleted_user = await user_repository.get_by_id(user.id)
        assert deleted_user is None

    @pytest.mark.asyncio
    async def test_get_all_users_with_pagination(self, user_repository: UserRepository):
        for i in range(15):
            await user_repository.create(
                UserCreate(
                    email=f"user{i}@example.com",
                    username=f"user{i}",
                    first_name=f"First{i}",
                    last_name=f"Last{i}",
                )
            )

        # Получаем первую страницу (10)
        users_page_1, total = await user_repository.get_all(page=1, count=10)

        assert total == 15
        assert len(users_page_1) == 10
        assert users_page_1[0].email == "user0@example.com"
        assert users_page_1[-1].email == "user9@example.com"

        # Получаем вторую страницу (оставшиеся 5)
        users_page_2, total2 = await user_repository.get_all(page=2, count=10)

        assert total2 == 15
        assert len(users_page_2) == 5
        assert users_page_2[0].email == "user10@example.com"
        assert users_page_2[-1].email == "user14@example.com"
