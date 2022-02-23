import os
from types import SimpleNamespace


class ConfigSetter:
    def __init__(self, keys_class, defaults_factory=None, novalue=None):
        self.novalue = novalue
        self.defaults_factory = defaults_factory
        self.keys = {
            k for k in keys_class.__dict__
            if not k.startswith('_')
        }

    def extend(self, dst, src, optional_keys=None, get_default=None):
        self.apply(dst, src, optional_keys, get_default, extend_mode=False)

    def apply(self, dst, src, optional_keys=None, get_default=None, extend_mode=False):
        optional_keys = optional_keys or set()
        if get_default is None:
            if self.defaults_factory:
                get_default = self.defaults_factory(src).get
            else:
                get_default = {}.get

        no_value = self.novalue
        if isinstance(src, dict):
            get = src.get
        else:
            def get(k, default=None):
                return getattr(src, k, default)

        for k in self.keys:
            v = get(k, no_value)
            if extend_mode and v is not no_value:
                continue
            if v is no_value:
                try:
                    v = get_default(k)
                except KeyError:
                    if k in optional_keys:
                        continue
                    raise KeyError(f'Missing key: {k}')

            setattr(dst, k, v)

    def dict_from(self, src, get_default=None):
        defaults = get_default or {}.get
        ret = {}
        no_value = self.novalue
        for k in self.keys:
            v = getattr(src, k, no_value)
            if v is no_value:
                v = defaults(k, no_value)
            if v is no_value:
                raise KeyError(f'Missing key: {k}')
            ret[k] = v


class AppConfigKeys:
    folder = None

    # optional
    base_url = None
    static_base_url = None
    static_version = None

    static_folder = None
    template_folder = None


class AppConfig(AppConfigKeys):
    def __getitem__(s, k):
        return getattr(s, k)

    def __setitem__(s, k, v):
        return setattr(s, k, v)

    def get(s, k, d=None):
        return getattr(s, k, d)


class AppConfigDefaultsFactory:
    base_url = None
    static_version = '0.0.1'

    def __init__(self, src):
        if isinstance(src, dict):
            src = SimpleNamespace(**src)
        self.src = src

    def static_base_url(self):
        ret = getattr(self.src, 'base_url', None)
        return ret

    def folder(self):
        # to allow to use for static/template folders
        folder = getattr(self.src, 'folder', None)
        if folder is None:
            folder = '.'
        return folder

    def static_folder(self):
        return os.path.join(self.folder(), 'static')

    def template_folder(self):
        return os.path.join(self.folder(), 'templates')

    def get(self, k):
        no_value = []
        attr = getattr(self, k, no_value)
        if attr is no_value:
            raise KeyError(f'{k}')
        return attr() if callable(attr) else attr


_config_setter = ConfigSetter(AppConfigKeys, AppConfigDefaultsFactory)

