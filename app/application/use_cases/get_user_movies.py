from app.application.dto import (
    GetUserMoviesRequestDTO,
    GetUserMoviesResponseDTO,
    MovieDTO,
)
from app.domain.repositories import SavedMovieRepository


class GetUserMoviesUseCase:
    def __init__(
        self,
        saved_movie_repository: SavedMovieRepository,
    ) -> None:
        self.saved_movie_repository = saved_movie_repository

    async def execute(self, data: GetUserMoviesRequestDTO) -> GetUserMoviesResponseDTO:
        user_movies = await self.saved_movie_repository.get_by_user_id(data.user_id)
        return GetUserMoviesResponseDTO(
            movies=[
                MovieDTO(
                    id=movie.id,
                    title=movie.title,
                    year=movie.year,
                )
                for movie in user_movies
            ]
        )
