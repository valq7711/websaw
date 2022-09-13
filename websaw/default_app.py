import os
import ombott
import logging

from .error_pages import error_page
from .core.loggers import get_error_snapshot, error_logger
from . import renders

from .core import (
    BaseApp,
    BaseContext,
    Reloader,
    HTTP,
)

from .fixtures import templates
from .fixtures.templates import SPAComponent


class DefaultApp(BaseApp):
    def __init__(self, ctx: BaseContext, *, config=None, name: str = None):
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
            render_map={dict: renders.jsonfy, BaseApp.SPAResponse: renders.spa_response},
            exception_handler=self._exception_handler,
            group_name=None,
        )
        if config:
            cfg.update(config)

        super().__init__(cfg, ctx)

    def use(self, *fixt):
        app_name = self.default_config['app_name']
        fixtures = []
        for fx in fixt:
            if isinstance(fx, str):
                if '#' in fx:
                    fx = SPAComponent(fx.replace('#', ''))
                else:
                    fx = templates.YATLTemplate(
                        fx, path=self.default_config['template_folder'], inject={'mixin_name': app_name}
                    )
            elif isinstance(fx, dict):
                fx = templates.UTemplate(fx)
            fixtures.append(fx)
        return super().use(*fixtures)

    @staticmethod
    def _exception_handler(ctx: BaseContext, exc):
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
