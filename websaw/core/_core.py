from . import globs
from .core_events import core_event_bus, CoreEvents
from .install import install_args
from .reloader import Reloader


__all__ = (
    'import_apps',
    'reload_apps',
    'wsgi',
)


def import_apps(pyjsaw_installed):
    core_event_bus.emit(CoreEvents.BEFORE_APPS_LOAD)

    Reloader.import_apps()
    if pyjsaw_installed is not None:
        if 'pyjsaw' in Reloader.modules:
            # we have apps/pyjsaw
            # forget pyjsaw_installed
            Reloader.forget_package('pyjsaw')
        else:
            pyjsaw_installed.websaw_main()

    core_event_bus.emit(CoreEvents.APPS_LOADED)


@core_event_bus.on(CoreEvents.RELOAD_APPS)
def reload_apps(*app_names):
    Reloader.reimport_apps(*app_names)
    core_event_bus.emit(CoreEvents.APPS_LOADED)


def wsgi(**kwargs):
    """Initializes everything, loads apps, returns the wsgi app"""
    install_args(kwargs)
    try:
        import pyjsaw
    except ImportError:
        pyjsaw = None
    import_apps(pyjsaw)
    return globs.app
