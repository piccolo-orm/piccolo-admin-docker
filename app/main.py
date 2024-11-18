import asyncio
import os

from hypercorn import Config
from hypercorn.asyncio import serve
from piccolo.engine import PostgresEngine
from piccolo.table import create_db_tables
from piccolo.table_reflection import TableStorage
from piccolo_admin.endpoints import TableConfig, create_admin
from piccolo_api.encryption.providers import XChaCha20Provider
from piccolo_api.mfa.authenticator.provider import AuthenticatorProvider
from tables import AuthenticatorSecret, Sessions, User
from utils import additional_config


async def main():
    # Create auth tables in separate Sqlite DB
    await create_db_tables(
        *[User, Sessions, AuthenticatorSecret],
        if_not_exists=True,
    )
    # Create a admin user in separate Sqlite DB
    if not await User.exists().where(User.email == os.environ["EMAIL"]):
        user = User(
            username=os.environ["USERNAME"],
            password=os.environ["PASSWORD"],
            email=os.environ["EMAIL"],
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

    # additional configuration of admin tables
    if additional_config.tables is not None:
        admin_tables = []
        for config in additional_config.tables:
            for table in storage.tables.values():
                if table._meta.tablename == config.table_name:
                    # visible columns
                    try:
                        visible_columns = [
                            column
                            for column in table._meta.columns
                            if column._meta.name in config.visible_columns
                        ]
                    except TypeError:
                        visible_columns = table._meta.columns
                    # visible filters
                    try:
                        visible_filters = [
                            column
                            for column in table._meta.columns
                            if column._meta.name in config.visible_filters
                        ]
                    except TypeError:
                        visible_filters = table._meta.columns
                    # rich text columns
                    rich_text_columns = [
                        column
                        for column in table._meta.columns
                        if column._meta.name == config.rich_text_columns
                    ]
                    # link column
                    try:
                        link_column = [
                            column
                            for column in table._meta.columns
                            if column._meta.name == config.link_column
                        ][0]
                    except IndexError:
                        link_column = None
                    # menu_group
                    menu_group = config.menu_group

                    admin_tables.append(
                        TableConfig(
                            table_class=table,
                            visible_columns=visible_columns,
                            visible_filters=visible_filters,
                            rich_text_columns=rich_text_columns,
                            link_column=link_column,
                            menu_group=menu_group,
                        )
                    )
    else:
        admin_tables = storage.tables.values()

    for table in admin_tables:
        if isinstance(table, TableConfig):
            table.table_class._meta._db = db
        else:
            table._meta._db = db

    # create new encription key for MFA
    encryption_key = XChaCha20Provider.get_new_key()

    app = create_admin(
        admin_tables,
        auth_table=User,
        session_table=Sessions,
        auto_include_related=False,
        mfa_providers=[
            AuthenticatorProvider(
                encryption_provider=XChaCha20Provider(
                    encryption_key=encryption_key,
                ),
                secret_table=AuthenticatorSecret,
            ),
        ],
        sidebar_links=additional_config.sidebar_links or {},
    )

    # Server
    class CustomConfig(Config):
        use_reloader = True
        accesslog = "-"

    await serve(app, CustomConfig())


if __name__ == "__main__":
    asyncio.run(main())
