import os
import functools
from types import SimpleNamespace

from . import globs
from .context import BaseContext
from .exceptions import FixtureProcessError
from .reloader import Reloader


def _dummy_exception_handler(ctx: BaseContext, exc: Exception):
    raise exc


class StaticRegistry:

    static_file = staticmethod(globs.static_file)

    class Registered(SimpleNamespace):
        folder: str
        client_apps: set

    mounted: dict[str, Registered] = {}

    def register(self, base_url, folder, app):
        folder_apps = self.mounted.get(base_url)
        if folder_apps:
            if os.path.samefile(folder_apps.folder, folder):
                raise KeyError(
                    f'URL already in use: {base_url} => path:'
                    f'{folder_apps.folder}'
                )
            folder_apps.client_apps.add(app)
        self.mounted[base_url] = SimpleNamespace(
            folder=folder, client_apps={app}
        )

    def get_registered(self, base_url, folder):
        folder_apps = self.mounted.get(base_url)
        if not folder_apps:
            return None
        if os.path.samefile(folder_apps.folder, folder):
            return folder_apps

    def make_rule_and_handler(self, static_base_url, folder, client_app):
        if not os.path.exists(folder):
            return None, None
        registered = self.get_registered(static_base_url, folder)
        if registered:
            registered.client_apps.add(client_app)
            return None, None

        self.register(static_base_url, folder, client_app)
        rule = fr'{static_base_url}/static/<re((_\d+(\.\d+){2}/)?)><fp.path()>'
        h = self.make_static_handler(folder)
        return rule, h

    @classmethod
    def make_static_handler(cls, folder):
        response = globs.response

        def serve_static(fp):
            response.headers.setdefault("Pragma", "cache")
            response.headers.setdefault("Cache-Control", "private")
            return cls.static_file(fp, root=folder)
        return serve_static

    def __contains__(self, base_url_folder_tuple):
        if isinstance(base_url_folder_tuple, str):
            raise TypeError(
                f'A pair like [url, folder] is required, '
                f'got string: {base_url_folder_tuple}'
            )
        base_url, folder = base_url_folder_tuple
        folder_apps = self.mounted.get(base_url)
        if not folder_apps:
            return False
        return os.path.samefile(folder_apps.folder, folder)


_static_registry = StaticRegistry()


class Fixtured:
    def __init__(self, h, fixt: list[str]):
        if isinstance(h, self.__class__):
            fixt = [*fixt, *h.fixt]
            h = h.h
        self.h = h
        self.fixt = fixt
        functools.update_wrapper(self, h)

    def __call__(self, *a, **kw):
        return self.h(*a, **kw)


class BaseApp:

    static_registry = _static_registry
    add_route = staticmethod(globs.app.add_route)
    reloader = Reloader

    def __init__(
        self,
        default_config,
        default_ctx: BaseContext,
        render_map: dict = None,
        exception_handler=None
    ):
        self.default_config = default_config
        self.default_ctx = default_ctx
        self._registered = {}
        self.render_map = render_map
        self.exception_handler = exception_handler

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
        if render_map is None:
            render_map = self.render_map
        if exception_handler is None:
            exception_handler = self.exception_handler

        context = context.clone()
        app_data = context.app_data = SimpleNamespace(
            routes=[],
            named_routes={},
            app_name=self.reloader.current_import_app,
            **config
        )
        for raw_h, meta in self._registered.items():
            h = self.make_handler(raw_h, meta.fixtures, context, render_map, exception_handler)
            for route_args, route_kw in meta.routes_args:
                self._mount_route(context.app_data, h, route_args, route_kw)

        static_rule, static_h = self.static_registry.make_rule_and_handler(
            app_data.static_base_url, app_data.static_folder, self
        )
        if static_rule is not None:
            self._mount_route(context.app_data, static_h, (static_rule, 'GET', None), {})
        self.reloader.register_app_data(context.app_data)
        context.app_mounted()
        return context

    @staticmethod
    def make_handler(h, fixtures, ctx: BaseContext, render_map: dict = None, exception_handler=None):

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

        def handler(**kw):
            exc = None
            ctx.initialize()
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
