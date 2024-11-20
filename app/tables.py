from pathlib import Path

from piccolo.apps.user.tables import BaseUser
from piccolo.engine.sqlite import SQLiteEngine
from piccolo_api.mfa.authenticator.tables import (
    AuthenticatorSecret as AuthenticatorSecret_,
)
from piccolo_api.session_auth.tables import SessionsBase

try:
    Path(Path(__file__).parent.parent / "data").mkdir()
except FileExistsError:
    pass

DB_PATH = Path("data").absolute() / "auth.sqlite"
DB = SQLiteEngine(str(DB_PATH))


class Sessions(SessionsBase, db=DB):
    pass


class User(BaseUser, tablename="piccolo_user", db=DB):
    pass


class AuthenticatorSecret(AuthenticatorSecret_, db=DB):
    pass
