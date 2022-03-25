import uuid
import json
import jwt
import time

from ..core.globs import current_config
from ..core import Fixture
from ..core import BaseContext


class Session(Fixture):
    token_env_key = "session_token"

    # All apps share the same default secret if not specified.

    def __init__(
        self,
        secret=None,
        expiration=None,
        algorithm="HS256",
        storage=None,
        same_site="Lax",
    ):
        """
        secret is the shared key used to encrypt the session (using algorithm)
        expiration is in seconds
        (optional) storage must have a get(key) and set(key,value,expiration) methods
        if not provided session is stored in jwt cookie else the jwt is stored in storage
        and its uuid key is stored in the cookie
        """
        self.secret = secret  # see app_mounted
        self.expiration = int(expiration) if expiration is not None else None
        self.algorithm = algorithm
        self.storage = storage
        self.same_site = same_site

    def app_mounted(self, ctx):
        if not self.secret:
            self.secret = current_config.session_secret
        assert self.secret

    def take_on(self, ctx: BaseContext):
        self.data.ctx = ctx
        self.load(ctx)

    def take_off(self, ctx):
        if self.data.changed:
            self.save()

    @staticmethod
    def get_session_cookie_name(app_data):
        return f'{app_data.app_name}_session'

    def initialize(self, request, response, session_cookie_name, data=None, secure=False, storage=None):
        local = self.data
        local.request = request
        local.response = response
        local.changed = False
        local.data = data or {}
        local.session_cookie_name = session_cookie_name  # f"{app_name}_session"
        local.secure = secure
        local.storage = storage

    def load(self, ctx: BaseContext):
        request = ctx.request
        storage = None
        data_in_cookie = True
        if self.storage:
            storage = ctx.ask(self.storage)
            if storage is None:
                raise KeyError(f'Storage is not provided by context: {self.storage}')
            data_in_cookie = False

        session_cookie_name = self.get_session_cookie_name(ctx.app_data)

        env_get = request.environ.get
        secure = "https" == (
            env_get('HTTP_X_FORWARDED_PROTO') or env_get('wsgi.url_scheme')
        )

        self.initialize(
            request=request,
            response=ctx.response,
            session_cookie_name=session_cookie_name,
            secure=secure,
            storage=storage
        )

        token_data = (
            request.get_cookie(session_cookie_name)
            or ctx.env.get(self.token_env_key)
        )

        # fast exit
        if not token_data:
            return

        if isinstance(token_data, str):
            token_data = token_data.encode()

        data = None
        if storage is not None:
            json_data = storage.get(token_data)
            if json_data:
                try:
                    data = json.loads(json_data)
                except json.JSONDecodeError:
                    pass
        else:
            try:
                data = jwt.decode(
                    token_data, self.secret, algorithms=[self.algorithm]
                )
            except jwt.PyJWTError:
                pass

        if data is None:
            return

        is_valid = True

        if session_cookie_name != data.get("session_cookie_name"):
            is_valid = False
        if is_valid and "uuid" not in data:
            is_valid = False
        if is_valid and data_in_cookie and self.expiration is not None:
            is_valid = self.expiration > time.time() - data.get("timestamp", 0)
        if is_valid and secure is not data.get("secure"):
            is_valid = False

        if not is_valid:
            self.clear()
        else:
            self.data.data = data

    def get_data(self):
        return self.data.data

    def save(self):
        local = self.data
        response = local.response
        local.data["timestamp"] = time.time()
        local.data["session_cookie_name"] = local.session_cookie_name
        if local.storage:
            cookie_data = local.data["uuid"]
            local.storage.set(cookie_data, json.dumps(local.data), self.expiration)
        else:
            cookie_data = jwt.encode(
                local.data, self.secret, algorithm=self.algorithm
            )
            if isinstance(cookie_data, bytes):
                cookie_data = cookie_data.decode()

        response.set_cookie(
            local.session_cookie_name,
            cookie_data,
            path="/",
            secure=local.secure,
            samesite=self.same_site,
        )

    def get(self, key, default=None):
        return self.data.data.get(key, default)

    def __getitem__(self, key):
        return self.data.data[key]

    def __delitem__(self, key):
        data = self.data.data
        if key in data:
            self.data.changed = True
            del data[key]

    def __setitem__(self, key, value):
        self.data.changed = True
        self.data.data[key] = value

    def __contains__(self, k):
        return k in self.keys()

    def keys(self):
        return self.data.data.keys()

    def __iter__(self):
        yield from self.data.data.items()

    def clear(self):
        """Produces a brand-new session."""
        local = self.data
        local.changed = True
        data = local.data
        data.clear()
        data["uuid"] = str(uuid.uuid1())
        data["secure"] = local.secure


class GroupSession(Session):

    @staticmethod
    def get_session_cookie_name(app_data):
        return f'{app_data.group_name}_session'
