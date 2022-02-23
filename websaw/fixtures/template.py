import os

import yatl

from ..core import Cache, render, BaseContext
from ..core.fixture import Fixture


_HELPERS = {name: getattr(yatl.helpers, name) for name in yatl.helpers.__all__}


class Template(Fixture):

    cache = Cache(100)

    def __init__(self, filename, path=None, delimiters="[[ ]]"):
        self.context_key = filename
        self.filename = filename
        self.path = path
        self.delimiters = delimiters

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
            __vars__=output,
            **shared_data.get("template_context", {}),
            **output,
        )
        path = self.path or ctx.app_data.template_folder
        filename = path_join(path, self.filename)
        if not os.path.exists(filename):
            generic_filename = path_join(path, "generic.html")
            if os.path.exists(generic_filename):
                filename = generic_filename
        ctx.output = render(
            filename=filename, path=path, context=context, delimiters=self.delimiters
        )
