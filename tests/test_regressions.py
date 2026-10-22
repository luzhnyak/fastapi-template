import importlib
import os
import subprocess
import sys
from pathlib import Path

from conftest import headers, register
from jose import jwt


def test_all_modules_import():
    import app

    for path in Path(app.__path__[0]).rglob("*.py"):
        module = ".".join(path.relative_to(Path(app.__path__[0]).parent).with_suffix("").parts)
        importlib.import_module(module)


def test_secret_key_is_required():
    env = {key: value for key, value in os.environ.items() if key != "SECRET_KEY"}
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from app.core.config import AppSettings; AppSettings(_env_file=None)",
        ],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "SECRET_KEY" in result.stderr


def test_database_constraints_return_conflict_and_rollback(client, admin):
    auth = headers(admin)
    data = {"name": "First", "slug": "same", "content": "Text", "category_ids": []}
    assert client.post("/posts/", headers=auth, json=data).status_code == 201
    duplicate = client.post("/posts/", headers=auth, json=data)
    assert duplicate.status_code == 409
    assert "INSERT" not in duplicate.text
    assert client.get("/posts/").json()["total"] == 1
    assert client.post("/posts/", headers=auth, json={**data, "slug": "second"}).status_code == 201


def test_comment_counts_and_deletion(client, admin):
    post = client.post(
        "/posts/", headers=headers(admin), json={"name": "Post", "slug": "post", "content": "Text"}
    ).json()
    user = register(client)
    comment = client.post(
        "/comments/", headers=headers(user), json={"post_id": post["id"], "content": "Hello"}
    ).json()
    assert client.get(f"/posts/{post['id']}").json()["stats"]["comments_count"] == 1
    assert client.delete(f"/comments/{comment['id']}", headers=headers(user)).status_code == 200
    assert client.get(f"/posts/{post['id']}").json()["stats"]["comments_count"] == 0


def test_deleting_user_updates_comment_counts(client, admin):
    post = client.post(
        "/posts/", headers=headers(admin), json={"name": "Post", "slug": "post", "content": "Text"}
    ).json()
    user = register(client)
    assert (
        client.post(
            "/comments/", headers=headers(user), json={"post_id": post["id"], "content": "Hello"}
        ).status_code
        == 201
    )
    assert client.get(f"/posts/{post['id']}").json()["stats"]["comments_count"] == 1
    assert client.delete(f"/users/{user['user']['id']}", headers=headers(admin)).status_code == 200
    assert client.get(f"/posts/{post['id']}").json()["stats"]["comments_count"] == 0
    assert client.get(f"/comments/?post_id={post['id']}").json()["items"] == []


def test_deleted_user_tokens_cannot_authenticate_recreated_email(client, admin):
    user = register(client)
    refresh = client.cookies.get("refresh_token")
    assert client.delete(f"/users/{user['user']['id']}", headers=headers(admin)).status_code == 200
    register(client)
    assert client.get("/auth/me", headers=headers(user)).status_code == 401
    client.cookies.clear()
    client.cookies.set("refresh_token", refresh)
    assert client.post("/auth/refresh").status_code == 401


def test_inactive_user_tokens_are_rejected(client, user):
    async def deactivate():
        from sqlalchemy import update

        from app.infrastructure.models.user import UserModel

        async with client.app.state.session_factory.begin() as session:
            await session.execute(
                update(UserModel).where(UserModel.id == user["user"]["id"]).values(is_active=False)
            )

    client.portal.call(deactivate)
    assert client.get("/auth/me", headers=headers(user)).status_code == 401
    assert client.post("/auth/refresh").status_code == 401
    assert (
        client.post(
            "/auth/login", json={"email": "user@example.com", "password": "a-long-test-password"}
        ).status_code
        == 401
    )


def test_missing_and_expired_exp_claims_are_rejected(client, user):
    from app.core.config import settings

    for extra in ({}, {"exp": 1}):
        token = jwt.encode(
            {"sub": str(user["user"]["id"]), "type": "access", "iat": 1, **extra},
            settings.app.SECRET_KEY,
        )
        assert (
            client.get("/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401
        )


def test_google_login_creates_unpredictable_password(client, monkeypatch):
    async def google_info(code):
        return {
            "id": "google-123",
            "email": "google@example.com",
            "name": "Google User",
            "verified_email": True,
        }

    monkeypatch.setattr("app.services.auth.get_user_info", google_info)
    response = client.post("/auth/google", json={"code": "code"})
    assert response.status_code == 200, response.text
    assert (
        client.post(
            "/auth/login", json={"email": "google@example.com", "password": "google@example.com"}
        ).status_code
        == 401
    )


def test_google_rejects_unverified_email(client, monkeypatch):
    import httpx

    from app.core.config import settings

    for field in ("OAUTH_CLIENT_ID", "OAUTH_SECRET", "OAUTH_REDIRECT_URI"):
        monkeypatch.setattr(settings.app, field, "test")
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            200,
            json={"access_token": "token"}
            if request.method == "POST"
            else {"email": "unverified@example.com", "verified_email": False},
        )
    )
    real_client = httpx.AsyncClient
    monkeypatch.setattr(
        "app.utils.oauth_google.httpx.AsyncClient",
        lambda **kwargs: real_client(transport=transport, **kwargs),
    )
    assert client.post("/auth/google", json={"code": "code"}).status_code == 401


