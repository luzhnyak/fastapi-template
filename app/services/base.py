from app.core.exceptions import ForbiddenException
from app.domain.entities.user import User


class BaseService:
    def _check_permission(self, current_user: User) -> None:
        if not current_user.is_active or current_user.role != "admin":
            raise ForbiddenException("Administrator access required")
