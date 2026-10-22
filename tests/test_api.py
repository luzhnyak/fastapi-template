import pytest
from conftest import headers, register


def test_authentication_and_refresh(client, user):
    assert (
        client.get("/auth/me", headers=headers(user)).json()["user"]["email"] == "user@example.com"
    )
    login = client.post(
        "/auth/login", json={"email": "user@example.com", "password": "a-long-test-password"}
    )
    assert login.status_code == 200
    assert "refresh_token" not in login.json()
    assert client.post("/auth/refresh").status_code == 200
    assert client.post("/auth/logout").status_code == 200
    assert client.post("/auth/refresh").status_code == 401


def test_invalid_credentials(client, user):
    assert (
        client.post(
            "/auth/login", json={"email": "user@example.com", "password": "wrong"}
        ).status_code
        == 401
    )
    assert client.get("/auth/me").status_code == 401
    assert client.get("/auth/me", headers={"Authorization": "Bearer garbage"}).status_code == 401


def test_refresh_token_cannot_authenticate(client, user):
    token = client.cookies.get("refresh_token")
    assert client.get("/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401


def test_access_token_cannot_refresh(client, user):
    client.cookies.set("refresh_token", user["access_token"])
    assert client.post("/auth/refresh").status_code == 401


def test_duplicate_email_and_password_validation(client, user):
    assert (
        client.post(
            "/auth/register",
            json={"name": "Other", "email": "user@example.com", "password": "some-password"},
        ).status_code
        == 409
    )
    assert (
        client.post(
            "/auth/register",
            json={"name": "Other", "email": "other@example.com", "password": "short"},
        ).status_code
        == 422
    )


def test_first_registered_user_is_not_admin(client, user):
    result = client.post(
        "/posts/",
        headers=headers(user),
        json={"name": "Post", "slug": "post", "content": "Text", "category_ids": []},
    )
    assert result.status_code == 403
    assert client.delete(f"/users/{user['user']['id']}", headers=headers(user)).status_code == 403


@pytest.mark.parametrize("path", ["/users/", "/posts/", "/categories/", "/comments/?post_id=1"])
@pytest.mark.parametrize("query", ["limit=0", "limit=101", "skip=-1"])
def test_pagination_bounds(client, path, query):
    separator = "&" if "?" in path else "?"
    assert client.get(path + separator + query).status_code == 422


def test_missing_records_are_404(client):
    for path in [
        "/users/999",
        "/posts/999",
        "/posts/missing/slug",
        "/categories/999",
        "/comments/999",
    ]:
        assert client.get(path).status_code == 404


def test_post_and_category_crud(client, admin):
    auth = headers(admin)
    category = client.post("/categories/", headers=auth, json={"name": "News", "slug": "news"})
    assert category.status_code == 201, category.text
    category_id = category.json()["id"]
    data = {
        "name": "First",
        "slug": "first",
        "content": "<p>Text</p>",
        "category_ids": [category_id],
    }
    post = client.post("/posts/", headers=auth, json=data)
    assert post.status_code == 201, post.text
    post_id = post.json()["id"]
    assert post.json()["categories"][0]["id"] == category_id
    assert post.json()["user_id"] == admin["user"]["id"]
    assert client.get("/posts/first/slug").json()["description"] == "Text"
    assert client.get("/posts/").json()["total"] == 1
    assert (
        client.put(
            f"/posts/{post_id}", headers=auth, json={**data, "name": "Updated", "category_ids": []}
        ).json()["name"]
        == "Updated"
    )
    assert client.get(f"/posts/{post_id}").json()["categories"] == []
    assert client.delete(f"/posts/{post_id}", headers=auth).status_code == 200
    assert client.get(f"/posts/{post_id}").status_code == 404
    assert client.delete(f"/categories/{category_id}", headers=auth).status_code == 200


def test_invalid_category_rolls_back_post(client, admin):
    result = client.post(
        "/posts/",
        headers=headers(admin),
        json={"name": "Post", "slug": "post", "content": "Text", "category_ids": [999]},
    )
    assert result.status_code == 422
    assert client.get("/posts/").json()["total"] == 0


def test_comment_ownership_and_post_cascade(client, admin):
    post = client.post(
        "/posts/",
        headers=headers(admin),
        json={"name": "Post", "slug": "post", "content": "Text", "category_ids": []},
    ).json()
    user = register(client)
    comment = client.post(
        "/comments/",
        headers=headers(user),
        json={"post_id": post["id"], "content": "Hello", "user_id": admin["user"]["id"]},
    )
    assert comment.status_code == 201, comment.text
    comment_id = comment.json()["id"]
    assert comment.json()["user"]["id"] == user["user"]["id"]
    other = register(client, "other@example.com")
    assert (
        client.put(
            f"/comments/{comment_id}", headers=headers(other), json={"content": "Stolen"}
        ).status_code
        == 403
    )
    assert (
        client.put(
            f"/comments/{comment_id}", headers=headers(user), json={"content": "Updated"}
        ).json()["content"]
        == "Updated"
    )
    assert client.get(f"/comments/?post_id={post['id']}").json()["total"] == 1
    assert client.delete(f"/posts/{post['id']}", headers=headers(admin)).status_code == 200
    assert client.get(f"/comments/{comment_id}").status_code == 404


def test_admin_user_crud(client, admin):
    auth = headers(admin)
    created = client.post(
        "/users/",
        headers=auth,
        json={"name": "New", "email": "new@example.com", "password": "a-long-password"},
    )
    assert created.status_code == 201, created.text
    user_id = created.json()["id"]
    assert "password" not in created.json()
    assert (
        client.put(f"/users/{user_id}", headers=auth, json={"name": "Changed"}).json()["name"]
        == "Changed"
    )
    assert client.delete(f"/users/{user_id}", headers=auth).status_code == 200
    assert client.get(f"/users/{user_id}").status_code == 404


def test_optional_auth_providers_are_disabled(client):
    assert client.post("/auth/google", json={"code": "invalid"}).status_code == 503
    assert client.post("/auth/auth0-login", json={"token": "invalid"}).status_code == 503
