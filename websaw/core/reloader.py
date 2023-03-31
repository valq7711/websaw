import sys
import os
import click
import importlib.machinery
import traceback
from typing import Dict
import logging
from pathlib import Path

from .globs import app as om_app
from .utils import module2filename

from .core_events import core_event_bus, CoreEvents


_logger = logging.getLogger('websaw')


def _clear_modules(pckg_name):
    # all files/submodules
    names = [
        name for name in sys.modules
        if (f'{name}.').startswith(f'{pckg_name}.')
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
        pwf = Path(os.environ["WEBSAW_PASSWORD_FILE"])
        if pwf.exists():
            hash = pwf.read_text().strip()
            return hash

    @staticmethod
    def get_apps_folder():
        return Path(os.environ["WEBSAW_APPS_FOLDER"])

    @classmethod
    def package_folder(cls, package_name):
        pdir = Path(sys.modules[package_name].__file__).parent
        return pdir

    @classmethod
    def register_app(cls, app_name: str, app):
        cls.registered_apps[app_name] = app

    @classmethod
    def install_reloader_hook(cls):
        core_event_bus.on(CoreEvents.RELOAD_APPS, cls.reimport_apps)

    @classmethod
    def is_package(self, pth: Path):
        return pth.is_dir() and not pth.name.startswith(('__', '.')) and (pth / '__init__.py').exists()

    @classmethod
    def get_packs_names(cls, folder: Path):
        return [
            p.name for p in folder.iterdir()
            if cls.is_package(p)
        ]

    @classmethod
    def reimport_apps(cls, *app_names: str):
        reload_all = not app_names or {app_names} - {cls.registered_apps}
        apps_folder = cls.get_apps_folder()
        apps_folder_name = apps_folder.name
        if reload_all:
            pack_names = cls.get_packs_names(apps_folder)
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
    def load_package(cls, folder: Path, name_id: str = None):
        if name_id is None:
            name_id = folder.name
        loader = importlib.machinery.SourceFileLoader(name_id, str(folder / "__init__.py"))
        return loader.load_module()

    @classmethod
    def import_apps(cls):
        """Import or reimport modules"""
        apps_folder = cls.get_apps_folder()
        _logger.info(
            f"\n\n\n\n************** Start loading applications from {apps_folder} ******************\n"
        )
        # if first time reload dummy top module
        if not cls.modules:
            cls.load_package(apps_folder)
        # Then load all the apps as submodules
        for pack_name in cls.get_packs_names(apps_folder):
            cls.import_apps_package(pack_name)

    @classmethod
    def import_apps_package(cls, pack_name: str):
        apps_folder = cls.get_apps_folder()
        pack_folder = apps_folder / pack_name
        if not cls.is_package(pack_folder):
            return

        full_pack_name = f"{apps_folder.name}.{pack_name}"
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
                _logger.info(f'(re)loading module: {pack_name}')
                module = cls.load_package(pack_folder, name_id=full_pack_name)
                if hasattr(module, 'websaw_main'):
                    module.websaw_main()
                _logger.info(f'(re)loaded successfully: {pack_name}')
                click.secho(f"\x1b[A[X] loaded {pack_name}       ", fg="green")
            cls.modules[pack_name] = module
            cls.errors[pack_name] = None
        except Exception as err:
            cls.errors[pack_name] = traceback.format_exc()
            _logger.error(f'failed to load {pack_name}:', exc_info=True)
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
