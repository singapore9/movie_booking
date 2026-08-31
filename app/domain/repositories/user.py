from abc import ABC, abstractmethod

from app.domain.entities import User


class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None: ...
