from abc import ABC
from app.domain.entities.comment import Comment
from app.domain.repositories.base_repository import BaseRepository


class CommentRepository(BaseRepository[Comment], ABC):
    pass
