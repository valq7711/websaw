import os
import json
import functools
from types import SimpleNamespace
from typing import List, Dict, Callable, Optional, Union, Set, Tuple
import dataclasses
from dataclasses import dataclass
from pathlib import Path

from . import globs
from .context import BaseContext
from .exceptions import FixtureProcessError
from .reloader import Reloader
from .static_registry import StaticRegistry
from .fixture import SPAFixture
from .utils import compile_pyjs_folder


try:
    import pyjsaw
except ImportError:
    pyjsaw = None
    pass


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


class SPAPath(dict):
    path: str
    is_main_path: bool
    meta: dict
    name: str

    def __init__(self, path, meta, name):
        obj = {
            'path': path,
        }
        for k, v in [('meta', meta), ('name', name)]:
            if v is not None:
                obj[k] = v

        super().__init__(obj)

    __setattr__ = dict.__setitem__

    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            raise AttributeError(k)


class SPAResponse(dict):
    pass


typeStrOrFactory = Union[str, Callable[['AppData'], str]]
pjoin = os.path.join


@dataclass
class AppData:

    app_name: str
    folder: str

    base_url: typeStrOrFactory = lambda s: f'/{s.app_name}'
    static_base_url: typeStrOrFactory = lambda s: s.base_url
    static_folder: typeStrOrFactory = lambda s: pjoin(s.folder, 'static')
    template_folder: typeStrOrFactory = lambda s: pjoin(s.folder, 'templates')
    spa_template_folder: typeStrOrFactory = lambda s: pjoin(s.static_folder, 'spa', 'pages')

    render_map: Dict[type, Callable[[BaseContext, dict], str]] = None
    exception_handler: Callable[[BaseContext, Exception], None] = None

    group_name: str = None

    spa_routes: Dict[str, Dict[str, List[SPAPath]]] = dataclasses.field(default_factory=dict)
    routes: Set[globs.Route] = dataclasses.field(default_factory=set)
    named_routes: Dict[str, globs.Route] = dataclasses.field(default_factory=dict)

    as_dict = dataclasses.asdict

    def __post_init__(self):
        for name in ['base_url', 'static_base_url', 'static_folder', 'template_folder', 'spa_template_folder']:
            fld = getattr(self, name)
            if callable(fld):
                setattr(self, name, fld(self))


class RouteMeta(SimpleNamespace):
    routes_args: List[Tuple[tuple, dict]]
    fixtures: List[str]


