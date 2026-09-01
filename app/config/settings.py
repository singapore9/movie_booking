from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MOVIE_BOOKING__",
        env_file=".env",
    )

    DATABASE_URL: str
    DEBUG: bool = False


settings = Settings()
