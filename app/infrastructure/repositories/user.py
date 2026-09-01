from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import User
from app.domain.repositories import UserRepository
from app.infrastructure.database import UserModel


class SqlAlchemyUserRepositor(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model: UserModel | None = result.scalar_one_or_none()

        return UserModel.to_domain(model) if model else None
