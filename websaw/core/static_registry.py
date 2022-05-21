import os
from typing import Dict, Callable

from . import globs


class StaticRegistry:

    static_file = staticmethod(globs.static_file)

    folder_handler_map: Dict[str, Callable] = {}

    @classmethod
    def get_hahdler(cls, folder: str):
        if not os.path.isdir(folder):
            return
        folder = os.path.abspath(folder)
        h = cls.folder_handler_map.get(folder)
        if h is None:
            h = cls.folder_handler_map[folder] = cls.make_static_handler(folder)
        return h

    @classmethod
    def make_rule_and_handler(cls, static_base_url: str, folder: str):
        h = cls.get_hahdler(folder)
        if h is None:
            return None, None
        static_ver_rex = r'<re((_\d+(\.\d+){2}/)?)>'
        if static_base_url.endswith('static'):
            static_base_url = f'{static_base_url}/{static_ver_rex}'
        elif '/static/' in static_base_url:
            static_base_url = static_base_url.replace('/static/', f'/static/{static_ver_rex}', 1)
        if not static_base_url.endswith(('/', '/)?)>')):
            static_base_url = f'{static_base_url}/'
        rule = f'{static_base_url}<fp.path()>'
        return rule, h

    @classmethod
    def make_static_handler(cls, folder):
        response = globs.response

        def serve_static(fp):
            response.headers.setdefault("Pragma", "cache")
            response.headers.setdefault("Cache-Control", "private")
            return cls.static_file(fp, root=folder)
        return serve_static
