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


class CurrentUser(Fixture):

    def take_on(self, ctx: BaseContext):
        group_name = getattr(ctx.app_data, 'group_name', None)
        if group_name is not None:
            session: Fixture = ctx.group_session
        else:
            session: Fixture = ctx.session

        self.data.session = session

        user = session.get("user")
        user_id = user and user.get('id')

        if not user_id:
            if user is not None:
                self.clear()

    def take_off(self, ctx):
        if self.user:
            activity = self.recent_activity
            time_now = calendar.timegm(time.gmtime())
            if not activity or time_now - activity > 6:
                self.recent_activity = time_now
        else:
            self.recent_activity = None

    @property
    def recent_activity(self):
        return self.data.session.get("recent_activity")

    @recent_activity.setter
    def recent_activity(self, v):
        self.data.session["recent_activity"] = v
        return v

    @property
    def user(self):
        return self.data.session.get("user")

    def store_user_in_session(self, user: dict):
        session = self.data.session
        session["user"] = user
        session["uuid"] = str(uuid.uuid1())

    def clear(self):
        del self.data.session["user"]


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
        cuser: CurrentUser = ctx.current_user
        config: dict = ctx.ask(self.config_fkey, {})
        condition = config.get('condition', self.condition)
        user = cuser.user
        if cuser.user is None:
            cuser.recent_activity = None
            raise self._error(AuthErr.UNAUTHORIZED)

        activity = cuser.recent_activity
        time_now = calendar.timegm(time.gmtime())
        session_timeout = self.session_timeout
        # enforce the optionl auth session expiration time
        if session_timeout and activity:
            if time_now - activity > session_timeout:
                cuser.clear()
                raise self._error(AuthErr.TIMEOUT)
        # record the time of the latest activity for logged in user (with throttling)
        if condition and not condition(user):
            raise self._error(AuthErr.FORBIDDEN)
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
        self.data.ctx = ctx
        self.data.session = ctx.session
        self.data.cuser = ctx.current_user
        
    def user_by_login(self, login: str) -> dict:
        """Return user record with credentials.

        user: {'<self.id>', 'password', '<self.ban_field>'}
        ban-field is optional if `self.ban_field` is not set
        """
        raise NotImplementedError()

    def register(self, fields):
        """Registers a new user after the user's parameters are entered
        in the SignUp form"""
        raise NotImplementedError

    def update_profile(self, id, fields):
        db = self.data.ctx.auth_db
        self.res = db.auth_user(id).update_record(
            username=fields["username"],
            email=fields["email"],
            first_name=fields["first_name"],
            last_name=fields["last_name"],
        )
        if self.res: 
            rec = db.auth_user(self.res['id'])
            rec = self.store_user_in_session(self.res)
        return dict(id=self.res['id'])

    def user_for_session(self, user):
        return {"id": user[self.id_field]}

    def store_user_in_session(self, user: dict):
        self.data.cuser.store_user_in_session(user)
        self.data.ctx.state.shared_data['template_context']['l_user'] = user
            

    @property
    def user(self):
        return self.data.cuser.user

    @property
    def user_id(self):
        user = self.user
        return user and user["id"]

    @property
    def is_logged_in(self):
        return self.user is not None

    # Methods that do not assume a user

    def check_credentials(self, login: str, password: str) -> Tuple[dict, AuthErr]:
        user = self.user_by_login(login)
        if not user:
            return (None, AuthErr.CREDENTIALS)
        if self.ban_field and user[self.ban_field]:
            return (None, AuthErr.BANNED)
        #if password != user['password']:
        #    print('Password', password, 'User password', user['password'])
        #    return (None, AuthErr.CREDENTIALS)
        crypt_pw = self.crypt(password)
        if crypt_pw != user['password']:
            return (None, AuthErr.CREDENTIALS)
        return (user, None)

    def login(self, name, password) -> Tuple[dict, AuthErr]:
        user, error = self.check_credentials(name, password)
        if user:
            self.store_user_in_session(self.user_for_session(user))
            return (user, None)
        return None, error

    def logout(self):
        self.data.cuser.clear()
