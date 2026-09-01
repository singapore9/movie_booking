from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.entities import User
from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models import SavedMovieModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False)

    saved_movies: Mapped[list["SavedMovieModel"]] = relationship(
        back_populates="user",
    )

    @staticmethod
    def to_domain(model: "UserModel") -> User:
        return User(
            id=model.id,
            username=model.username,
        )

    @staticmethod
    def to_model(user: User) -> "UserModel":
        return UserModel(
            id=user.id,
            username=user.username,
        )
