from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.mappers.user_mapper import UserMapper
from app.infrastructure.models.user import UserModel
from app.infrastructure.repositories.sqlalchemy.base import SQLAlchemyRepository


class SQLAlchemyUserRepository(
    SQLAlchemyRepository[UserModel, User],
    UserRepository,
):
    model = UserModel
    mapper = UserMapper()
