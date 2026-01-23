from datetime import datetime, timezone
import json
import re
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    NotFoundException,
)

from app.domain.entities.user import User, UserMinimal
from app.infrastructure.repositories.sqlalchemy.comment import CommentRepository
from app.domain.entities.comment import (
    CommentList,
    Comment,
)
from app.infrastructure.repositories.sqlalchemy.place import PlaceRepository
from app.schemas.comment import CommentCreateRequest, CommentUpdateRequest
from app.services.base import BaseService


class CommentService(BaseService):

    def __init__(self, comment_repo: CommentRepository, place_repo: PlaceRepository):
        self.comment_repo = comment_repo
        self.place_repo = place_repo

    async def create_comment(
        self, data: CommentCreateRequest, current_user_id: int
    ) -> Comment:
        self._check_permission(data.user_id, current_user_id)
        new_comment = await self.comment_repo.add_one(data.model_dump())
        return new_comment

    async def get_comments_by_article_id(
        self, table_name: str, article_id: int, skip: int = 0, limit: int = 12
    ) -> CommentList:
        total = await self.comment_repo.count_all(
            table_name=table_name, article_id=article_id
        )
        page = (skip // limit) + 1
        comments = await self.comment_repo.get_comments(
            table_name=table_name, article_id=article_id, skip=skip, limit=limit
        )

        google_comments = []

        if table_name == "places":
            place = await self.place_repo.get_full_place(id=article_id)
            google_comments = []
            try:
                reviews = json.loads(place.google_reviews)
                for review in reviews:
                    time = datetime.fromtimestamp(review["time"], tz=timezone.utc)
                    user_id = 0
                    url = review["author_url"]
                    match = re.search(r"/contrib/(\d+)", url)

                    if match:
                        user_id = match.group(1)

                    text = review["text"]
                    if not text:
                        text = f"{review["rating"]} балів"

                    comment = Comment(
                        id=review["time"],
                        comment=text,
                        table_name="places",
                        article_id=article_id,
                        created_at=time,
                        updated_at=time,
                        user_id=user_id,
                        user=UserMinimal(
                            id=user_id,
                            name=review["author_name"],
                            image=review["profile_photo_url"],
                            email="user@goldfishnet.in.ua",
                            is_google_user=True,
                        ),
                    )

                    google_comments.append(comment)

            except Exception as e:
                print(e)
                reviews = []

        comments = sorted(
            [
                *[comment for comment in comments],
                *google_comments,
            ],
            key=lambda x: x.created_at,
            reverse=True,
        )

        return CommentList(
            items=comments,
            total=total,
            page=page,
            per_page=limit,
        )

    async def get_comments_by_user_id(
        self, user_id: int, skip: int = 0, limit: int = 12
    ) -> CommentList:
        total = await self.comment_repo.count_all(user_id=user_id)
        page = (skip // limit) + 1
        comments = await self.comment_repo.find_many(
            user_id=user_id, skip=skip, limit=limit
        )
        return CommentList(
            items=comments,
            total=total,
            page=page,
            per_page=limit,
        )

    async def get_comment_by_id(self, id: int) -> Comment:
        comment = await self.comment_repo.find_one(id=id)
        if not comment:
            None
        return comment

    async def get_comment_by_id_or_404(self, id: int) -> Comment:
        comment = await self.comment_repo.find_one_with_stats(id=id)
        if not comment:
            raise NotFoundException(f"Comment with id {id} not found")
        return comment

    async def update_comment(
        self, id: int, data: CommentUpdateRequest, current_user_id: int
    ) -> Comment:
        self._check_permission(current_user_id)
        self.get_comment_by_id_or_404(id)
        updated_comment = await self.comment_repo.edit_one(id, data)
        return updated_comment

    async def delete_comment(self, id: int, current_user_id: int) -> Comment:
        self._check_permission(current_user_id)
        self.get_comment_by_id_or_404(id)
        delete_comment = await self.comment_repo.delete_one(id=id)
        return delete_comment
