import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4
from app.services.order_service import OrderService
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository


class TestOrderService:

    @pytest.mark.asyncio
    async def test_create_order_success(self):
        """Тест успешного создания заказа"""

        # Мокаем репозитории
        mock_order_repo = AsyncMock(spec=OrderRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)
        mock_user_repo = AsyncMock(spec=UserRepository)

        # Настраиваем мок user
        mock_user_repo.get_by_id.return_value = Mock(
            id=uuid4(),
            email="test@example.com"
        )

        # Настраиваем мок product
        mock_product_repo.get_by_id.return_value = Mock(
            id=uuid4(),
            name="Test Product",
            price=100.0,
            stock_quantity=5
        )

        mock_order_repo.create.return_value = Mock(
            id=uuid4(),
            user_id=mock_user_repo.get_by_id.return_value.id,
            total_amount=200.0,
            status="pending"
        )

        order_service = OrderService(
            order_repository=mock_order_repo,
            product_repository=mock_product_repo,
            user_repository=mock_user_repo
        )

        order_data = {
            "user_id": str(mock_user_repo.get_by_id.return_value.id),
            "product_ids": [str(mock_product_repo.get_by_id.return_value.id)]
        }

        result = await order_service.create(order_data)

        assert result is not None
        assert result.total_amount == 200.0
        mock_order_repo.create.assert_called_once()
