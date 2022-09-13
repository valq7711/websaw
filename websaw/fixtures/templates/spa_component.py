import os

from websaw.core import BaseContext
from websaw.core.fixture import SPAFixture


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
        file_path: str
        if not file_path.startswith(static_folder):
            raise RuntimeError(f'SPA template should be under static folder ({static_folder}): {file_path}')

        rel_static = os.path.relpath(file_path, static_folder)
        return rel_static.replace(os.path.sep, '/')
