from pyjsaw.typing.jstyping import (
    Object, this, undefined, Array, String, literal, window, RegExp, setTimeout, alert
)
from pyjsaw.typing.vuetyping import VueRouter

#from asset.rs_vue import RS_vue, V_collector
from .asyncer import asyncer
from .server import API

# globals required:
# - axios
# - VueRouter

ENV = window.SPA_ENV
PAGES_API = f'pages-api/{ENV.spa_name}'

router = None

api = API(axios, ENV.app_base)


class PageUtil:

    @staticmethod
    def set_headers_getter(hg):
        api.headers_getter = hg

    def __init__(self, vm):
        self.vm = vm
        self.on_mounted_enabled = False

    @property
    def page_api(self):
        return f'{PAGES_API}{self.vm.S_route.path}'

    @property
    def page_vm(self):
        route = self.vm.S_route.matched[0]
        if route:
            return route.instances.default.S_children[0]
        return None

    @asyncer
    def http(self, meth, path_query, data_or_get_headers, headers):
        if not path_query or not len(path_query):
            path_query = [self.page_api]
        else:
            if not isinstance(path_query, Array):
                path_query = [path_query]

            if len(path_query) == 1 and type(path_query[0]) is not String:
                path_query = [None, path_query[0]]

            if not path_query[0]:
                path_query[0] = self.page_api
            elif not RegExp('^(pages-api|/)').exec(path_query[0]):
                path_query[0] = f'{PAGES_API}/{path_query[0]}'

        resp = yield api.http(meth, path_query, data_or_get_headers, headers)
        if self._on_response:
            self._on_reponse.call(None, resp)
        else:
            self.vm.on_response(resp)

    def get(self, *args):
        len_args = len(args)
        path, query, headers = [None, None, None]
        if len_args == 1:
            path = args.pop()
        elif len_args == 2:
            path, query = args
        elif len_args == 3:
            path, query, headers = args
        return self.http('get', [path, query], headers)

    def post(self, *args):
        return self.http('post', *args)

    def remove(self, *args):
        return self.http('delete', *args)

    @asyncer
    def redirect(self, path, query):
        if query is undefined and type(path) is Object:
            query = path
            path = None
        if not path or path == '.':
            path = self.vm.S_route.path
        if path[0] != '/':
            path = '/' + path
        if not query:
            query = {}
        try:
            yield self.vm.S_router.push({'path': path, 'query': query})
        except Exception as err:
            if err._isRouter and err.type != VueRouter.NavigationFailureType.duplicated:
                raise
            self.reload_data()

    def reload_data(self):
        r = self.vm.S_route
        self.get('.' + r.path, r.query)

    def parse_response(self, r):
        payload = r.data or {}
        commands = None
        state_patch = None
        set_state = None
        # axios lowers header names
        if r.headers['x-sparesponse']:
            data = payload.data or {}
            state_patch = payload.state_patch or None
            set_state = payload.set_state or None
            del payload.data
            del payload.state_patch
            del payload.set_state
            commands = payload
        else:
            data = payload
        return {'data': data, 'commands': commands, 'state_patch': state_patch, 'set_state': set_state}

    def apply_response(self, vm, r):
        back = self.parse_response(r)
        store = vm.S_store
        if back.state_patch:
            store.update(back.state_patch)
        if back.set_state:
            set_state = back.set_state
            # check if we have array of arrays
            if not Array.isArray(set_state[0]):
                set_state = [set_state]
            for it in set_state:
                store.set(*it)
        for k in back.data:
            vm[k] = back.data[k]
        for c in (back.commands or []):
            args = back.commands[c]
            if not Array.isArray(args):
                args = [args]
            vm[c].call(vm, *args)

    def on_mounted(self):
        vm = self.vm
        if not self.on_mounted_enabled:
            return

        back = vm.S_back
        store = vm.S_store
        if back.state_patch:
            store.update(back.state_patch)
        if back.set_state:
            set_state = back.set_state
            # check if we have array of arrays
            if not Array.isArray(set_state[0]):
                set_state = [set_state]
            for it in set_state:
                store.set(*it)
        for c in (back.commands or []):
            args = back.commands[c]
            if not Array.isArray(args):
                args = [args]
            vm[c].call(vm, *args)

    def on_response(self, r):
        self.apply_response(self.vm, r)

    @staticmethod
    def vue_mixin():
        def on_response(r):
            vm = this
            vm.S_pu.on_response(r)

        def beforeCreate():
            vm = this
            vm.S_pu = PageUtil(vm)
            meths = vm.S_options.methods
            print('create:', meths)
            if not meths:
                meths = vm.S_options.methods = {}
            if not hasattr(meths, 'on_response'):
                meths['on_response'] = on_response

        return {'beforeCreate': beforeCreate}


@literal
class page_mixin:

    def beforeCreate(self):
        self.S_back = self.S_pu.parse_response(self.S_attrs.pg_response)

    def data(self):
        self.S_pu.on_mounted_enabled = True
        return self.S_back.data

    @literal
    class methods:
        def redirect(self, *args):
            self.S_pu.redirect(*args)

        def alert(self, msg):
            @self.S_nextTick
            def _():
                setTimeout(lambda: alert(msg), 100)

    @literal
    class watch:

        def S_route(self, to_, from_):
            # need to remove root-slash
            page_url = to_.path[1:]
            self.S_pu.get(page_url, to_.query)

    @literal
    class computed:

        def page_api(self):
            return self.S_pu.page_api

        def page_api_root(self):
            return PAGES_API

    def mounted(self):
        self.S_pu.on_mounted()


class DataPreloader:
    def __init__(self):
        # last response and page uri
        self.response = None
        self.page_uri = None
        self._dest_route = None

    @property
    def dest_route(self):
        # read once
        ret = self._dest_route
        self._dest_route = None
        return ret

    @asyncer
    def preload(self, dest_route):
        self._dest_route = dest_route
        page_api_uri = self.page_uri = PAGES_API + dest_route.fullPath
        self.response = None
        self.response = (yield api.get([page_api_uri]))


data_preloader = DataPreloader()


def make_loader(page_component, pages):
    def load_page(ok, err):
        # if data_preloader.dest_route.matched[0].instances[0] is not load_page:
        #    raise
        # make component instance
        pg_module = pages[page_component]
        component = pg_module.make()
        component.mixins = [page_mixin]

        # make a simple wrapper to pass `response` to component via $attrs
        @literal
        class wrapper:
            functional = True

            def render(h, ctx):
                if not ctx.data.attrs:
                    ctx.data.attrs = {}
                ctx.data.attrs.pg_response = data_preloader.response
                return h(component, ctx.data, ctx.children)

        ok(wrapper)
    return load_page


def make_routes(routes_map, pages):
    ret = []
    for templ_url in routes_map:
        for spa_route in routes_map[templ_url]:
            route = spa_route.path
            if route.startsWith('/'):
                route = route[1:]
            if spa_route.is_main_path:
                # make it optional
                route = f'({route})?'
            type_prefix, page_component = templ_url.split(':')
            rec = {
                'path': f'/{route}',
                'meta': spa_route.meta,
                'component': make_loader(page_component, pages),
            }
            ret.push(rec)
    return ret


@asyncer
def data_preloader_guard(dest, cur, next):
    # must be last guard!
    yield data_preloader.preload(dest)
    next()


def make_router(routes_map, pages):
    # nonlocal router
    router = VueRouter({
        'routes': make_routes(routes_map, pages),
        'mode': 'history',
        'base': ENV.app_base,
    })
    return router
