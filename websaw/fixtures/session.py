import uuid
import json
import jwt
import time

from ..core.globs import current_config
from ..core import Fixture
from ..core import BaseContext


class Session(Fixture):

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
        self.expiration = expiration
        self.algorithm = algorithm
        self.storage = storage
        self.same_site = same_site

    def app_mounted(self, ctx):
        if not self.secret:
            self.secret = current_config.session_secret
        assert self.secret

    def take_on(self, ctx: BaseContext):
        self.load(ctx)

    def take_off(self, ctx):
        if self.data.changed:
            self.save()

    def initialize(self, request, response, app_name="unknown", data=None, secure=False, storage=None):
        local = self.data
        local.request = request
        local.response = response
        local.changed = False
        local.data = data or {}
        local.session_cookie_name = f"{app_name}_session"
        local.secure = secure
        local.storage = storage

    def load(self, ctx: BaseContext):
        request = ctx.request
        storage = None
        if self.storage:
            storage = ctx.ask(self.storage)
            if storage is None:
                raise KeyError(f'Storage is not provided by context: {self.storage}')

        self.initialize(
            request=request,
            response=ctx.response,
            app_name=ctx.app_data.app_name,
            secure=request.url.startswith("https"),  # FIXME
            storage=storage
        )

        local = self.data
        raw_token = (
            request.get_cookie(local.session_cookie_name)
            or request.query.get("_session_token")
        )
        if not raw_token and request.method in {"POST", "PUT", "DELETE", "PATCH"}:
            raw_token = (
                request.forms and request.forms.get("_session_token")
                or request.json and request.json.get("_session_token")
            )
        if raw_token:
            token_data = raw_token.encode()
            try:
                if storage:
                    json_data = storage.get(token_data)
                    if json_data:
                        local.data = json.loads(json_data)
                else:
                    local.data = jwt.decode(
                        token_data, self.secret, algorithms=[self.algorithm]
                    )
                if self.expiration is not None and storage is None:
                    assert (
                        local.data["timestamp"] > time.time() - int(self.expiration)
                    )
                assert self.get_data().get("secure") == local.secure
            except Exception:
                pass

        if (
            local.session_cookie_name != local.data.get("session_cookie_name")
            or "uuid" not in self.get_data()
        ):
            self.clear()

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
        return self.get_data().get(key, default)

    def __getitem__(self, key):
        return self.get_data()[key]

    def __delitem__(self, key):
        data = self.get_data()
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
