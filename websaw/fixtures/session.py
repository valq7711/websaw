import uuid
import json
import jwt
import time
from typing import Optional

from ..core.globs import current_config
from ..core import Fixture
from ..core import BaseContext


_UNDEFINED = object()


class IStorage:
    def get(self, key: str) -> str:
        raise NotImplementedError()

    def set(self, key: str, value: str, expiration: int):
        raise NotImplementedError()


class Session(Fixture):
    secret: str
    expiration: int
    algorithm: str
    storage: Optional[IStorage]
    same_site: str
    env_token_key: str

    def __init__(
        self,
        secret: str = None,
        expiration: int = None,
        algorithm="HS256",
        storage: str = None,
        same_site="Lax",
        env_token_key="session_token",
        env_cfg_key='session_config',
    ):
        """
        Args:
            secret: the key used to encrypt the session (using algorithm), if not provided must be in
                    `ctx.env[env_cfg_key]`
            algorithm: jwt-algorithm, can be in `ctx.env[env_cfg_key]`
            expiration: in seconds, optional, can be in `ctx.env[env_cfg_key]`
            storage: session storage fixture name, optional, can be in `ctx.env[env_cfg_key]`
                if not provided session is stored in cookie as jwt, otherwise `ctx.ask(self.storage)`
                must return `storage: IStorage` and the jwt is stored in it and its uuid key is stored in the cookie
            same_site: SameSite-attr, can be in `ctx.env[env_cfg_key]`
            env_token_key: `ctx.env`-key, if there is no token in cookie then it could be passed in
                           `ctx.env[env_token_key]`, can be used to set session from query string, for example
        """
        self.config = dict(
            secret=secret,
            expiration=int(expiration) if expiration is not None else None,
            algorithm=algorithm,
            storage=storage,
            same_site=same_site,
            env_token_key=env_token_key,
        )
        self.env_cfg_key = env_cfg_key

    def __getattr__(self, k):
        v = self.data.config.get(k, _UNDEFINED)
        if v is _UNDEFINED:
            raise AttributeError(k)
        return v

    def app_mounted(self, ctx):
        if not self.config['secret']:
            self.config['secret'] = current_config.session_secret

    def take_on(self, ctx: BaseContext):
        self.data.ctx = ctx
        self.load(ctx)

    def take_off(self, ctx):
        if self.data.changed:
            self.save()

    @staticmethod
    def get_session_cookie_name(app_data):
        return f'{app_data.app_name}_session'

    def initialize(self, request, response, session_cookie_name, ctx, data=None, secure=False):
        local = self.data
        local.request = request
        local.response = response
        local.session_cookie_name = session_cookie_name  # f"{app_name}_session"
        local.data = data or {}
        local.secure = secure

        local.changed = False
        config = local.config = {
            **self.config,
            **ctx.env.get(self.env_cfg_key, {})
        }
        assert config['secret'], 'session secret not provided'
        storage = config['storage']
        if storage is not None:
            storage_fixture = ctx.ask(storage)
            if storage_fixture is None:
                raise KeyError(f'Storage is not provided by context: {storage}')
            config['storage'] = storage_fixture

    def load(self, ctx: BaseContext):
        request = ctx.request
        session_cookie_name = self.get_session_cookie_name(ctx.app_data)
        env_get = request.environ.get
        secure = "https" == (
            env_get('HTTP_X_FORWARDED_PROTO') or env_get('wsgi.url_scheme')
        )
        self.initialize(
            request=request,
            response=ctx.response,
            session_cookie_name=session_cookie_name,
            ctx=ctx,
            secure=secure,
        )

        token_data = (
            request.get_cookie(session_cookie_name)
            or ctx.env.get(self.env_token_key)
        )

        # fast exit
        if not token_data:
            return

        if isinstance(token_data, str):
            token_data = token_data.encode()

        try:
            token_decoded = jwt.decode(
                token_data, self.secret, algorithms=[self.algorithm]
            )
        except jwt.PyJWTError:
            return

        data = None
        storage = self.storage
        if storage is not None:
            data_in_cookie = False
            json_data = storage.get(token_decoded)
            if json_data:
                try:
                    data = json.loads(json_data)
                except json.JSONDecodeError:
                    pass
        else:
            data_in_cookie = True
            data = token_decoded

        if data is None:
            return

        expiration = self.expiration
        is_valid = (
            session_cookie_name == data.get("session_cookie_name")
            and "uuid" in data
            and (
                not data_in_cookie
                or expiration is None
                or expiration > time.time() - data.get("timestamp", 0)
            )
            and secure is data.get("secure")
        )
        if not is_valid:
            self.clear()
        else:
            self.data.data = data

    def get_data(self):
        return self.data.data

    def save(self):
        local = self.data
        data = local.data
        response = local.response
        storage = self.storage
        expiration = self.expiration
        data["timestamp"] = time.time()
        session_cookie_name = data["session_cookie_name"] = local.session_cookie_name
        secure = data["secure"] = local.secure
        if "uuid" not in data:
            data["uuid"] = str(uuid.uuid1())
        if storage is not None:
            cookie_data = data["uuid"]
            storage.set(cookie_data, json.dumps(data), expiration)
        else:
            cookie_data = data

        cookie_data = jwt.encode(
            cookie_data, self.secret, algorithm=self.algorithm
        )
        if isinstance(cookie_data, bytes):
            cookie_data = cookie_data.decode()

        response.set_cookie(
            session_cookie_name,
            cookie_data,
            path="/",
            secure=secure,
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

    def pop(self, key, *default):
        sd = self.data
        v = sd.data.pop(key, *default)
        sd.changed = True
        return v

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
