from app.core.exceptions import ForbiddenException


class BaseService:
    __abstract__ = True

    def _check_permission(self, current_user_id: int) -> None:
        if current_user_id != 1:
            raise ForbiddenException("You are not authorized to perform this action")
