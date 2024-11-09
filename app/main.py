import asyncio
import os

from dotenv import find_dotenv, load_dotenv
from hypercorn import Config
from hypercorn.asyncio import serve
from piccolo.apps.user.tables import BaseUser
from piccolo.engine import PostgresEngine
from piccolo.engine.sqlite import SQLiteEngine
from piccolo.table import create_db_tables
from piccolo.table_reflection import TableStorage
from piccolo_admin import create_admin
from piccolo_api.encryption.providers import XChaCha20Provider
from piccolo_api.mfa.authenticator.provider import AuthenticatorProvider
from piccolo_api.mfa.authenticator.tables import (
    AuthenticatorSecret as AuthenticatorSecret_,
)
from piccolo_api.session_auth.tables import SessionsBase

DB = SQLiteEngine()


load_dotenv(find_dotenv())


class Sessions(SessionsBase, db=DB):
    pass


class User(BaseUser, tablename="piccolo_user", db=DB):
    pass


class AuthenticatorSecret(AuthenticatorSecret_, db=DB):
    pass


async def main():
    # Create auth tables in separate Sqlite DB
    await create_db_tables(
        *[User, Sessions, AuthenticatorSecret],
        if_not_exists=True,
    )
    # Create a admin user in separate Sqlite DB
    if not await User.exists().where(User.email == "admin@test.com"):
        user = User(
            username=os.environ["USERNAME"],
            password=os.environ["PASSWORD"],
            email="admin@test.com",
            admin=True,
            active=True,
            superuser=True,
        )
        await user.save()

    db = PostgresEngine(
        config={
            "database": os.environ["DB_NAME"],
            "user": os.environ["DB_USER"],
            "password": os.environ["DB_PASSWORD"],
            "host": os.environ["DB_HOST"],
            "port": int(os.environ["DB_PORT"]),
        },
        extensions=tuple(),
    )

    storage = TableStorage(engine=db)
    await storage.reflect(schema_name="public")

    # This tuple IS unique
    # however auto_include_related within
    # create_admin makes it non unique TableConfigs
    found_tables = storage.tables.values()

    for table_class in found_tables:
        table_class._meta._db = db

    app = create_admin(
        found_tables,
        auth_table=User,
        session_table=Sessions,
        auto_include_related=False,
        mfa_providers=[
            AuthenticatorProvider(
                encryption_provider=XChaCha20Provider(
                    encryption_key=os.environb[b"ENCRIPTION_KEY"]
                    .decode("unicode-escape")
                    .encode("latin-1")
                ),
                secret_table=AuthenticatorSecret,
            ),
        ],
    )

    # Server
    class CustomConfig(Config):
        use_reloader = True
        accesslog = "-"

    await serve(app, CustomConfig())


if __name__ == "__main__":
    asyncio.run(main())
