import os

import redis
from litestar import Litestar, get
from litestar.di import Provide
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm.session import sessionmaker

from app.API.modules.order_module.order_controller import OrderController
from app.API.modules.product_module.product_controller import ProductController
from app.API.modules.user_module.user_controller import UserController
from app.repositories import OrderRepository, ProductRepository
from app.repositories.user_repository import UserRepository
from app.services.order_service import OrderService
from app.services.product_service import ProductService
from app.services.user_service import UserService

from .rabbitmq.consumer import start_consumers

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/prod_db"
)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def provide_db_session() -> AsyncSession:
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    return UserRepository(db_session)


async def provide_user_service(
    redis_client: redis.Redis, user_repository: UserRepository
) -> UserService:
    return UserService(redis_client, user_repository)


async def provide_order_repository(
    db_session: AsyncSession,
    user_repository: UserRepository,
    product_repository: ProductRepository,
) -> OrderRepository:
    return OrderRepository(db_session, user_repository, product_repository)


async def provide_order_service(
    order_repository: OrderRepository,
    product_repository: ProductRepository,
    user_repository: UserRepository,
) -> OrderService:
    return OrderService(order_repository, product_repository, user_repository)


async def provide_product_repository(db_session: AsyncSession) -> ProductRepository:
    return ProductRepository(db_session)


async def provide_product_service(
    redis_client: redis.Redis,
    product_repository: ProductRepository,
) -> ProductService:
    return ProductService(redis_client, product_repository)


async def provide_redis_client() -> redis.Redis:
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=6379,
        db=0,
        decode_responses=True,
    )


app = Litestar(
    route_handlers=[UserController, OrderController, ProductController],
    dependencies={
        "db_session": Provide(provide_db_session),
        "user_repository": Provide(provide_user_repository),
        "user_service": Provide(provide_user_service),
        "order_repository": Provide(provide_order_repository),
        "order_service": Provide(provide_order_service),
        "product_repository": Provide(provide_product_repository),
        "product_service": Provide(provide_product_service),
        "redis_client": Provide(provide_redis_client),
    },
    debug=True,
    on_startup=[start_consumers],
)


def start():
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


def run_tests():
    import pytest

    pytest.main([])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
