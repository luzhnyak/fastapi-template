import hashlib


def gavatar(email, size):
    gravatar_url = (
        "https://www.gravatar.com/avatar/"
        + hashlib.md5(email.lower().encode("utf-8")).hexdigest()
        + f"?d=robohash&s={str(size)}"
    )

    return gravatar_url