def test_category_update_and_permissions(client, admin):
    auth = headers(admin)
    category = client.post(
        "/categories/", headers=auth, json={"name": "Before", "slug": "category"}
    ).json()
    assert (
        client.put(f"/categories/{category['id']}", headers=auth, json={"name": "After"}).json()[
            "name"
        ]
        == "After"
    )
    user = register(client)
    assert client.delete(f"/categories/{category['id']}", headers=headers(user)).status_code == 403
    assert (
        client.put(
            f"/users/{admin['user']['id']}",
            headers=headers(user),
            json={"password": "new-password"},
        ).status_code
        == 403
    )


def test_create_admin_command(client):
    async def create():
        from app.cli import create_admin

        await create_admin("Admin", "admin@example.com", "admin-password")

    client.portal.call(create)
    login = client.post(
        "/auth/login", json={"email": "admin@example.com", "password": "admin-password"}
    )
    assert login.status_code == 200
    assert (
        client.post(
            "/categories/",
            headers=headers(login.json()),
            json={"name": "Category", "slug": "category"},
        ).status_code
        == 201
    )


def test_admin_can_have_id_other_than_one(client, user):
    async def create():
        from app.cli import create_admin

        await create_admin("Second Admin", "second-admin@example.com", "admin-password")

    client.portal.call(create)
    login = client.post(
        "/auth/login", json={"email": "second-admin@example.com", "password": "admin-password"}
    )
    assert login.status_code == 200
    assert login.json()["user"]["id"] != 1
    assert (
        client.post(
            "/categories/",
            headers=headers(login.json()),
            json={"name": "Category", "slug": "category"},
        ).status_code
        == 201
    )


def test_legacy_password_hashes_still_authenticate(client, user):
    from passlib.hash import sha256_crypt

    legacy_hash = sha256_crypt.hash("legacy-password")

    async def replace():
        from sqlalchemy import update

        from app.infrastructure.models.user import UserModel

        async with client.app.state.session_factory.begin() as session:
            await session.execute(
                update(UserModel)
                .where(UserModel.id == user["user"]["id"])
                .values(password=legacy_hash)
            )

    client.portal.call(replace)
    assert (
        client.post(
            "/auth/login", json={"email": "user@example.com", "password": "legacy-password"}
        ).status_code
        == 200
    )


def test_google_does_not_link_to_unverified_local_registration(client, user, monkeypatch):
    async def info(code):
        return {"id": "google-123", "email": "user@example.com", "verified_email": True}

    monkeypatch.setattr("app.services.auth.get_user_info", info)
    response = client.post("/auth/google", json={"code": "code"})
    assert response.status_code == 409


def test_google_binding_supports_repeat_login(client, monkeypatch):
    async def info(code):
        return {
            "id": "google-123",
            "email": "google@example.com",
            "name": "Google",
            "verified_email": True,
        }

    monkeypatch.setattr("app.services.auth.get_user_info", info)
    first = client.post("/auth/google", json={"code": "first"})
    second = client.post("/auth/google", json={"code": "second"})
    assert first.status_code == second.status_code == 200
    assert first.json()["user"]["id"] == second.json()["user"]["id"]
    assert client.get("/users/").json()["total"] == 1


def test_google_rejects_missing_provider_id(client, monkeypatch):
    import httpx

    from app.core.config import settings

    for field in ("OAUTH_CLIENT_ID", "OAUTH_SECRET", "OAUTH_REDIRECT_URI"):
        monkeypatch.setattr(settings.app, field, "test")
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            200,
            json={"access_token": "token"}
            if request.method == "POST"
            else {"email": "verified@example.com", "verified_email": True},
        )
    )
    real_client = httpx.AsyncClient
    monkeypatch.setattr(
        "app.utils.oauth_google.httpx.AsyncClient",
        lambda **kwargs: real_client(transport=transport, **kwargs),
    )
    assert client.post("/auth/google", json={"code": "code"}).status_code == 401


def test_logout_clears_legacy_root_cookie(client, user):
    client.cookies.set(
        "refresh_token", client.cookies.get("refresh_token"), domain="testserver.local", path="/"
    )
    assert client.post("/auth/logout").status_code == 200
    assert client.post("/auth/refresh").status_code == 401


def test_oversized_sqlite_ids_are_validation_errors(client, admin):
    maximum = 2**63
    for path in (
        f"/posts/{maximum}",
        f"/users/{maximum}",
        f"/categories/{maximum}",
        f"/comments/{maximum}",
        f"/comments/?post_id={maximum}",
        f"/posts/?skip={maximum}",
    ):
        assert client.get(path).status_code == 422
    data = {"name": "Post", "slug": "post", "content": "Text", "category_ids": [maximum]}
    assert client.post("/posts/", headers=headers(admin), json=data).status_code == 422
