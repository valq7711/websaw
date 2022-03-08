import os
from types import SimpleNamespace
from typing import Dict

from . import globs


class StaticRegistry:

    static_file = staticmethod(globs.static_file)

    class Registered(SimpleNamespace):
        folder: str
        client_apps: set

    mounted: Dict[str, Registered] = {}

    def register(self, base_url, folder, app):
        folder_apps = self.mounted.get(base_url)
        if folder_apps:
            if os.path.samefile(folder_apps.folder, folder):
                raise KeyError(
                    f'URL already in use: {base_url} => path:'
                    f'{folder_apps.folder}'
                )
            folder_apps.client_apps.add(app)
        self.mounted[base_url] = SimpleNamespace(
            folder=folder, client_apps={app}
        )

    def unregister(self, base_url, app):
        reg = self.mounted.get(base_url)
        if not reg:
            return
        reg.client_apps.difference_update({app})
        if not reg.client_apps:
            self.mounted.pop(base_url)

    def get_registered(self, base_url, folder):
        folder_apps = self.mounted.get(base_url)
        if not folder_apps:
            return None
        if os.path.samefile(folder_apps.folder, folder):
            return folder_apps

    def make_rule_and_handler(self, static_base_url: str, folder: str, client_app):
        if not os.path.exists(folder):
            return None, None
        registered = self.get_registered(static_base_url, folder)
        if registered:
            registered.client_apps.add(client_app)
            return None, None

        self.register(static_base_url, folder, client_app)
        if static_base_url.endswith('static'):
            static_base_url = fr'{static_base_url}/<re((_\d+(\.\d+){2}/)?)>'
        elif '/static/' in static_base_url:
            static_base_url = static_base_url.replace('/static/', r'/static/<re((_\d+(\.\d+){2}/)?)>', 1)
        if not static_base_url.endswith(('/', '/)?)>')):
            static_base_url = f'{static_base_url}/'
        rule = f'{static_base_url}<fp.path()>'
        h = self.make_static_handler(folder)
        return rule, h

    @classmethod
    def make_static_handler(cls, folder):
        response = globs.response

        def serve_static(fp):
            response.headers.setdefault("Pragma", "cache")
            response.headers.setdefault("Cache-Control", "private")
            return cls.static_file(fp, root=folder)
        return serve_static

    def __contains__(self, base_url_folder_tuple):
        if isinstance(base_url_folder_tuple, str):
            raise TypeError(
                f'A pair like [url, folder] is required, '
                f'got string: {base_url_folder_tuple}'
            )
        base_url, folder = base_url_folder_tuple
        folder_apps = self.mounted.get(base_url)
        if not folder_apps:
            return False
        return os.path.samefile(folder_apps.folder, folder)


static_registry = StaticRegistry()
