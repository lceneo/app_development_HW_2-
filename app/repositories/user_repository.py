from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.API.modules.user_module.DTO.requests.user_create_request_dto import UserCreate
from app.API.modules.user_module.DTO.requests.user_update_request_dto import UserUpdate
from sql_schemas import User


class UserRepository:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, page: int = 1, count: int = 10) -> tuple[list[User], int]:
        # Вычисляем offset
        offset = (page - 1) * count

        # Получаем пользователей для текущей страницы
        users_result = await self.session.execute(
            select(User)
            .offset(offset)
            .limit(count)
        )
        users = users_result.scalars().all()

        # Получаем общее количество пользователей
        total_count_result = await self.session.execute(
            select(func.count(User.id))
        )
        total_count = total_count_result.scalar_one()

        return users, total_count

    async def create(self, user_data: UserCreate) -> User:
        user_dict = {
            'username': user_data.username,
            'email': user_data.email,
            'description': user_data.description
        }
        user = User(**user_dict)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user_id: UUID, user_data: UserUpdate) -> User | None:
        user = await self.get_by_id(user_id)
        if not user:
            return
        if user_data.username is not None:
            user.username = user_data.username
        if user_data.email is not None:
            user.email = user_data.email
        if user_data.description is not None:
            user.description = user_data.description
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: UUID) -> None:
        user = await self.get_by_id(user_id)
        if user:
            await self.session.delete(user)
            await self.session.commit()
