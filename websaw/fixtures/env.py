
from ..core import Fixture, BaseContext


class Env(Fixture):

    def __init__(self, **kw):
        self._env = kw

    def take_on(self, ctx: BaseContext):
        ctx.env.update(self._env)
