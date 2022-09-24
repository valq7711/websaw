import os

from upytl import UPYTL

from websaw.core import BaseContext
from websaw.core.fixture import Fixture


class UTemplate(Fixture):

    def __init__(self, template: dict, inject=None, global_ctx=None):
        self.template = template
        self.global_ctx = global_ctx or {}
        self.inject = inject or {}

    def take_off(self, ctx: BaseContext):
        output = ctx.output
        if not isinstance(output, dict):
            return
        env = ctx.env
        context = dict(
            request=ctx.request,
            URL=ctx.URL,
            app_get=ctx.get,
            mixin_get=ctx.mixin_get,
            __vars__=output,
            env=env,
            **self.inject,
            **env.get("default_template_context", {}),
            **output,
        )
        u = UPYTL(global_ctx={'URL': ctx.URL})
        ctx.output = u.render(self.template, context, indent=0)
