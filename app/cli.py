import argparse
import asyncio
from getpass import getpass

from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.config import settings
from app.core.exceptions import ConflictException
from app.infrastructure.db.database import init_db, make_engine
from app.infrastructure.repositories.sqlalchemy.user import SQLAlchemyUserRepository
from app.schemas.auth import RegisterRequest
from app.services.user import UserService


async def create_admin(name: str, email: str, password: str) -> None:
    data = RegisterRequest(name=name, email=email, password=password)
    engine = make_engine(settings.db.DATABASE_URL)
    try:
        if settings.app.INIT_DB:
            await init_db(engine)
        factory = async_sessionmaker(engine, expire_on_commit=False)
        async with factory.begin() as session:
            repo = SQLAlchemyUserRepository(session)
            user = await UserService(repo).create_user(data)
            await repo.edit_one(user.id, {"role": "admin"})
    finally:
        await engine.dispose()


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage the FastAPI template")
    commands = parser.add_subparsers(dest="command", required=True)
    admin = commands.add_parser("create-admin", help="Create an administrator")
    admin.add_argument("--name", required=True)
    admin.add_argument("--email", required=True)
    args = parser.parse_args()
    password = getpass("Password (8+ characters): ")
    if password != getpass("Repeat password: "):
        parser.error("Passwords do not match")
    try:
        asyncio.run(create_admin(args.name, args.email, password))
    except ValidationError:
        parser.error("Invalid name, email or password (8–1024 characters)")
    except ConflictException:
        parser.error("User with this email already exists")
    except SQLAlchemyError:
        parser.error("Database operation failed")
    print("Administrator created")


if __name__ == "__main__":
    main()
