from unittest.mock import AsyncMock

import pytest

from app.application.dto import UnsaveMovieDTO
from app.application.use_cases.unsave_movie import UnsaveMovieUseCase
from app.domain.entities import Movie
from app.domain.exceptions import (
    MovieNotFoundError,
    SavedMovieNotFoundError,
)


@pytest.fixture
def movie_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def saved_movie_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def use_case(
    movie_repository: AsyncMock,
    saved_movie_repository: AsyncMock,
) -> UnsaveMovieUseCase:
    return UnsaveMovieUseCase(
        movie_repository=movie_repository,
        saved_movie_repository=saved_movie_repository,
    )


@pytest.fixture
def movie():
    return Movie(id=3, title="Movie Lego", year=2025)


@pytest.fixture
def unsave_movie_dto() -> UnsaveMovieDTO:
    return UnsaveMovieDTO(
        user_id=10,
        movie_id=1,
    )


class TestGetMovie:
    @pytest.mark.anyio
    async def test_returns_movie(
        self,
        use_case: UnsaveMovieUseCase,
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
        use_case: UnsaveMovieUseCase,
        movie_repository: AsyncMock,
    ) -> None:
        movie_repository.get_by_id.return_value = None

        with pytest.raises(MovieNotFoundError):
            await use_case.get_movie(1)

        movie_repository.get_by_id.assert_awaited_once_with(1)


class TestRaiseIfSavedMovieDoesNotExist:
    @pytest.mark.anyio
    async def test_does_not_raise_when_movie_already_saved(
        self,
        use_case: UnsaveMovieUseCase,
        saved_movie_repository: AsyncMock,
    ) -> None:
        saved_movie_repository.exists.return_value = True

        await use_case.raise_if_saved_movie_not_exists(10, 1)

        saved_movie_repository.exists.assert_awaited_once_with(10, 1)

    @pytest.mark.anyio
    async def test_raises_when_saved_movie_not_found(
        self,
        use_case: UnsaveMovieUseCase,
        saved_movie_repository: AsyncMock,
    ) -> None:
        saved_movie_repository.exists.return_value = False

        with pytest.raises(SavedMovieNotFoundError):
            await use_case.raise_if_saved_movie_not_exists(10, 1)

        saved_movie_repository.exists.assert_awaited_once_with(10, 1)


class TestExecute:
    @pytest.mark.anyio
    async def test_unsaves_movie(
        self,
        use_case: UnsaveMovieUseCase,
        movie_repository: AsyncMock,
        saved_movie_repository: AsyncMock,
        movie: Movie,
        unsave_movie_dto: UnsaveMovieDTO,
    ) -> None:
        movie_repository.get_by_id.return_value = movie
        saved_movie_repository.exists.return_value = True

        await use_case.execute(unsave_movie_dto)

        movie_repository.get_by_id.assert_awaited_once_with(
            unsave_movie_dto.movie_id,
        )
        saved_movie_repository.exists.assert_awaited_once_with(
            unsave_movie_dto.user_id,
            unsave_movie_dto.movie_id,
        )
        saved_movie_repository.unsave.assert_awaited_once_with(
            unsave_movie_dto.user_id,
            unsave_movie_dto.movie_id,
        )

    @pytest.mark.anyio
    @pytest.mark.parametrize(
        ("movie", "exists", "expected_exception"),
        [
            (
                None,
                True,
                MovieNotFoundError,
            ),
            (
                Movie(id=1, title="Movie1", year=2020),
                False,
                SavedMovieNotFoundError,
            ),
        ],
    )
    async def test_does_not_unsave_when_error_happened(
        self,
        use_case: UnsaveMovieUseCase,
        movie_repository: AsyncMock,
        saved_movie_repository: AsyncMock,
        movie: Movie | None,
        exists: bool,
        expected_exception: type[Exception],
    ) -> None:
        movie_repository.get_by_id.return_value = movie
        saved_movie_repository.exists.return_value = exists

        data = UnsaveMovieDTO(
            user_id=10,
            movie_id=1,
        )

        with pytest.raises(expected_exception):
            await use_case.execute(data)

        saved_movie_repository.unsave.assert_not_awaited()
