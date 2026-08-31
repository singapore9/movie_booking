class BaseDomainError(Exception):
    pass


class MovieNotFoundError(BaseDomainError):
    pass


class MovieAlreadySavedError(BaseDomainError):
    pass
