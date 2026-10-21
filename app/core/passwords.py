from passlib.hash import sha256_crypt
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed: str | None) -> bool:
    if not hashed:
        return False
    try:
        if hashed.startswith("$5$"):
            return sha256_crypt.verify(password, hashed)
        return password_hash.verify(password, hashed)
    except (ValueError, TypeError):
        return False
