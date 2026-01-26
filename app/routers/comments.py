from app.api.dependencies import get_comment_service
from app.schemas.comment import CommentListResponse
from fastapi import APIRouter, Depends


from app.services.comment import CommentService


router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/", response_model=CommentListResponse)
async def get_comments_by_article_id(
    table_name: str,
    article_id: int,
    service: CommentService = Depends(get_comment_service),
):
    comments = await service.get_comments_by_article_id(
        table_name=table_name, article_id=article_id
    )
    # print("comments", comments)
    return comments

    # reviews = []
    # if path == "places":
    #     place = session.query(PlaceModel).get(article_id)
    #     reviews = place.reviews

    # if not comments and not reviews:
    #     JSON = {"message": "Comments not found", "data": []}
    #     return jsonify(JSON)

    # data = []

    # for comment in comments:
    #     id = comment.id
    #     created_at = comment.created_at
    #     text = comment.comment
    #     table_name = comment.table_name
    #     user_id = comment.user_id
    #     user_name = comment.users.name
    #     user_avatar = comment.users.avatar
    #     article_id = comment.article_id

    #     commentJson = {
    #         "id": id,
    #         "created_at": created_at,
    #         "text": text,
    #         "table_name": table_name,
    #         "user_id": user_id,
    #         "user_name": user_name,
    #         "user_avatar": user_avatar,
    #         "article_id": article_id,
    #     }

    #     data.append(commentJson)

    # if reviews:
    #     for comment in reviews:
    #         id = comment["time"]
    #         created_at = datetime.fromtimestamp(comment["time"]).strftime(
    #             "%Y-%m-%d %I:%M"
    #         )
    #         text = comment["text"]
    #         table_name = path
    #         user_id = None
    #         user_name = comment["author_name"]
    #         user_avatar = comment["profile_photo_url"]
    #         article_id = article_id

    #         commentJson = {
    #             "id": id,
    #             "created_at": created_at,
    #             "text": text,
    #             "table_name": table_name,
    #             "user_id": user_id,
    #             "user_name": user_name,
    #             "user_avatar": user_avatar,
    #             "article_id": article_id,
    #         }

    #         data.append(commentJson)

    # data = sorted(data, key=lambda x: x["created_at"], reverse=True)
    # data = data[(page - 1) * PER_PAGE : (page - 1) * PER_PAGE + PER_PAGE]

    # mainJSON = {
    #     "page": page,
    #     "per_page": PER_PAGE,
    #     "total": len(data),
    #     "total_page": math.ceil(len(data) / PER_PAGE),
    #     "data": data,
    # }

    # return jsonify(mainJSON)
