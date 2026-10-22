from app.domain.entities.post import Post, PostStats
from app.infrastructure.mappers.base import BaseMapper
from app.infrastructure.mappers.category_mapper import CategoryMapper
from app.infrastructure.models.post import PostModel


class PostMapper(BaseMapper[PostModel, Post]):
    def to_entity(self, model: PostModel) -> Post:
        return Post(
            id=model.id,
            name=model.name,
            slug=model.slug,
            content=model.content,
            image=model.image,
            video=model.video,
            user_id=model.user_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            categories=[CategoryMapper().to_entity(category) for category in model.categories],
            stats=PostStats(
                post_id=model.stats.post_id,
                comments_count=model.stats.comments_count,
                views=model.stats.views,
            )
            if model.stats
            else None,
        )

    def to_model_dict(self, entity: Post) -> dict:
        return {
            key: getattr(entity, key)
            for key in ("name", "slug", "content", "image", "video", "user_id")
        }
