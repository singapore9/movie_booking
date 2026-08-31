from abc import ABC, abstractmethod

from app.domain.entities import Movie


class MovieRepository(ABC):
    @abstractmethod
    async def get_by_id(self, movie_id: int) -> Movie | None: ...
