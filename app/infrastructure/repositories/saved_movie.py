from collections.abc import Iterable

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Movie
from app.domain.repositories import SavedMovieRepository
from app.infrastructure.database import MovieModel, SavedMovieModel


class SqlAlchemySavedMovieRepository(SavedMovieRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user_id(self, user_id: int) -> Iterable[Movie]:
        result = await self.session.execute(
            select(MovieModel)
            .join(
                SavedMovieModel,
                SavedMovieModel.movie_id == MovieModel.id,
            )
            .where(
                SavedMovieModel.user_id == user_id,
            )
        )
        models: Iterable[MovieModel] = result.scalars().all()
        return [MovieModel.to_domain(model) for model in models]

    async def save(self, user_id: int, movie_id: int) -> None:
        saved_movie = SavedMovieModel(
            user_id=user_id,
            movie_id=movie_id,
        )

        self.session.add(saved_movie)
        await self.session.flush()

    async def unsave(self, user_id: int, movie_id: int) -> None:
        stmt = delete(SavedMovieModel).where(
            SavedMovieModel.user_id == user_id,
            SavedMovieModel.movie_id == movie_id,
        )

        await self.session.execute(stmt)
        await self.session.flush()

    async def exists(self, user_id: int, movie_id: int) -> bool:
        result = await self.session.execute(
            select(SavedMovieModel)
            .where(
                SavedMovieModel.user_id == user_id,
                SavedMovieModel.movie_id == movie_id,
            )
            .limit(1)
        )
        model: SavedMovieModel | None = result.scalar_one_or_none()

        return bool(model)
