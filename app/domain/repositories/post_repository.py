from abc import ABC
from app.domain.entities.post import Post
from app.domain.repositories.base_repository import BaseRepository


class PostRepository(BaseRepository[Post], ABC):
    pass
