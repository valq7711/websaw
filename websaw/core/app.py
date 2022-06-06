import os
import json
import functools
from types import SimpleNamespace
from typing import List, Dict

from . import globs
from .context import BaseContext
from .exceptions import FixtureProcessError
from .reloader import Reloader
from .static_registry import StaticRegistry
from .fixture import SPAFixture


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

    static_registry = StaticRegistry
    add_route = staticmethod(globs.app.add_route)
    remove_route = staticmethod(globs.app.router.remove)
    reloader = Reloader

    def __init__(
            self,
            default_config,
            context: BaseContext,
    ):
        self.default_config = default_config
        self.context = context
        self._registered = {}
        self._mixins: List['BaseApp'] = []
        self.app_data = None

    def spa(self, name='main'):
        return SPA(self, name)

    def mixin(self, *mixins):
        self._mixins.extend(mixins)
        self.context.extend(*[m.context for m in mixins])

    def _register_route(self, fun, route_args, fixtures=None):
        meta = self._registered.setdefault(
            fun, SimpleNamespace(routes_args=[], fixtures=[])
        )
        meta.routes_args.append(route_args)
        if fixtures is not None:
            meta.fixtures.extend(fixtures)

    def route(self, rule, method='GET', name=None, **kw):
        args = (rule, method, name)

        def decorator(h):
            fixt = None
            if isinstance(h, Fixtured):
                fixt = h.fixt
                h = h.h
            self._register_route(h, (args, kw), fixt)
            return h
        return decorator

    def use(self, *fixt):
        fixt = [self.context.get_or_make_fixture_key(f) for f in fixt]

        def decorator(h):
            if isinstance(h, Fixtured):
                h.fixt[:] = [*fixt, *h.fixt]
                return h
            return Fixtured(h, fixt)
        return decorator

    def mount(self, config: dict = None):
        try:
            self._mount(config)
        except Exception:
            if self.app_data is not None:
                self.unmount()
            raise

    def _mount(self, config: dict = None):
        if config is None:
            config = self.default_config

        render_map: dict = config.get('render_map')
        exception_handler = config.get('exception_handler')

        context = self.context.clone()
        app_data = self.app_data = context.app_data = SimpleNamespace(
            spa_routes={},
            routes=set(),
            named_routes={},
            **config
        )
        for raw_h, meta, mixin_data in self._iter_registered():
            h = self.make_handler(raw_h, meta.fixtures, context, render_map, exception_handler, mixin_data)
            spa_component = self._get_spa_component(context, meta.fixtures)
            if spa_component:
                prefix = ''
                if mixin_data:
                    prefix = f'mxn/{mixin_data.app_name}'
                spa_component = spa_component.make_component_reference(context, prefix)
            for route_args, route_kw in meta.routes_args:
                spa: SPA = route_kw.pop('spa', None)
                if spa:
                    if spa_component:
                        spa_component_routes: dict = app_data.spa_routes.setdefault(spa.name, {})
                        spa_routes: list = spa_component_routes.setdefault(spa_component, [])
                        # collect only rules
                        spa_routes.append(route_args[0])
                    # prefix all spa routes with 'spa-pages-api/<spa_name>'
                    route_args = [f'pages-api/{spa.name}/{route_args[0]}', *route_args[1:]]
                self._mount_route(h, route_args, route_kw)

        # make static/spa_routes.js
        # 'redirect' all spa-routes to 'index'
        self._mount_spa_routes()

        # mount app static
        static_rule, static_h = self.static_registry.make_rule_and_handler(
            f'{app_data.static_base_url}/static', app_data.static_folder
        )
        if static_rule is not None:
            self._mount_route(static_h, (static_rule, 'GET', None), {})

        # mount mixins static as /{app_name}/static/mxn/{mixin_name}/
        for m in self._mixins:
            m_cfg = m.default_config
            m_name = m_cfg['app_name']
            static_base_url = f'{app_data.base_url}/static/mxn/{m_name}'
            static_rule, static_h = self.static_registry.make_rule_and_handler(
                static_base_url, m_cfg['static_folder']
            )
            if static_rule is not None:
                self._mount_route(static_h, (static_rule, 'GET', None), {})

        # register
        self.reloader.register_app(app_data.app_name, self)
        context.app_mounted()
        return context

    def unmount(self):
        app_data = self.app_data
        base_urls = {app_data.base_url, app_data.static_base_url}
        for base_url in base_urls:
            self.remove_route(f'{base_url}/*')
            self.remove_route(base_url)
        for r in app_data.routes:
            root_prefix = f"/{r.rule[1:].split('/', 1)[0]}"
            if root_prefix not in base_urls:
                r.remove()

    def _get_spa_component(self, ctx: BaseContext, fixture_keys: List[str]):
        if not fixture_keys:
            return None
        first = ctx.ask(fixture_keys[0])
        if isinstance(first, SPAFixture):
            return first

    def _mount_spa_routes(self):
        spa_routes_map: Dict[str, Dict[str, list]] = self.app_data.spa_routes
        if not spa_routes_map:
            return

        for spa_name, spa_component_routes in spa_routes_map.items():
            spa_routes_json = json.dumps(spa_component_routes, indent=4)
            with open(os.path.join(self.app_data.static_folder, f'spa_{spa_name}_routes.js'), 'w') as f:
                f.write(f'SPA_ROUTES={spa_routes_json}')
            spa_index_get_handler = self.app_data.named_routes[f'spa_main[{spa_name}]'].methods['GET'].handler
            for rules in spa_component_routes.values():
                for r in rules:
                    self._mount_route(spa_index_get_handler, (r, 'GET', None), {})

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

    def _mount_route(self, fun, route_args, route_kw):
        path, method, name = route_args
        app_data = self.app_data

        is_index = path == 'index'
        path = self._get_abs_url(app_data.base_url, path)
        route = self.add_route(path, method, fun, **route_kw)
        app_data.routes.add(route)
        if name:
            if name in app_data.named_routes:
                raise KeyError(f'The route name already in use: {name}')
            app_data.named_routes[name] = route

        if is_index:
            app_data.named_routes['[spa-index]'] = route
            route = self.add_route(
                path[:-len('/index')] or '/', method, fun, **route_kw
            )
            app_data.routes.add(route)


class SPA:

    main_route_name: str

    def __init__(self, app: BaseApp, name):
        self.name = name
        self._app = app

    def main(self, path):
        self.main_route_name = f'spa_main[{self.name}]'
        return self._app.route(path, name=self.main_route_name)

    def route(self, rule, *args, **kw):
        kw['spa'] = self
        return self._app.route(rule, *args, **kw)

    def use(self, *fixt):
        return self._app.use(*fixt)

