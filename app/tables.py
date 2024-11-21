from pathlib import Path

from piccolo.apps.user.tables import BaseUser
from piccolo.engine.sqlite import SQLiteEngine
from piccolo_api.mfa.authenticator.tables import (
    AuthenticatorSecret as AuthenticatorSecret_,
)
from piccolo_api.session_auth.tables import SessionsBase

DATA_DIR = Path(__file__).parent.parent / "data"

if not DATA_DIR.exists():
    DATA_DIR.mkdir()

DB = SQLiteEngine(str(DATA_DIR / "auth.sqlite"))


class Sessions(SessionsBase, db=DB):
    pass


class User(BaseUser, tablename="piccolo_user", db=DB):
    pass


class AuthenticatorSecret(AuthenticatorSecret_, db=DB):
    pass
