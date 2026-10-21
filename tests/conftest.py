import os

import pytest
from fastapi.testclient import TestClient

os.environ["SECRET_KEY"] = "test-secret-" * 4


@pytest.fixture
def client(tmp_path, monkeypatch):
    from app.core.config import settings
    from app.main import create_app

    monkeypatch.setattr(settings.db, "SQLITE_DB_PATH", str(tmp_path / "test.sqlite3"))
    monkeypatch.setattr(settings.app, "COOKIE_SECURE", False)
    for field in ("OAUTH_CLIENT_ID", "OAUTH_SECRET", "OAUTH_REDIRECT_URI"):
        monkeypatch.setattr(settings.app, field, None)
    with TestClient(create_app()) as client:
        yield client


def register(client, email="user@example.com", password="a-long-test-password"):
    response = client.post(
        "/auth/register", json={"name": "Test User", "email": email, "password": password}
    )
    assert response.status_code == 201, response.text
    return response.json()


@pytest.fixture
def user(client):
    return register(client)


@pytest.fixture
def admin(client):
    result = register(client, "admin@example.com")

    async def promote():
        from sqlalchemy import update

        from app.infrastructure.models.user import UserModel

        async with client.app.state.session_factory.begin() as session:
            await session.execute(
                update(UserModel).where(UserModel.id == result["user"]["id"]).values(role="admin")
            )

    client.portal.call(promote)
    return result


def headers(auth):
    return {"Authorization": f"Bearer {auth['access_token']}"}
