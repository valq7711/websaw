import sys
import os
import click
import importlib
import traceback
from typing import Dict

from .globs import app as om_app
from .loggers import error_logger, get_error_snapshot
from .utils import module2filename

from .core_events import core_event_bus, CoreEvents


def _clear_modules(pckg_name):
    # all files/submodules
    names = [
        name for name in sys.modules
        if (name + ".").startswith(pckg_name + ".")
    ]
    for name in names:
        del sys.modules[name]


class Reloader:

    modules = {}
    errors = {}
    registered_apps: Dict[str, object] = {}
    forget_package = staticmethod(_clear_modules)

    @staticmethod
    def read_password_hash():
        """Read admin password hash from WEBSAW_PASSWORD_FILE if exists one."""
        pwf = os.environ["WEBSAW_PASSWORD_FILE"]
        if os.path.exists(pwf):
            with open(pwf, 'r') as f:
                hash = f.read().strip()
            return hash

    @staticmethod
    def get_apps_folder():
        return os.environ["WEBSAW_APPS_FOLDER"]

    @classmethod
    def get_apps_folder_name(cls):
        return os.path.split(cls.get_apps_folder())[-1]

    @classmethod
    def package_folder(cls, package_name):
        pdir = os.path.dirname(sys.modules[package_name].__file__)
        return pdir

    @classmethod
    def package_folder_path(cls, package_name, *parts):
        return os.path.join(cls.package_folder(package_name), *parts)

    @classmethod
    def register_app(cls, app_name, app):
        cls.registered_apps[app_name] = app

    @classmethod
    def install_reloader_hook(cls):
        core_event_bus.on(CoreEvents.RELOAD_APPS, cls.reimport_apps)

    @classmethod
    def reimport_apps(cls, *app_names):
        reload_all = not app_names or set(app_names) - set(cls.registered_apps)
        apps_folder_name = cls.get_apps_folder_name()
        if reload_all:
            pack_names = os.listdir(cls.get_apps_folder())
        else:
            pack_names = app_names
        for pack_name in pack_names:
            app = cls.registered_apps.pop(pack_name, None)
            if app is not None:
                app.unmount()
            cls.forget_package(f"{apps_folder_name}.{pack_name}")
        for pack_name in pack_names:
            cls.import_apps_package(pack_name)

    @classmethod
    def import_apps(cls):
        """Import or reimport modules"""
        folder = cls.get_apps_folder()
        # if first time reload dummy top module
        if not cls.modules:
            path = os.path.join(folder, "__init__.py")
            loader = importlib.machinery.SourceFileLoader("apps", path)
            loader.load_module()
        # Then load all the apps as submodules
        for pack_name in os.listdir(folder):
            cls.import_apps_package(pack_name)

    @classmethod
    def import_apps_package(cls, pack_name: str):
        folder = cls.get_apps_folder()
        path = os.path.join(folder, pack_name)
        init = os.path.join(path, "__init__.py")

        if not (
            not pack_name.startswith("__")
            and os.path.isdir(path)
            and os.path.exists(init)
        ):
            return

        apps_folder_name = cls.get_apps_folder_name()
        full_pack_name = f"{apps_folder_name}.{pack_name}"
        is_loaded = full_pack_name in sys.modules
        try:
            module = cls.modules.get(pack_name)
            if module is None:
                if is_loaded:
                    click.secho(f"[X] already loaded {pack_name}       ", fg="green")
                else:
                    click.echo(f"[ ] loading {pack_name} ...")
            else:
                if is_loaded:
                    click.secho(f"[X] already reloaded {pack_name}       ", fg="green")
                else:
                    click.echo(f"[ ] reloading {pack_name} ...")
                    # forget the module
                    del cls.modules[pack_name]

            if not is_loaded:
                module = importlib.machinery.SourceFileLoader(full_pack_name, init).load_module()
                if hasattr(module, 'websaw_main'):
                    module.websaw_main()
                click.secho(f"\x1b[A[X] loaded {pack_name}       ", fg="green")
            cls.modules[pack_name] = module
            cls.errors[pack_name] = None
        except Exception as err:
            cls.errors[pack_name] = traceback.format_exc()
            error_logger.log(
                pack_name, get_error_snapshot()
            )
            click.secho(
                f"\x1b[A[FAILED] loading {pack_name} ({err})",
                fg="red",
            )
            # clear all files/submodules if the loading fails
            cls.forget_package(full_pack_name)

    @classmethod
    def get_registered_routes(cls):
        routes = []
        apps_folder = cls.get_apps_folder()
        for route in om_app.routes.values():
            for method, method_obj in route.methods.items():
                func = method_obj.handler
                rule = route.rule
                routes.append(
                    {
                        "rule": rule,
                        "method": method,
                        "filename": module2filename(func.__module__, apps_folder),
                        "action": func.__name__,
                    }
                )
        return [*sorted(routes, key=lambda item: item["rule"])]
