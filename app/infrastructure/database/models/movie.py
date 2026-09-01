from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.entities import Movie
from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models import SavedMovieModel


class MovieModel(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)

    saved_by: Mapped[list["SavedMovieModel"]] = relationship(
        back_populates="movie",
    )

    @staticmethod
    def to_domain(model: "MovieModel") -> Movie:
        return Movie(
            id=model.id,
            title=model.title,
            year=model.year,
        )

    @staticmethod
    def to_model(movie: Movie) -> "MovieModel":
        return MovieModel(
            id=movie.id,
            title=movie.title,
            year=movie.year,
        )
