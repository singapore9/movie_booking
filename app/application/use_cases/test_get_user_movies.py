from collections.abc import Iterable
from unittest.mock import AsyncMock

import pytest

from app.application.dto import (
    GetUserMoviesRequestDTO,
    GetUserMoviesResponseDTO,
    MovieDTO,
)
from app.application.use_cases.get_user_movies import GetUserMoviesUseCase
from app.domain.entities import Movie


@pytest.fixture
def saved_movie_repository(
    repository_user_movies: Iterable[Movie],
) -> AsyncMock:
    _saved_movie_repository = AsyncMock()
    _saved_movie_repository.get_by_user_id.return_value = repository_user_movies
    return _saved_movie_repository


@pytest.fixture
def use_case(
    saved_movie_repository: AsyncMock,
) -> GetUserMoviesUseCase:
    return GetUserMoviesUseCase(
        saved_movie_repository=saved_movie_repository,
    )


@pytest.fixture
def get_user_movies_request_dto() -> GetUserMoviesRequestDTO:
    return GetUserMoviesRequestDTO(
        user_id=10,
    )


class TestExecute:
    @pytest.mark.anyio
    @pytest.mark.parametrize(
        ["repository_user_movies", "user_movies_response_dto"],
        (
            (
                [
                    Movie(id=3, title="Movie Lego", year=2025),
                    Movie(id=4, title="Movie Lego 2", year=2026),
                ],
                GetUserMoviesResponseDTO(
                    movies=[
                        MovieDTO(id=3, title="Movie Lego", year=2025),
                        MovieDTO(id=4, title="Movie Lego 2", year=2026),
                    ]
                ),
            ),
            (
                [
                    Movie(id=4, title="Movie Lego 2", year=2026),
                ],
                GetUserMoviesResponseDTO(
                    movies=[
                        MovieDTO(id=4, title="Movie Lego 2", year=2026),
                    ]
                ),
            ),
            (
                [],
                GetUserMoviesResponseDTO(movies=[]),
            ),
        ),
    )
    async def test_get_user_movies(
        self,
        use_case: GetUserMoviesUseCase,
        saved_movie_repository: AsyncMock,
        get_user_movies_request_dto: GetUserMoviesRequestDTO,
        repository_user_movies: Iterable[Movie],
        user_movies_response_dto: GetUserMoviesResponseDTO,
    ) -> None:
        response = await use_case.execute(get_user_movies_request_dto)

        saved_movie_repository.get_by_user_id.assert_awaited_once_with(
            get_user_movies_request_dto.user_id,
        )
        assert response == user_movies_response_dto
