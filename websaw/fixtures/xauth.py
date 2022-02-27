import json
import calendar
import time
import uuid
from enum import Enum
from typing import Dict, Callable, Tuple

from ..core import Fixture, BaseContext, HTTP

from pydal.validators import (
    CRYPT,
)


class AuthErrEnumMixin(str):

    def __new__(cls, msg, code):
        mem = super().__new__(cls, msg)
        mem._value_ = msg
        mem.code = code
        return mem

    def __int__(self):
        return self.code

    def as_dict(self):
        return dict(code=self.code, msg=self.value)


class AuthErr(AuthErrEnumMixin, Enum):
    UNAUTHORIZED = ('unauthorized', 401)
    CREDENTIALS = ('credentials', 401)
    BANNED = ('banned', 403)
    TIMEOUT = ('timeout', 440)
    FORBIDDEN = ('forbidden', 403)


class AuthGuard(Fixture):
    config_fkey = 'auth_guard_config'

    def __init__(
        self,
        session_timeout=3600,  # seconds,
        condition=None,
        error_handlers: Dict[AuthErr, Callable] = None
    ):

        if error_handlers is None:
            error_handlers = {}
        self.error_handlers = error_handlers
        self.condition = condition
        self.session_timeout = session_timeout

    def take_on(self, ctx: BaseContext):
        self.data.user_id = None
        self.data.user = None

        session: Fixture = ctx.session
        user = session.get("user")
        user_id = user and user.get('id')
        config: dict = ctx.ask(self.config_fkey, {})
        condition = config.get('condition', self.condition)
        if user_id is None:
            if config.get('allow_anonymous') is True:
                # should be managed by fixture, which sets the config
                return
            else:
                session["recent_activity"] = None
                raise self._error(AuthErr.UNAUTHORIZED)

        activity = session.get("recent_activity")
        time_now = calendar.timegm(time.gmtime())
        session_timeout = self.session_timeout
        # enforce the optionl auth session expiration time
        if session_timeout and activity:
            if time_now - activity > session_timeout:
                del session["user"]
                raise self._error(AuthErr.TIMEOUT)
        # record the time of the latest activity for logged in user (with throttling)
        if not activity or time_now - activity > 6:
            session["recent_activity"] = time_now
        if condition and not condition(user):
            raise self._error(AuthErr.FORBIDDEN)
        self.data.user_id = user_id
        self.data.user = user

    @property
    def user(self):
        return self.data.user

    def _error(self, err_type: AuthErr):
        cb = self.error_handlers.get(err_type)
        if cb:
            return cb()
        return HTTP(int(err_type), body=err_type.as_dict())


class XAuth(Fixture):

    _crypt = CRYPT()

    @classmethod
    def crypt(cls, pw: str):
        return cls._crypt(pw)[0]

    def __init__(self, id_field='id', ban_field='is_blocked'):
        self.id_field = id_field
        self.ban_field = ban_field

    def take_on(self, ctx: BaseContext):
        session = self.data.session = ctx.session
        user = session.get("user")
        self.data.user = user

    def user_by_login(self, login: str) -> dict:
        """Return user record with credentials.

        user: {'<self.id>', 'password', '<self.ban_field>'}
        ban-field is optional if `self.ban_field` is not set
        """
        raise NotImplementedError()

    def register(self, fields):
        raise NotImplementedError()

    def user_for_session(self, user):
        return {"id": user[self.id_field]}

    def store_user_in_session(self, user: dict):
        session = self.data.session
        session["user"] = user
        session["recent_activity"] = calendar.timegm(time.gmtime())
        session["uuid"] = str(uuid.uuid1())

    @property
    def user(self):
        user = self.data.user
        return user if user and "id" in user else None

    @property
    def user_id(self):
        user = self.user
        return user and user["id"]

    @property
    def is_logged_in(self):
        return self.user_id is not None

    # Methods that do not assume a user

    def check_credentials(self, login: str, password: str) -> Tuple[dict, AuthErr]:
        user = self.user_by_login(login)
        if not user:
            return (None, AuthErr.CREDENTIALS)
        if self.ban_field and user[self.ban_field]:
            return (None, AuthErr.BANNED)
        crypt_pw = self.crypt(password)
        if crypt_pw != user['password']:
            return (None, AuthErr.CREDENTIALS)
        return (user, None)

    def login(self, name, password) -> Tuple[dict, AuthErr]:
        user, error = self.check_credentials(name, password)
        if user:
            self.store_user_in_session(self.user_for_session(user))
            self.data.user = user
            return (user, None)
        return None, error

    def logout(self):
        self.data.session.clear()
