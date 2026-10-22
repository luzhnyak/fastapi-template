from app.domain.entities.user import User
from app.infrastructure.mappers.base import BaseMapper
from app.infrastructure.models.user import UserModel


class UserMapper(BaseMapper[UserModel, User]):
    def to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            name=model.name,
            email=model.email,
            password=model.password,
            avatar=model.avatar,
            role=model.role,
            google_id=model.google_id,
            is_active=model.is_active,
            lastvisit_date=model.lastvisit_date,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def to_model_dict(self, entity: User) -> dict:
        return {
            key: getattr(entity, key)
            for key in ("name", "email", "password", "avatar", "role", "is_active", "google_id")
        }
