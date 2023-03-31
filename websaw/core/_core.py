from . import globs
from .core_events import core_event_bus, CoreEvents
from .install import install_args
from .reloader import Reloader


__all__ = (
    'import_apps',
    'reload_apps',
    'wsgi',
)


def import_apps():
    core_event_bus.emit(CoreEvents.BEFORE_APPS_LOAD)
    Reloader.import_apps()
    core_event_bus.emit(CoreEvents.APPS_LOADED)


@core_event_bus.on(CoreEvents.RELOAD_APPS)
def reload_apps(*app_names):
    Reloader.reimport_apps(*app_names)
    core_event_bus.emit(CoreEvents.APPS_LOADED)


def wsgi(**kwargs):
    """Initializes everything, loads apps, returns the wsgi app"""
    install_args(kwargs)
    import_apps()
    return globs.app
