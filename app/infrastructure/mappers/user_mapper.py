from app.infrastructure.mappers.base import BaseMapper
from app.domain.entities.user import User
from app.infrastructure.models.user import UserModel


class UserMapper(BaseMapper[UserModel, User]):
    def to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            name=model.name,
            email=model.email,
            password=model.password,
            image=model.image,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def to_model_dict(self, entity: User) -> dict:
        return {
            "name": entity.name,
            "email": entity.email,
            "password": entity.password,
            "image": entity.image,
        }
