from dataclasses import dataclass
from datetime import datetime
from typing import List


from app.utils.avatar import gavatar


@dataclass(kw_only=True)
class UserMinimal:
    id: int
    name: str
    image: str | None = None
    email: str
    is_google_user: bool = False

    @property
    def avatar(self):
        if self.image:
            return self.image
        return gavatar(self.email, 128)


@dataclass(kw_only=True)
class User:
    id: int
    name: str
    email: str
    password: str | None = None
    image: str | None = None
    google_id: str | None = None
    fb_id: str | None = None
    tg_id: str | None = None
    tg_username: str | None = None
    role_id: int | None = None
    ip: str | None = None
    ban: bool | None = None
    token: str | None = None
    lastvisit_date: str | None = None
    created_at: datetime
    updated_at: datetime

    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @property
    def avatar(self):
        if self.image:
            return self.image
        return gavatar(self.email, 128)

        # if self.fb_id is not None:
        #     avatar = "https://graph.facebook.com/v3.0/" + \
        #         self.fb_id + "/picture?height=128&width=128"
        # elif self.google_id is not None:
        #     try:
        #         jsonpic = requests.get(
        #             "http://picasaweb.google.com/data/entry/api/user/"
        #             + self.google_id
        #             + "?alt=json"
        #         ).json()
        #         avatar = jsonpic["entry"]["gphoto$thumbnail"]["$t"]
        #         avatar = avatar.replace("s64-c", "s128-c")
        #     except:
        #         avatar = gavatar(self.email, 128)
        # else:
        #     avatar = gavatar(self.email, 128)
        # return avatar


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
