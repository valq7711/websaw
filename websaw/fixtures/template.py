import os

import yatl

from ..core import Cache, render, BaseContext
from ..core.fixture import Fixture


_HELPERS = {name: getattr(yatl.helpers, name) for name in yatl.helpers.__all__}


class Template(Fixture):

    cache = Cache(100)

    def __init__(self, filename, path=None, delimiters="[[ ]]", inject=None):
        if ':' in filename:
            context_key, filename = filename.split(':')
        else:
            context_key = None
        self.context_key = context_key
        self.filename = filename
        self.path = path
        self.delimiters = delimiters
        self.inject = inject or {}

    def take_off(self, ctx: BaseContext):
        output = ctx.output
        if not isinstance(output, dict):
            return
        shared_data = ctx.state.shared_data
        path_join = os.path.join

        context = dict(
            _HELPERS,
            request=ctx.request,
            URL=ctx.URL,
            app_get=ctx.get,
            mixin_get=ctx.mixin_get,
            __vars__=output,
            **self.inject,
            **shared_data.get("template_context", {}),
            **output,
        )
        path = self.path or ctx.env.get('template_folder') or ctx.app_data.template_folder
        filename = path_join(path, self.filename)
        if not os.path.exists(filename):
            generic_filename = path_join(path, "generic.html")
            if os.path.exists(generic_filename):
                filename = generic_filename
        ctx.output = render(
            filename=filename, path=path, context=context, delimiters=self.delimiters
        )
