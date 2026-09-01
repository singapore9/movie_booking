from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Movie
from app.domain.repositories import MovieRepository
from app.infrastructure.database import MovieModel


class SqlAlchemyMovieRepository(MovieRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, movie_id: int) -> Movie | None:
        result = await self.session.execute(
            select(MovieModel).where(MovieModel.id == movie_id)
        )
        model: MovieModel | None = result.scalar_one_or_none()

        return MovieModel.to_domain(model) if model else None
