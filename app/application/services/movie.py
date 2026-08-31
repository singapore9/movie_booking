from app.domain.entities import Movie
from app.domain.exceptions import MovieNotFoundError
from app.domain.repositories import MovieRepository


class MovieService:
    def __init__(
        self,
        movie_repository: MovieRepository,
    ):
        self.movie_repository = movie_repository

    async def get_movie(self, movie_id: int) -> Movie | None:
        movie = await self.movie_repository.get_by_id(movie_id)

        if movie is None:
            raise MovieNotFoundError()
        return movie
