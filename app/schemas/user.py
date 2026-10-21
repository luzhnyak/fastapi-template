from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SignUpRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    email: EmailStr
    password: str = Field(min_length=8, max_length=1024)


class SignInRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=1024)


class UserUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    password: str | None = Field(default=None, min_length=8, max_length=1024)


class RelationshipUserResponse(BaseModel):
    id: int
    name: str
    avatar: str | None = None
    model_config = ConfigDict(from_attributes=True)


class UserResponse(RelationshipUserResponse):
    email: EmailStr


class UsersListResponse(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    per_page: int
