import asyncio

from app.application.dto import UnsaveMovieDTO
from app.domain.entities import Movie
from app.domain.exceptions import MovieNotFoundError, SavedMovieNotFoundError
from app.domain.repositories import MovieRepository, SavedMovieRepository


class UnsaveMovieUseCase:
    def __init__(
        self,
        movie_repository: MovieRepository,
        saved_movie_repository: SavedMovieRepository,
    ) -> None:
        self.movie_repository = movie_repository
        self.saved_movie_repository = saved_movie_repository

    async def get_movie(self, movie_id: int) -> Movie | None:
        movie = await self.movie_repository.get_by_id(movie_id)

        if movie is None:
            raise MovieNotFoundError()

        return movie

    async def raise_if_saved_movie_not_exists(
        self, user_id: int, movie_id: int
    ) -> None:
        if not await self.saved_movie_repository.exists(user_id, movie_id):
            raise SavedMovieNotFoundError()

    async def execute(self, data: UnsaveMovieDTO) -> None:
        await asyncio.gather(
            *(
                self.get_movie(data.movie_id),
                self.raise_if_saved_movie_not_exists(data.user_id, data.movie_id),
            ),
        )

        return await self.saved_movie_repository.unsave(data.user_id, data.movie_id)
