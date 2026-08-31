from app.application.dto import (
    GetMovieRequestDTO,
    GetMovieResponseDTO,
)
from app.domain.entities import Movie
from app.domain.exceptions import MovieNotFoundError
from app.domain.repositories import MovieRepository


class GetMovieUseCase:
    def __init__(
        self,
        movie_repository: MovieRepository,
    ) -> None:
        self.movie_repository = movie_repository

    async def get_movie(self, movie_id: int) -> Movie | None:
        movie = await self.movie_repository.get_by_id(movie_id)

        if movie is None:
            raise MovieNotFoundError()

        return movie

    async def execute(self, data: GetMovieRequestDTO) -> GetMovieResponseDTO:
        movie = await self.get_movie(data.movie_id)

        return GetMovieResponseDTO(
            id=movie.id,
            title=movie.title,
            year=movie.year,
        )
