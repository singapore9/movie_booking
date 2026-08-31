import asyncio

from app.application.dto import SaveMovieDTO
from app.application.services import MovieService
from app.domain.entities import Movie
from app.domain.exceptions import MovieAlreadySavedError
from app.domain.repositories import MovieRepository, SavedMovieRepository


class SaveMovieUseCase:
    def __init__(
        self,
        movie_repository: MovieRepository,
        saved_movie_repository: SavedMovieRepository,
    ) -> None:
        self.movie_repository = movie_repository
        self.saved_movie_repository = saved_movie_repository
        self.movie_service = MovieService(movie_repository)

    async def get_movie(self, movie_id: int) -> Movie | None:
        return await self.movie_service.get_movie(movie_id)

    async def raise_if_saved_movie_exists(self, user_id: int, movie_id: int) -> None:
        if await self.saved_movie_repository.exists(user_id, movie_id):
            raise MovieAlreadySavedError()

    async def execute(self, data: SaveMovieDTO) -> None:
        await asyncio.gather(
            *(
                self.get_movie(data.movie_id),
                self.raise_if_saved_movie_exists(data.user_id, data.movie_id),
            ),
        )

        return await self.saved_movie_repository.save(data.user_id, data.movie_id)
