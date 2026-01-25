from abc import ABC
from app.domain.entities.user import User
from app.domain.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User], ABC):
    pass
