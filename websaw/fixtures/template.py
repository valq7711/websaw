import os

import yatl
from upytl import UPYTL

from ..core import Cache, render, BaseContext, redirect
from ..core.fixture import Fixture, SPAFixture


_HELPERS = {name: getattr(yatl.helpers, name) for name in yatl.helpers.__all__}


class Template(Fixture):

    cache = Cache(100)

    def __init__(self, filename, path=None, delimiters="[[ ]]", inject=None):
        if ':' in filename:
            context_key, filename = filename.split(':')
        else:
            context_key = None
        self.context_key = context_key
        self.with_path_prefix = '/' in filename
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
            env=ctx.env,
            **self.inject,
            **shared_data.get("template_context", {}),
            **output,
        )
        if self.with_path_prefix:
            file_path = self.filename.format(**ctx.env)
            path, filename = os.path.split(file_path)
        else:
            filename = self.filename
            path = self.path or ctx.app_data.template_folder
            file_path = path_join(path, filename)

        if not os.path.exists(file_path):
            raise RuntimeError(f'Template was not found: {file_path}')
        ctx.output = render(
            filename=filename, path=path, context=context, delimiters=self.delimiters
        )


class UTemplate(Fixture):

    def __init__(self, template: dict, inject=None, global_ctx=None):
        self.template = template
        self.global_ctx = global_ctx or {}
        self.inject = inject or {}

    def take_off(self, ctx: BaseContext):
        output = ctx.output
        if not isinstance(output, dict):
            return
        shared_data = ctx.state.shared_data
        context = dict(
            request=ctx.request,
            URL=ctx.URL,
            app_get=ctx.get,
            mixin_get=ctx.mixin_get,
            __vars__=output,
            env=ctx.env,
            **self.inject,
            **shared_data.get("template_context", {}),
            **output,
        )
        u = UPYTL(global_ctx=self.global_ctx)
        ctx.output = u.render(self.template, context)
