from typing import Annotated

from pydantic import BaseModel


def is_positive(value: int, handler, ctx) -> int:
    if value > 0:
        field_name = ctx.field_name
        raise ValueError(f"{field_name.capitalize()} value should be positive")
    return value


class MovieDTO(BaseModel):
    id: Annotated[int, is_positive]
    title: str
    year: Annotated[int, is_positive]


class GetUserMoviesRequestDTO(BaseModel):
    user_id: Annotated[int, is_positive]


class GetUserMoviesResponseDTO(BaseModel):
    movies: list[MovieDTO]


class SaveMovieDTO(BaseModel):
    user_id: Annotated[int, is_positive]
    movie_id: Annotated[int, is_positive]


class UnsaveMovieDTO(BaseModel):
    user_id: Annotated[int, is_positive]
    movie_id: Annotated[int, is_positive]
