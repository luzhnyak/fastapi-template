from pydantic import BaseModel, ConfigDict, EmailStr
from typing import List


class SignUpRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class UserUpdateRequest(BaseModel):
    name: str | None = None
    password: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    id: int | None = None
    name: str
    # email: EmailStr | None = None
    avatar: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UsersListResponse(BaseModel):
    items: List[UserResponse]
    total: int
    page: int
    per_page: int


class RelationshipUserResponse(BaseModel):
    id: int
    name: str
    avatar: str
    is_google_user: bool
