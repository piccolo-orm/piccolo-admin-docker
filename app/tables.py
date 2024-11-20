import os

# from pathlib import Path

from piccolo.apps.user.tables import BaseUser
from piccolo.engine.sqlite import SQLiteEngine
from piccolo_api.mfa.authenticator.tables import (
    AuthenticatorSecret as AuthenticatorSecret_,
)
from piccolo_api.session_auth.tables import SessionsBase

# use this if we want the data as a directory and VOLUME /app/data
# try:
#     Path(Path(__file__).parent / "data").mkdir()
# except FileExistsError:
#     pass
# DB_PATH = Path("data").absolute() / "auth.sqlite"
# DB = SQLiteEngine(str(DB_PATH))

DB_PATH = os.path.join(os.path.dirname(__file__), "data")
DB = SQLiteEngine(DB_PATH)


class Sessions(SessionsBase, db=DB):
    pass


class User(BaseUser, tablename="piccolo_user", db=DB):
    pass


class AuthenticatorSecret(AuthenticatorSecret_, db=DB):
    pass
