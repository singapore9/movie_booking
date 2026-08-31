from unittest.mock import AsyncMock

import pytest

from app.application.services import MovieService
from app.domain.entities import Movie
from app.domain.exceptions import MovieNotFoundError


@pytest.fixture
def movie_repository(
    movie: Movie,
) -> AsyncMock:
    _movie_repository = AsyncMock()
    _movie_repository.get_by_id.return_value = movie
    return _movie_repository


@pytest.fixture
def service(
    movie_repository: AsyncMock,
) -> MovieService:
    return MovieService(
        movie_repository=movie_repository,
    )


@pytest.fixture
def movie() -> Movie:
    return Movie(id=3, title="Movie Lego", year=2025)


class TestGetMovie:
    @pytest.mark.anyio
    async def test_returns_movie(
        self,
        service: MovieService,
        movie_repository: AsyncMock,
        movie: Movie,
    ) -> None:
        result = await service.get_movie(movie.id)

        assert result == movie
        movie_repository.get_by_id.assert_awaited_once_with(movie.id)

    @pytest.mark.anyio
    async def test_raises_when_movie_not_found(
        self,
        service: MovieService,
        movie_repository: AsyncMock,
    ) -> None:
        movie_repository.get_by_id.return_value = None

        with pytest.raises(MovieNotFoundError):
            await service.get_movie(1)

        movie_repository.get_by_id.assert_awaited_once_with(1)
