from app.application.dto import (
    GetMovieRequestDTO,
    GetMovieResponseDTO,
)
from app.application.services import MovieService
from app.domain.entities import Movie
from app.domain.repositories import MovieRepository


class GetMovieUseCase:
    def __init__(
        self,
        movie_repository: MovieRepository,
    ) -> None:
        self.movie_repository = movie_repository
        self.movie_service = MovieService(movie_repository)

    async def get_movie(self, movie_id: int) -> Movie | None:
        return await self.movie_service.get_movie(movie_id)

    async def execute(self, data: GetMovieRequestDTO) -> GetMovieResponseDTO:
        movie = await self.get_movie(data.movie_id)

        return GetMovieResponseDTO(
            id=movie.id,
            title=movie.title,
            year=movie.year,
        )
