import copy
from pydal import DAL as _DAL
from threadsafevariable import ThreadSafeVariable

from ..core import BaseContext
from ..core.core_events import core_event_bus, CoreEvents
from ..core.fixture import Fixture
from .dbregistry import DBRegistry




# this global object will be used to store their state to restore it for every http request
ICECUBE = {}


@core_event_bus.on(CoreEvents.APPS_LOADED)
def update_icecube(*a, **kw):
    ICECUBE.update(ThreadSafeVariable.freeze())


class DAL(_DAL, Fixture):

    reconnect_on_request = True

    _websaw_db_registry_key = 'db_registry'

    def set_db_registry_key(self, key: str):
        self._websaw_db_registry_key = key

    @property
    def websaw_db_registry_key(self) -> str:
        return self._websaw_db_registry_key

    def take_on(self, ctx: BaseContext):
        if self.reconnect_on_request:
            self._adapter.reconnect()
        ThreadSafeVariable.restore(ICECUBE)

    def app_mounted(self, ctx: BaseContext):
        """Perform self-registration if `self._websaw_db_registry_key` in ctx."""
        db_registry: DBRegistry = ctx.ask(self._websaw_db_registry_key)
        if db_registry is not None:
            self_key = ctx.get_or_make_fixture_key(self)
            db_registry.register(self_key)

    def take_off(self, ctx: BaseContext):
        if ctx.exception:
            self.rollback()
        else:
            self.commit()
        self._adapter.close(action=None, really=False)


# make sure some variables in pydal are thread safe
def thread_safe_pydal_patch():
    Field = _DAL.Field
    tsafe_attrs = [
        "readable",
        "writable",
        "default",
        "update",
        "requires",
        "widget",
        "represent",
    ]
    [setattr(Field, a, ThreadSafeVariable()) for a in tsafe_attrs]

    # hack 'copy.copy' behavior, since it makes a shallow copy,
    # but ThreadSafe-attributes (see above) are class-level, so:
    # no copy -> no attr in ICECUBE for the fresh one -> gevent-error on try to access to any of ThreadSafe-attributes
    def field_copy(self):
        # to prevent infinite recursion
        # temporarily set __copy__ to None
        me = self.__class__.__copy__
        self.__class__.__copy__ = None
        clone = copy.copy(self)
        self.__class__.__copy__ = me
        [setattr(clone, a, getattr(self, a)) for a in tsafe_attrs]
        return clone

    # to avoid possible future problems
    if hasattr(Field, "__copy__"):
        raise RuntimeError("code fix required!")
    setattr(Field, "__copy__", field_copy)


thread_safe_pydal_patch()
