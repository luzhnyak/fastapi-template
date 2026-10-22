from app.domain.entities.comment import Comment
from app.infrastructure.mappers.base import BaseMapper
from app.infrastructure.mappers.user_mapper import UserMapper
from app.infrastructure.models.comment import CommentModel


class CommentMapper(BaseMapper[CommentModel, Comment]):
    def to_entity(self, model: CommentModel) -> Comment:
        return Comment(
            id=model.id,
            post_id=model.post_id,
            content=model.content,
            created_at=model.created_at,
            updated_at=model.updated_at,
            user_id=model.user_id,
            user=UserMapper().to_entity(model.user),
        )

    def to_model_dict(self, entity: Comment) -> dict:
        return {key: getattr(entity, key) for key in ("post_id", "content", "user_id")}
