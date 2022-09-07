import os

import yatl
from upytl import UPYTL

from ..core import Cache, render, BaseContext
from ..core.fixture import Fixture, SPAFixture


_HELPERS = {name: getattr(yatl.helpers, name) for name in yatl.helpers.__all__}


class Template(Fixture):

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


class SPAComponent(SPAFixture):

    def __init__(self, component_or_file_name: str, path: str = None):
        self.component = None
        self.path = path
        self.filename = None
        self.with_path_prefix = False
        self.context_key = None

        if ':' in component_or_file_name:
            context_key, component_or_file_name = component_or_file_name.split(':')
        else:
            context_key = None
        self.context_key = context_key

        if component_or_file_name.endswith(('.html', '.js')):
            filename = component_or_file_name
            self.with_path_prefix = '/' in filename
            self.filename = filename
        else:
            self.component = component_or_file_name

    def make_component_reference(self, ctx: BaseContext, prefix: str):
        if self.component is not None:
            return f"component:{self.component}"
        templ_url = self._make_static_tail_url(ctx)
        prefix = prefix.rstrip('/')
        if prefix:
            prefix = f'{prefix}/'
        return f"url:{prefix}{templ_url}"

    def _make_static_tail_url(self, ctx: BaseContext):
        '''
        Return the tail of the static url, which must be prefixed with
        `{app}/static/` or `{app}/static/{mxn}/`
        '''
        if self.component is not None:
            raise RuntimeError(f'This one points to the component `{self.component}`, not a file')

        path_join = os.path.join
        if self.with_path_prefix:
            file_path = self.filename.format(**ctx.env)
            path, filename = os.path.split(file_path)
        else:
            filename = self.filename
            path = self.path or ctx.app_data.spa_template_folder
            file_path = path_join(path, filename)

        if not os.path.exists(file_path):
            raise RuntimeError(f'Template was not found: {file_path}')

        file_path, static_folder = [os.path.normpath(p) for p in (file_path, ctx.app_data.static_folder)]
        if not file_path.startswith(static_folder):
            raise RuntimeError(f'SPA template should be under static folder ({static_folder}): {file_path}')

        rel_static = os.path.relpath(file_path, static_folder)
        return rel_static.replace(os.path.sep, '/')
