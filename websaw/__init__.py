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
    Session,
    DAL,
    URL,
    XAuth,
    AuthGuard,
    AuthErr,
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
    'Session',
    'DAL',
    'Field',

    'HTTP',
    'WebsawException',

    'XAuth',
    'AuthGuard',
    'AuthErr'
)

__author__ = "Kucherov Valery <valq7711@gmail.com>"
__license__ = "MIT"
__version__ = "0.0.6"


def _maybe_gevent():
    for arg in sys.argv[1:]:
        if 'gevent' in arg.lower():
            from gevent import monkey
            monkey.patch_all()
            break
_maybe_gevent()  # noqa


class DefaultContext(BaseContext):
    session = Session()
    URL = URL()
    auth_guard = AuthGuard()


class DefaultApp(BaseApp):
    def __init__(self, ctx: BaseContext):
        pjoin = os.path.join
        app_name = Reloader.current_import_app
        folder = pjoin(Reloader.get_apps_folder(), app_name)
        static_folder = pjoin(folder, 'static')
        template_folder = pjoin(folder, 'templates')

        cfg = dict(
            base_url=f'/{app_name}',
            static_base_url=f'/{app_name}',
            folder=folder,
            static_folder=static_folder,
            template_folder=template_folder,
            render_map={dict: jsonfy},
            exception_handler=_default_exception_handler,
        )

        super().__init__(cfg, ctx)

    def use(self, *fixt):
        return super().use(*[
            Template(f) if isinstance(f, str) else f
            for f in fixt
        ])


def jsonfy(ctx: BaseContext, dct):
    ctx.response.headers['Content-Type'] = 'application/json'
    return json.dumps(dct, sort_keys=True, indent=2, ensure_ascii=False)


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
