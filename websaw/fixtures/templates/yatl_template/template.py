import os

import yatl

from websaw.core import Cache, BaseContext
from websaw.core.fixture import Fixture

from .render import render


_HELPERS = {name: getattr(yatl.helpers, name) for name in yatl.helpers.__all__}


class YATLTemplate(Fixture):

    cache = Cache(100)

    def __init__(self, filename: str, path: str = None, delimiters="[[ ]]", inject: dict = None):
        if ':' in filename:
            context_key, filename = filename.split(':')
        else:
            context_key = None
        self.context_key = context_key
        self.with_path_prefix = '/' in filename
        if self.with_path_prefix and filename.startswith('.'):
            filename = '{}' + filename[1:]  # `./`-> `{}/`
        self.filename = filename
        self.path = path
        self.delimiters = delimiters
        self.inject = inject or {}

    def take_off(self, ctx: BaseContext):
        output = ctx.output
        if not isinstance(output, dict):
            return
        path_join = os.path.join

        env = ctx.env
        context = dict(
            _HELPERS,
            request=ctx.request,
            URL=ctx.URL,
            app_get=ctx.get,
            mixin_get=ctx.mixin_get,
            __vars__=output,
            env=env,
            **self.inject,
            **env.get("template_context", {}),
            **output,
        )

        template_folder = ctx.app_data.template_folder
        if self.with_path_prefix:
            file_path = self.filename.format(template_folder, **ctx.env)
            path, filename = os.path.split(file_path)
        else:
            filename = self.filename
            path = self.path or template_folder
            file_path = path_join(path, filename)

        if not os.path.exists(file_path):
            raise RuntimeError(f'Template was not found: {file_path}')
        ctx.output = render(
            filename=filename, path=path, context=context, delimiters=self.delimiters
        )
