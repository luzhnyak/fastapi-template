from passlib.hash import sha256_crypt


from app.core.exceptions import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)
from app.domain.entities.user import User
from app.infrastructure.repositories.sqlalchemy.user import UserRepository
from app.schemas.auth import RegisterRequest
from app.schemas.user import (
    UserResponse,
    UserUpdateRequest,
    UsersListResponse,
)


from app.services.base import BaseService


class UserService(BaseService):
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_password_hash(self, password: str) -> str:
        return sha256_crypt.encrypt(password)

    async def create_user(self, user_data: RegisterRequest) -> User:
        user = await self.user_repo.find_one(email=user_data.email)
        if user:
            raise ConflictException("User with this email already exists")

        hashed_password = self.get_password_hash(user_data.password)
        new_user_data = {
            "name": user_data.name,
            "email": user_data.email,
            "password": hashed_password,
        }
        new_user = await self.user_repo.add_one(new_user_data)

        return new_user

    async def get_users(self, skip: int = 0, limit: int = 10) -> UsersListResponse:
        total = await self.user_repo.count_all()
        page = (skip // limit) + 1
        users = await self.user_repo.find_many(skip=skip, limit=limit)
        return UsersListResponse(
            items=users,
            total=total,
            page=page,
            per_page=limit,
        )

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.user_repo.find_one(id=user_id)
        if not user:
            raise None
        return user

    async def get_user_by_id_or_404(self, id: int) -> User:
        user = await self.user_repo.find_one(id=id)
        if not user:
            raise NotFoundException(f"User with id {id} not found")
        return user

    async def get_user_by_email(self, email: str) -> User | None:
        user = await self.user_repo.find_one(email=email)
        if not user:
            return None
        return user

    async def get_user_by_google_id(self, google_id: int) -> User:
        user = await self.user_repo.find_one(google_id=google_id)
        if not user:
            return None
        return user

    async def update_user(
        self, user_id: int, data: UserUpdateRequest, current_user_id: int
    ) -> UserResponse:
        self._check_permission(current_user_id)
        user = await self.get_user_by_id_or_404(user_id)
        update_data = {}

        if data.name:
            update_data["name"] = data.name
        if data.password:
            update_data["password"] = self.get_password_hash(data.password)

        if not update_data:
            raise BadRequestException("No valid fields provided for update")

        user = await self.user_repo.edit_one(user_id, update_data)
        return user

    async def delete_user(self, id: int, current_user_id: int) -> UserResponse:
        self._check_permission(current_user_id)
        await self.get_user_by_id_or_404(id)
        deleted_user = await self.user_repo.delete_one(id)
        return deleted_user
