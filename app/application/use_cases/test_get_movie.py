from unittest.mock import AsyncMock

import pytest

from app.application.dto import GetMovieRequestDTO, GetMovieResponseDTO
from app.application.use_cases.get_movie import GetMovieUseCase
from app.domain.entities import Movie
from app.domain.exceptions import MovieNotFoundError


@pytest.fixture
def movie_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def use_case(
    movie_repository: AsyncMock,
) -> GetMovieUseCase:
    return GetMovieUseCase(
        movie_repository=movie_repository,
    )


@pytest.fixture
def movie() -> Movie:
    return Movie(id=3, title="Movie Lego", year=2025)


@pytest.fixture
def get_movie_request_dto() -> GetMovieRequestDTO:
    return GetMovieRequestDTO(
        movie_id=1,
    )


class TestGetMovie:
    @pytest.mark.anyio
    async def test_returns_movie(
        self,
        use_case: GetMovieUseCase,
        movie_repository: AsyncMock,
        movie: Movie,
    ) -> None:
        movie_repository.get_by_id.return_value = movie

        result = await use_case.get_movie(movie.id)

        assert result == movie
        movie_repository.get_by_id.assert_awaited_once_with(movie.id)

    @pytest.mark.anyio
    async def test_raises_when_movie_not_found(
        self,
        use_case: GetMovieUseCase,
        movie_repository: AsyncMock,
    ) -> None:
        movie_repository.get_by_id.return_value = None

        with pytest.raises(MovieNotFoundError):
            await use_case.get_movie(1)

        movie_repository.get_by_id.assert_awaited_once_with(1)


class TestExecute:
    @pytest.mark.anyio
    async def test_gets_movie(
        self,
        use_case: GetMovieUseCase,
        movie_repository: AsyncMock,
        get_movie_request_dto: GetMovieRequestDTO,
    ) -> None:
        movie_repository.get_by_id.return_value = Movie(
            id=3, title="Movie Lego", year=2025
        )

        result = await use_case.execute(get_movie_request_dto)

        movie_repository.get_by_id.assert_awaited_once_with(
            get_movie_request_dto.movie_id,
        )

        assert result == GetMovieResponseDTO(id=3, title="Movie Lego", year=2025)

    @pytest.mark.anyio
    async def test_does_not_get_when_error_happened(
        self,
        use_case: GetMovieUseCase,
        movie_repository: AsyncMock,
    ) -> None:
        movie_repository.get_by_id.return_value = None

        data = GetMovieRequestDTO(
            movie_id=1,
        )

        with pytest.raises(MovieNotFoundError):
            await use_case.execute(data)
