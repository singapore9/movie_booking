from abc import ABC, abstractmethod
from collections.abc import Iterable

from app.domain.entities import Movie


class SavedMovieRepository(ABC):
    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> Iterable[Movie]: ...

    @abstractmethod
    async def save(self, user_id: int, movie_id: int) -> None: ...

    @abstractmethod
    async def unsave(self, user_id: int, movie_id: int) -> None: ...

    @abstractmethod
    async def exists(self, user_id: int, movie_id: int) -> bool: ...
