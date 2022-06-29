import sys
import os
import json
import ombott
import logging

from websaw.core.loggers import get_error_snapshot, error_logger
from .error_pages import error_page

from .core import (
    request,
    response,
    abort,

    import_apps,
    reload_apps,
    wsgi,
    BaseApp,
    BaseContext,
    Reloader,

    redirect,
    Cache,

    HTTP,
    WebsawException,
)

from .fixtures import (
    Template,
    SPAComponent,
    Session, GroupSession,
    DAL,
    URL,
    XAuth,
    AuthGuard,
    AuthErr,
    CurrentUser,
    Env,
)

from pydal import Field

__all__ = (
    'request',
    'response',
    'abort',

    'import_apps',
    'reload_apps',
    'wsgi',
    'BaseApp',
    'BaseContext',

    'URL',
    'redirect',
    'Cache',

    'Template',
    'SPAComponent',
    'Session', 'GroupSession',
    'DAL',
    'Field',

    'HTTP',
    'WebsawException',

    'XAuth',
    'AuthGuard',
    'AuthErr',
    'CurrentUser',

    'Env',
)

__author__ = "Kucherov Valery <valq7711@gmail.com>"
__license__ = "MIT"
__version__ = "0.0.8"


def _maybe_gevent():
    for arg in sys.argv[1:]:
        if 'gevent' in arg.lower():
            from gevent import monkey
            monkey.patch_all()
            break
_maybe_gevent()  # noqa


class DefaultContext(BaseContext):
    group_session = GroupSession()
    session = Session()
    URL = URL()
    auth_guard = AuthGuard()
    current_user = CurrentUser()


class DefaultApp(BaseApp):
    def __init__(self, ctx: BaseContext, config=None, *, name=None):
        if name is None:
            if self.__class__ is DefaultApp:
                raise ValueError(
                    f"{self.__class__} can't be directly instantiated without 'name' argument"
                )
            name = self.__package__
        name_split = name.split('.')
        app_name = name_split[-1]

        pjoin = os.path.join
        folder = Reloader.package_folder(name)
        static_folder = pjoin(folder, 'static')
        template_folder = pjoin(folder, 'templates')
        spa_template_folder = pjoin(static_folder, 'spa', 'pages')

        cfg = dict(
            app_name=app_name,
            base_url=f'/{app_name}',
            static_base_url=f'/{app_name}',
            folder=folder,
            static_folder=static_folder,
            template_folder=template_folder,
            spa_template_folder=spa_template_folder,
            render_map={dict: jsonfy, BaseApp.SPAResponse: spa_response},
            exception_handler=_default_exception_handler,
            group_name=None,
        )
        if config:
            cfg.update(config)

        super().__init__(cfg, ctx)

    def use(self, *fixt):
        return super().use(*[
            self._str_to_template(f, self) if isinstance(f, str) else f
            for f in fixt
        ])

    @staticmethod
    def _str_to_template(templ: str, app: 'DefaultApp'):
        if '#' in templ:
            templ = templ.replace('#', '')
            return SPAComponent(templ)
        template_folder = app.default_config['template_folder']
        app_name = app.default_config['app_name']
        return Template(templ, path=template_folder, inject={'mixin_name': app_name})


def jsonfy(ctx: BaseContext, dct):
    ctx.response.headers['Content-Type'] = 'application/json'
    return json.dumps(dct, sort_keys=True, indent=2, ensure_ascii=False, default=str)


def spa_response(ctx: BaseContext, dct):
    ret = jsonfy(ctx, dct)
    ctx.response.headers['X-SPAResponse'] = True
    return ret


def _default_exception_handler(ctx: BaseContext, exc):
    response = ctx.response
    try:
        raise exc
    except HTTP as http:
        response.status = http.status
        ret = getattr(http, "body", "")
        http_headers = getattr(http, 'headers', None)
        if http_headers:
            response.headers.update(http_headers)
        ctx.output = ret
    except ombott.HTTPResponse as resp:
        ctx.output = resp
    except Exception:
        snapshot = get_error_snapshot()
        logging.error(snapshot["traceback"])
        ticket_uuid = error_logger.log(ctx.app_data.app_name, snapshot) or "unknown"
        ctx.output = ombott.HTTPResponse(
            body=error_page(
                500,
                button_text=ticket_uuid,
                href="/_dashboard/ticket/" + ticket_uuid,
            ),
            status=500,
        )
