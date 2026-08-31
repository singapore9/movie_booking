from unittest.mock import AsyncMock

import pytest

from app.application.dto import SaveMovieDTO
from app.application.use_cases.save_movie import SaveMovieUseCase
from app.domain.entities import Movie
from app.domain.exceptions import (
    MovieAlreadySavedError,
    MovieNotFoundError,
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
) -> SaveMovieUseCase:
    return SaveMovieUseCase(
        movie_repository=movie_repository,
        saved_movie_repository=saved_movie_repository,
    )


@pytest.fixture
def movie():
    return Movie(id=3, title="Movie Lego", year=2025)


@pytest.fixture
def save_movie_dto() -> SaveMovieDTO:
    return SaveMovieDTO(
        user_id=10,
        movie_id=1,
    )


class TestGetMovie:
    @pytest.mark.anyio
    async def test_returns_movie(
        self,
        use_case: SaveMovieUseCase,
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
        use_case: SaveMovieUseCase,
        movie_repository: AsyncMock,
    ) -> None:
        movie_repository.get_by_id.return_value = None

        with pytest.raises(MovieNotFoundError):
            await use_case.get_movie(1)

        movie_repository.get_by_id.assert_awaited_once_with(1)


class TestRaiseIfSavedMovieExists:
    @pytest.mark.anyio
    async def test_does_not_raise_when_movie_not_saved(
        self,
        use_case: SaveMovieUseCase,
        saved_movie_repository: AsyncMock,
    ) -> None:
        saved_movie_repository.exists.return_value = False

        await use_case.raise_if_saved_movie_exists(10, 1)

        saved_movie_repository.exists.assert_awaited_once_with(10, 1)

    @pytest.mark.anyio
    async def test_raises_when_movie_already_saved(
        self,
        use_case: SaveMovieUseCase,
        saved_movie_repository: AsyncMock,
    ) -> None:
        saved_movie_repository.exists.return_value = True

        with pytest.raises(MovieAlreadySavedError):
            await use_case.raise_if_saved_movie_exists(10, 1)

        saved_movie_repository.exists.assert_awaited_once_with(10, 1)


class TestExecute:
    @pytest.mark.anyio
    async def test_saves_movie(
        self,
        use_case: SaveMovieUseCase,
        movie_repository: AsyncMock,
        saved_movie_repository: AsyncMock,
        movie: Movie,
        save_movie_dto: SaveMovieDTO,
    ) -> None:
        movie_repository.get_by_id.return_value = movie
        saved_movie_repository.exists.return_value = False

        await use_case.execute(save_movie_dto)

        movie_repository.get_by_id.assert_awaited_once_with(
            save_movie_dto.movie_id,
        )
        saved_movie_repository.exists.assert_awaited_once_with(
            save_movie_dto.user_id,
            save_movie_dto.movie_id,
        )
        saved_movie_repository.save.assert_awaited_once_with(
            save_movie_dto.user_id,
            save_movie_dto.movie_id,
        )

    @pytest.mark.anyio
    @pytest.mark.parametrize(
        ("movie", "exists", "expected_exception"),
        [
            (
                None,
                False,
                MovieNotFoundError,
            ),
            (
                Movie(id=1, title="Movie1", year=2020),
                True,
                MovieAlreadySavedError,
            ),
        ],
    )
    async def test_does_not_save_when_error_happened(
        self,
        use_case: SaveMovieUseCase,
        movie_repository: AsyncMock,
        saved_movie_repository: AsyncMock,
        movie: Movie | None,
        exists: bool,
        expected_exception: type[Exception],
    ) -> None:
        movie_repository.get_by_id.return_value = movie
        saved_movie_repository.exists.return_value = exists

        data = SaveMovieDTO(
            user_id=10,
            movie_id=1,
        )

        with pytest.raises(expected_exception):
            await use_case.execute(data)

        saved_movie_repository.save.assert_not_awaited()