class BaseApp:

    static_registry = StaticRegistry
    add_route = staticmethod(globs.app.add_route)
    remove_route = staticmethod(globs.app.router.remove)
    reloader = Reloader
    SPAResponse = SPAResponse
    app_data: AppData

    def __init__(
            self,
            default_config: dict,
            context: BaseContext,
    ):
        self.default_config = default_config
        self.context = context
        self._registered: Dict[Callable, RouteMeta] = {}
        self._mixins: List['BaseApp'] = []
        self.app_data = None

    def spa(self, name='main'):
        return SPA(self, name)

    def mixin(self, *mixins: 'BaseApp'):
        self._mixins.extend(mixins)
        self.context.extend(*[m.context for m in mixins])

    def _register_route(self, fun: Callable, route_args: Tuple[tuple, dict], fixtures: List[str] = None):
        meta = self._registered.setdefault(
            fun, RouteMeta(routes_args=[], fixtures=[])
        )
        meta.routes_args.append(route_args)
        if fixtures is not None:
            meta.fixtures.extend(fixtures)

    def route(self, rule: str, method='GET', name: str = None, **kw):
        args = (rule, method, name)

        def decorator(h: Callable):
            fixt = None
            if isinstance(h, Fixtured):
                fixt = h.fixt
                h = h.h
            self._register_route(h, (args, kw), fixt)
            return h
        return decorator

    def use(self, *fixt) -> Callable[[Callable], Fixtured]:
        fixt = [self.context.get_or_make_fixture_key(f) for f in fixt]

        def decorator(h):
            if isinstance(h, Fixtured):
                h.fixt[:] = [*fixt, *h.fixt]
                return h
            return Fixtured(h, fixt)
        return decorator

    def mount(self, config: dict = None, *, as_mixin=False):
        mount_meth = self._mount if not as_mixin else self._mount_as_mixin
        try:
            mount_meth(config)
        except Exception:
            if self.app_data is not None:
                self.unmount()
            raise

    def _mount_as_mixin(self, config: dict = None):
        if config is None:
            config = self.default_config

        app_data = AppData(**config)
        self._compile_pyjs_folder(app_data.folder, app_data.static_folder)

    def _mount(self, config: dict = None):
        if config is None:
            config = self.default_config

        context = self.context.clone()
        app_data = self.app_data = context.app_data = AppData(**config)
        render_map = app_data.render_map
        exception_handler = app_data.exception_handler

        for raw_h, meta, mixin_data in self._iter_registered():
            h = self.make_handler(raw_h, meta.fixtures, context, render_map, exception_handler, mixin_data)
            spa_component = self._get_spa_component_reference(context, meta.fixtures, mixin_data)
            for route_args, route_kw in meta.routes_args:
                spa: SPA = route_kw.pop('spa', None)
                if spa:
                    self._register_spa_component_and_mount_api_route(h, route_args, route_kw, spa, spa_component)
                else:
                    self._mount_route(h, route_args, route_kw)

        self._compile_pyjs_folder(self.app_data.folder, self.app_data.static_folder)

        # make static/spa_routes.js
        # 'redirect' all spa-routes to 'index'
        self._mount_spa_routes()

        # mount static as /{app_name}/static/
        self._mount_static()

        # mount mixins static as /{app_name}/static/mxn/{mixin_name}/
        self._mount_mixins_static()

        # register
        self.reloader.register_app(app_data.app_name, self)
        context.app_mounted()
        return context

    def _register_spa_component_and_mount_api_route(
            self, h: Callable, route_args: List, route_kw: dict,
            spa: 'SPA', spa_component: str = None
    ):
        app_data = self.app_data
        route_rule, route_rest_args = route_args[0], route_args[1:]
        route_spa_main_args = None
        if spa_component:
            spa_component_routes: dict = app_data.spa_routes.setdefault(spa.name, {})
            spa_routes: list = spa_component_routes.setdefault(spa_component, [])
            spa_path = SPAPath(route_rule, route_kw.pop('meta', None), route_kw.get('name', None))
            if spa_path.path == spa.main_path:  # usually 'index'
                spa_path.is_main_path = True
                route_spa_main_args = [f'pages-api/{spa.name}', *route_rest_args]
            spa_routes.append(spa_path)
        # prefix all spa routes with 'spa-pages-api/<spa_name>'
        route_args = [f'pages-api/{spa.name}/{route_rule}', *route_rest_args]
        self._mount_route(h, route_args, route_kw)
        if route_spa_main_args:
            self._mount_route(h, route_spa_main_args, route_kw)

    def _mount_static(self):
        app_data = self.app_data
        static_rule, static_h = self.static_registry.make_rule_and_handler(
            f'{app_data.static_base_url}/static', app_data.static_folder
        )
        if static_rule is not None:
            self._mount_route(static_h, (static_rule, 'GET', None), {})

    def _mount_mixins_static(self):
        """Mount mixins static as `/{app_name}/static/mxn/{mixin_app_name}/`."""
        app_data = self.app_data
        for mxn in self._mixins:
            mxn_app_data = AppData(**mxn.default_config)
            static_base_url = f'{app_data.base_url}/static/mxn/{mxn_app_data.app_name}'
            static_rule, static_h = self.static_registry.make_rule_and_handler(
                static_base_url, mxn_app_data.static_folder
            )
            if static_rule is not None:
                self._mount_route(static_h, (static_rule, 'GET', None), {})

    def unmount(self):
        app_data = self.app_data
        base_urls = {app_data.base_url, app_data.static_base_url}
        for base_url in base_urls:
            self.remove_route(f'{base_url}/*')
            self.remove_route(base_url)
        for r in app_data.routes:
            root_prefix = f"/{r.rule[1:].split('/', 1)[0]}"
            if root_prefix not in base_urls:
                self.remove_route(r)

    def _get_spa_component_reference(self, ctx: BaseContext, fixture_keys: List[str], mixin_data: AppData = None):
        if not fixture_keys:
            return
        first = ctx.ask(fixture_keys[0])
        if not isinstance(first, SPAFixture):
            return
        spa_component = first

        prefix = ''
        if mixin_data:
            prefix = f'mxn/{mixin_data.app_name}'
        return spa_component.make_component_reference(ctx, prefix)

    def _compile_pyjs_folder(self, app_folder, app_static_folder):
        pyjs_dir = Path(app_folder) / 'pyjs'
        out_dir = Path(app_static_folder) / 'pyjs'
        compile_pyjs_folder(pyjs_dir, out_dir)

    def _mount_spa_routes(self):
        spa_routes_map = self.app_data.spa_routes
        if not spa_routes_map:
            return
        static_folder = Path(self.app_data.static_folder)
        for spa_name, spa_component_routes in spa_routes_map.items():
            spa_routes_json = json.dumps(spa_component_routes, indent=4)
            (
                (static_folder / f'spa_{spa_name}_routes.js')
                .write_text(f'SPA_ROUTES={spa_routes_json}', encoding='utf8')
            )
            spa_main_handler = self.app_data.named_routes[f'spa_main[{spa_name}]'].methods['GET'].handler
            for spa_paths in spa_component_routes.values():
                spa_paths = (p for p in spa_paths if not p.get('is_main_path'))
                for p in spa_paths:
                    self._mount_route(spa_main_handler, (p.path, 'GET', None), {})

    def _iter_registered(self):
        for mixin in reversed(self._mixins):
            for raw_h, meta in mixin._registered.items():
                yield raw_h, meta, AppData(**mixin.default_config)

        for raw_h, meta in self._registered.items():
            yield raw_h, meta, None

    @staticmethod
    def make_handler(
            h: Callable, fixtures: List[str], ctx: BaseContext,
            render_map: dict = None, exception_handler=None, mixin_data=None
    ) -> Callable:

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

    def _mount_route(self, fun, route_args, route_kw):
        path, method, name = route_args
        app_data = self.app_data

        is_app_index = path == 'index'
        path = self._get_abs_url(app_data.base_url, path)
        route = self.add_route(path, method, fun, **route_kw)
        app_data.routes.add(route)
        if name:
            if name in app_data.named_routes:
                raise KeyError(f'The route name already in use: {name}')
            app_data.named_routes[name] = route

        if is_app_index:
            route = self.add_route(
                path[:-len('/index')] or '/', method, fun, **route_kw
            )
            app_data.routes.add(route)


class SPA:

    main_route_name: str
    main_path: str

    def __init__(self, app: BaseApp, name):
        self.name = name
        self._app = app

    def main(self, path):
        self.main_route_name = f'spa_main[{self.name}]'
        self.main_path = path
        return self._app.route(path, name=self.main_route_name)

    def route(self, rule, *args, **kw):
        kw['spa'] = self
        return self._app.route(rule, *args, **kw)

    def use(self, *fixt):
        return self._app.use(*fixt)

    def response(self, **kw):
        return SPAResponse(**kw)
