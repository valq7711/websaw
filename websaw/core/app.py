import functools
from types import SimpleNamespace
from typing import List

from . import globs
from .context import BaseContext
from .exceptions import FixtureProcessError
from .reloader import Reloader
from .static_registry import static_registry


def _dummy_exception_handler(ctx: BaseContext, exc: Exception):
    raise exc


class Fixtured:
    def __init__(self, h, fixt: List[str]):
        if isinstance(h, self.__class__):
            fixt = [*fixt, *h.fixt]
            h = h.h
        self.h = h
        self.fixt = fixt
        functools.update_wrapper(self, h)

    def __call__(self, *a, **kw):
        return self.h(*a, **kw)


class BaseApp:

    static_registry = static_registry
    add_route = staticmethod(globs.app.add_route)
    reloader = Reloader

    def __init__(
        self,
        default_config,
        default_ctx: BaseContext,
    ):
        self.default_config = default_config
        self.default_ctx = default_ctx
        self._registered = {}
        self._mixins = []

    def mixin(self, *mixins):
        self._mixins.extend(mixins)
        self.default_ctx.extend(*[m.default_ctx for m in mixins])

    def _register(self, fun, route_args, fixtures=None):
        meta = self._registered.setdefault(
            fun, SimpleNamespace(routes_args=[], fixtures=[])
        )
        meta.routes_args.append(route_args)
        if fixtures is not None:
            meta.fixtures.extend(fixtures)

    def route(self, rule, method='GET', name=None, **kw):
        args = (rule, method, name)

        def decorator(h):
            raw_h = h
            fixt = None
            if isinstance(h, Fixtured):
                raw_h = h.h
                fixt = h.fixt
            self._register(h, (args, kw), fixt)
            return raw_h
        return decorator

    def use(self, *fixt):
        fixt = [self.default_ctx.get_or_make_fixture_key(f) for f in fixt]

        def decorator(h):
            if isinstance(h, Fixtured):
                h.fixt[:] = [*fixt, *h.fixt]
                return h
            return Fixtured(h, fixt)
        return decorator

    def mount(
        self,
        config: dict = None,
        context: BaseContext = None,
        render_map: dict = None,
        exception_handler=None
    ):
        if context is None:
            context = self.default_ctx
        if config is None:
            config = self.default_config

        render_map: dict = config.get('render_map')
        exception_handler = config.get('exception_handler')

        context = context.clone()
        app_data = context.app_data = SimpleNamespace(
            routes=[],
            named_routes={},
            #app_name=self.reloader.current_import_app,
            **config
        )
        for raw_h, meta, mixin_data in self._iter_registered():
            h = self.make_handler(raw_h, meta.fixtures, context, render_map, exception_handler, mixin_data)
            for route_args, route_kw in meta.routes_args:
                self._mount_route(context.app_data, h, route_args, route_kw)

        static_rule, static_h = self.static_registry.make_rule_and_handler(
            f'{app_data.static_base_url}/static', app_data.static_folder, app_data.app_name
        )
        if static_rule is not None:
            self._mount_route(context.app_data, static_h, (static_rule, 'GET', None), {})

        for m in self._mixins:
            m_cfg = m.default_config
            m_name = m_cfg['app_name']
            static_base_url = f'{app_data.base_url}/static/mxn/{m_name}'
            static_rule, static_h = self.static_registry.make_rule_and_handler(
                static_base_url, m_cfg['static_folder'], app_data.app_name
            )
            if static_rule is not None:
                self._mount_route(context.app_data, static_h, (static_rule, 'GET', None), {})

        self.reloader.register_app_data(context.app_data)
        context.app_mounted()
        return context

    def _iter_registered(self):
        for m in reversed(self._mixins):
            for raw_h, meta in m._registered.items():
                yield raw_h, meta, SimpleNamespace(**m.default_config)

        for raw_h, meta in self._registered.items():
            yield raw_h, meta, None

    @staticmethod
    def make_handler(h, fixtures, ctx: BaseContext, render_map: dict = None, exception_handler=None, mixin_data=None):

        hooks = False
        if fixtures:
            hooks = {
                fkey: fobj for fkey, fobj
                in ([fkey, getattr(ctx, fkey)] for fkey in fixtures)
                if fobj.is_hook
            } or False
        else:
            fixtures = False

        if exception_handler is None:
            exception_handler = _dummy_exception_handler

        @functools.wraps(h)
        def handler(**kw):
            exc = None
            ctx.initialize()
            ctx.mixin_data = mixin_data
            try:
                if fixtures:
                    ctx.use_fixtures(fixtures, hooks)
                ctx.output = h(ctx, **kw)
            except FixtureProcessError:
                pass
            except Exception as exc_:
                exc = exc_
            ctx.finalize(exc)
            if ctx.exception is not None:
                exception_handler(ctx, ctx.exception)

            if render_map:
                output = ctx.output
                render = render_map.get(type(output), False)
                if render:
                    ctx.output = render(ctx, output)
            return ctx.output
        return handler

    @staticmethod
    def _get_abs_url(base_url, path):
        if not path:
            return base_url
        if path[0] != '/':
            path = f'{base_url}/{path}'
        return path

    def _mount_route(self, app_data, fun, route_args, route_kw):
        path, method, name = route_args

        is_index = path == 'index'
        path = self._get_abs_url(app_data.base_url, path)
        route = self.add_route(path, method, fun, **route_kw)
        app_data.routes.append(route)
        if name:
            if name in app_data.named_routes:
                raise KeyError(f'The route name already in use: {name}')
            app_data.named_routes[name] = route

        if is_index:
            route = self.add_route(
                path[:-len('/index')] or '/', method, fun, **route_kw
            )
            app_data.routes.append(route)
