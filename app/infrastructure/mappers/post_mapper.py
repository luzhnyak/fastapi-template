from app.domain.entities.post import Post
from app.infrastructure.mappers.base import BaseMapper
from app.domain.entities.post import Post, PostStats
from app.infrastructure.models.post import PostModel


class PostMapper(BaseMapper[PostModel, Post]):
    def to_entity(self, model: PostModel) -> Post:
        return Post(
            id=model.id,
            name=model.name,
            slug=model.slug,
            content=model.content,
            image=model.image,
            thumbnail=model.thumbnail,
            video=model.video,
            ena=model.ena,
            is_gallery=model.is_gallery,
            created_at=model.created_at,
            updated_at=model.updated_at,
            user_id=model.user_id,
            categories=model.categories,
            stats=(
                PostStats(
                    article_id=model.stats.article_id,
                    comments_count=model.stats.comments_count,
                    views=model.stats.views,
                )
                if model.stats
                else None
            ),
        )

    def to_model_dict(self, entity: Post) -> dict:
        return {
            "name": entity.name,
            "slug": entity.slug,
            "content": entity.content,
            "image": entity.image,
            "thumbnail": entity.thumbnail,
            "video": entity.video,
            "ena": entity.ena,
            "is_gallery": entity.is_gallery,
            "user_id": entity.user_id,
        }
