from pyjsaw.typing.jstyping import window, literal
from pyjsaw.typing.vuetyping import Vue, VueRouter
from pyjsaw.pyjs.vcollector import vc

from asset import spa_bundle, spa_tools

import components
import pages
from store import AppStore


spa_bundle.register_components(Vue, components)

store = AppStore()

Vue.prototype.S_store = store

spa_tools.PageUtil.set_headers_getter(
    lambda: {'x-api-token': store.get('api_token')}
)


Vue.mixin(spa_tools.PageUtil.vue_mixin())

# SPA_ROUTES comes from spa_main_routes.js


@vc.component()
class App:

    def render(self, h):
        return h('router-view')

    @literal
    class _extra:
        router = spa_tools.make_router(SPA_ROUTES, pages)


Vue.use(VueRouter)


def auth_guard(dst, src, next):
    if dst.meta == 'requires_login' and not store.get('user').name:
        next({'path': '/login', 'query': {'next': dst.fullPath}})
    else:
        next()


App.router.beforeEach(auth_guard)
App.router.beforeEach(spa_tools.data_preloader_guard)  # must be last guard

app = window.app = Vue(App)

__all__ = [app]
