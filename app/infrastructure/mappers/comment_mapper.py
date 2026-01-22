from app.domain.entities.user import UserMinimal
from app.infrastructure.mappers.base import BaseMapper
from app.domain.entities.comment import Comment
from app.infrastructure.models.comment import CommentModel


class CommentMapper(BaseMapper[CommentModel, Comment]):
    def to_entity(self, model: CommentModel) -> Comment:
        return Comment(
            id=model.id,
            article_id=model.article_id,
            comment=model.comment,
            created_at=model.created_at,
            updated_at=model.updated_at,
            table_name=model.table_name,
            user_id=model.user_id,
            user=(
                UserMinimal(
                    id=model.user.id,
                    email=model.user.email,
                    name=model.user.name,
                    is_google_user=False,
                )
                if model.user
                else None
            ),
        )

    def to_model_dict(self, entity: Comment) -> dict:
        return {
            "article_id": entity.article_id,
            "comment": entity.comment,
            "table_name": entity.table_name,
            "user_id": entity.user_id,
        }
