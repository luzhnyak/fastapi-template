from dataclasses import dataclass
from datetime import datetime
from typing import List

from app.utils.avatar import gavatar


@dataclass(kw_only=True)
class User:
    id: int
    name: str
    email: str
    password: str | None = None
    avatar: str | None = None
    role: str = "user"
    lastvisit_date: str | None = None
    created_at: datetime
    updated_at: datetime

    @property
    def gavatar(self):
        if self.avatar:
            return self.avatar
        return gavatar(self.email, 128)


@dataclass
class UserList:
    items: List[User]
    total: int
    page: int
    per_page: int


@dataclass(kw_only=True)
class Auth:
    access_token: str
    token_type: str = "Bearer"
    refresh_token: str
    user: User
