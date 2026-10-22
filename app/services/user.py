from starlette.concurrency import run_in_threadpool

from app.core.exceptions import BadRequestException, ConflictException, NotFoundException
from app.core.passwords import hash_password
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.schemas.user import SignUpRequest, UsersListResponse, UserUpdateRequest
from app.services.base import BaseService


class UserService(BaseService):
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, user_data: SignUpRequest) -> User:
        email = str(user_data.email).lower()
        if await self.user_repo.find_one(email=email):
            raise ConflictException("User with this email already exists")
        password = await run_in_threadpool(hash_password, user_data.password)
        return await self.user_repo.add_one(
            {"name": user_data.name, "email": email, "password": password}
        )

    async def get_users(self, skip: int = 0, limit: int = 10) -> UsersListResponse:
        return UsersListResponse(
            items=await self.user_repo.find_many(skip=skip, limit=limit),
            total=await self.user_repo.count_all(),
            page=skip // limit + 1,
            per_page=limit,
        )

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.user_repo.find_one(id=user_id)

    async def get_user_by_id_or_404(self, id: int) -> User:
        user = await self.get_user_by_id(id)
        if user is None:
            raise NotFoundException(f"User with id {id} not found")
        return user

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.user_repo.find_one(email=email.lower())

    async def get_user_by_google_id(self, google_id: str) -> User | None:
        return await self.user_repo.find_one(google_id=google_id)

    async def bind_google_id(self, user_id: int, google_id: str) -> User:
        return await self.user_repo.edit_one(user_id, {"google_id": google_id})

    async def update_user(self, user_id: int, data: UserUpdateRequest, current_user: User) -> User:
        self._check_permission(current_user)
        await self.get_user_by_id_or_404(user_id)
        update_data = data.model_dump(exclude_none=True)
        if not update_data:
            raise BadRequestException("No fields provided for update")
        if "password" in update_data:
            update_data["password"] = await run_in_threadpool(
                hash_password, update_data["password"]
            )
        return await self.user_repo.edit_one(user_id, update_data)

    async def delete_user(self, id: int, current_user: User) -> User:
        self._check_permission(current_user)
        await self.get_user_by_id_or_404(id)
        return await self.user_repo.delete_one(id)
