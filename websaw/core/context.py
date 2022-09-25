import threading
from types import SimpleNamespace
from typing import Any, Optional, List, Dict, Union

from .exceptions import FixtureProcessError
from . import globs
from .fixture import Fixture
from . import app


class IContextSate:
    in_use: Dict[str, Fixture]
    in_use_stack: List[Fixture]
    uninitialized_hooks_in_stack: set
    output: Any
    exception_stack: List[Exception]

class Local(threading.local):
    state: IContextSate
    in_process: bool
    mixin_data: SimpleNamespace
    env: Dict


class MetaContext(type):

    def __new__(cls, name, bases, dct):
        if not bases:
            return super().__new__(cls, name, bases, dct)

        dct['_env'] = dct.pop('env', {})
        new_fixt = {
            k: dct.pop(k) for k, v in {**dct}.items()
            if isinstance(v, Fixture)
        }
        base_fixt = {}
        [
            base_fixt.update(getattr(bcls, '_fixt', {}))
            for bcls in reversed(bases)
        ]
        dct['_fixt'] = {**base_fixt, **new_fixt}
        out_cls = super().__new__(cls, name, bases, dct)
        return out_cls


class BaseContext(metaclass=MetaContext):

    __local__ = threading.local()

    _fixt: Dict[str, Fixture] = {}  # see metaclass
    _env: dict  # default env, see metaclass

    _fixture_initialize = Fixture.initialize_safe_storage
    _fixture_prepare_for_use = Fixture.prepare_for_use

    request = globs.request
    response = globs.response
    app_data: 'app.AppData' = None

    @classmethod
    def cctx(cls) -> 'BaseContext':
        return cls.__local__.current_ctx

    def __init__(self):
        self._fixt = {**self._fixt}
        self._reverse_map = {f: k for k, f in self._fixt.items()}
        self._local = Local()
        self._local.in_process = False
        self._local.mixin_data = None
        self._local.env = None

    @property
    def state(self) -> IContextSate:
        return self._local.state

    @property
    def env(self) -> Dict:
        return self._local.env

    @env.setter
    def env(self, env: Dict):
        self._local.env = env

    @property
    def exception(self) -> Optional[Exception]:
        try:
            return self._local.state.exception_stack[0]
        except IndexError:
            pass

    @property
    def output(self):
        return self._local.state.output

    @output.setter
    def output(self, output):
        self._local.state.output = output

    @property
    def mixin_data(self):
        return self._local.mixin_data

    @mixin_data.setter
    def mixin_data(self, v):
        self._local.mixin_data = v

    def ask(self, fixture_key, default=None):
        return getattr(self, fixture_key, default)

    def get(self, app_attr, default=None):
        return getattr(self.app_data, app_attr, default)

    def mixin_get(self, mixin_attr, default=None):
        return getattr(self.mixin_data, mixin_attr, default)

    def __getitem__(self, k):
        return getattr(self.app_data, k)

    def __getattr__(self, k):
        local = self._local
        if not local.in_process:
            try:
                return self._fixt[k]
            except KeyError:
                raise AttributeError(k)
        state = local.state
        in_use = state.in_use
        fixt_value = in_use.get(k)
        if fixt_value is None:
            try:
                fixt = self._fixt[k]
            except KeyError:
                raise AttributeError(k)
            self._fixture_prepare_for_use(fixt)
            try:
                value = fixt.take_on(self)
            except Exception as exc:
                state.exception_stack.append(exc)
                raise FixtureProcessError()
            if value is None:
                value = fixt
            in_use[k] = (fixt, value)
            if fixt.is_hook:
                if k in state.uninitialized_hooks_in_stack:
                    # this is an edge case:
                    # there were some errors while processing fixtures from app.use()
                    # that happened before the hook was taken on.
                    # So the hook in in_use_stack, but it was not initialized,
                    # but now someone touches it via context.<hook>
                    # so we should reoder it in in_use_stack
                    state.in_use_stack.remove(fixt)
                    state.in_use_stack.append(fixt)
                    state.uninitialized_hooks_in_stack.pop(k)
                else:
                    state.in_use_stack.append(fixt)
            else:
                state.in_use_stack.append(fixt)
        else:
            value = fixt_value[1]
        return value

    def get_or_make_fixture_key(self, f) -> str:
        key = self._reverse_map.get(f)
        if key is None:
            key = getattr(f, 'context_key', None)
            if key is None:
                key = f'ID_{id(f)}'
            self._fixt[key] = f
            self._reverse_map[f] = key
        return key

    def clone(self, app_data=None):
        ret = self.__class__()
        ret._fixt = {**self._fixt}
        ret._reverse_map = {**self._reverse_map}
        ret.app_data = app_data
        return ret

    def extend(self, *mixins):
        fixt = {}
        [fixt.update(m._fixt) for m in reversed(mixins)]
        [self._fixt.setdefault(k, f) for k, f in fixt.items()]
        # rebuild reverse map
        self._reverse_map = {f: k for k, f in self._fixt.items()}

    def app_mounted(self):
        [f.app_mounted(self) for f in self._fixt.values()]

    def initialize(self):
        self.__local__.current_ctx = self
        local = self._local
        local.state = SimpleNamespace(
            in_use={},
            in_use_stack=[],
            uninitialized_hooks_in_stack=set(),
            output=None,
            exception_stack=[],
        )
        local.env = {**self._env}
        local.in_process = True
        self._fixture_initialize()

    def use_fixtures(self, fixt, hooks: Union[bool, dict] = False):
        if hooks:
            try:
                for fkey in fixt:
                    getattr(self, fkey)
                    hooks.pop(fkey, None)
            except Exception:
                if hooks:
                    state = self._local.state
                    state.in_use_stack.extend(hooks.values())
                    state.uninitialized_hooks_in_stack.update(hooks)
                raise
        else:
            [getattr(self, fkey) for fkey in fixt]

    def finalize(self, exc):
        state = self._local.state
        if exc:
            state.exception_stack.append(exc)

        max_cnt = 100
        in_use = state.in_use
        in_use_stack = state.in_use_stack

        err = None
        while max_cnt > 0:
            max_cnt -= 1
            if not in_use_stack:
                break
            f = in_use_stack.pop()
            try:
                f.take_off(self)
            except Exception as exc:
                state.exception_stack.append(exc)
            in_use[self._reverse_map[f]] = None
        else:
            err = RuntimeError('Max number of iterations exceeded')
        self._local.in_process = False
        if err:
            raise err
