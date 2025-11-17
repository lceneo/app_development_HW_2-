import os

from litestar import Litestar, get
from litestar.di import Provide
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm.session import sessionmaker

from app.API.modules.user_module.user_controller import UserController
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

DATABASE_URL = os.getenv("DATABASE_URL", 'postgresql+asyncpg://postgres:postgres@localhost:5432/prod_db')

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

async def provide_user_service(user_repository: UserRepository) -> UserService:
    return UserService(user_repository)

app = Litestar(
    route_handlers=[UserController],
    dependencies={
        "db_session": Provide(provide_db_session),
        "user_repository": Provide(provide_user_repository),
        "user_service": Provide(provide_user_service),
    },
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
