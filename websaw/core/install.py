import sys
import os
import click
import uuid
import logging
import logging.config
from pathlib import Path

from .globs import current_config
from .loggers import error_logger


def _process_apps_folder(apps_folder: Path, confirmed=False):
    if not apps_folder.exists():
        if confirmed or click.confirm(f"Create missing folder {apps_folder}?"):
            apps_folder.mkdir(parents=True)
            confirmed = True
        else:
            click.echo("Command aborted")
            sys.exit(0)

    _process_init_missing(apps_folder, confirmed)


def _process_init_missing(apps_folder: Path, confirmed=False):
    init_py = apps_folder / "__init__.py"
    if not init_py.exists():
        if confirmed or click.confirm(f"Create missing init file {init_py}?"):
            init_py.touch()
        else:
            click.echo("Command aborted")
            sys.exit(0)


def _get_session_secret(service_folder: Path):
    if not service_folder.exists():
        service_folder.mkdir(parents=True)
    session_secret_file = service_folder / "session.secret"
    if not session_secret_file.exists():
        session_secret_file.write_text(str(uuid.uuid4()))
    session_secret = session_secret_file.read_text()
    return session_secret


def install_args(kwargs, reinstall_apps=False):

    config = current_config

    apps_folder = config.apps_folder = Path(config.apps_folder).absolute().resolve()
    config.service_folder = apps_folder / config.service_folder
    config.password_file = Path(config.password_file).absolute().resolve()

    for key, val in config.items():
        os.environ[f"WEBSAW_{key.upper()}"] = str(val)

    yes_to_all = kwargs.get("yes", False)

    # If the apps folder does not exist create it and populate it
    _process_apps_folder(apps_folder, confirmed=yes_to_all)

    # ensure service stuff
    config.session_secret = _get_session_secret(config.service_folder)

    # ensure that "import <apps_folder.name>.someapp" works
    apps_folder_parent = str(apps_folder.parent)
    if str(apps_folder_parent) not in sys.path:
        sys.path.insert(0, apps_folder_parent)

    # loggers
    error_logger.initialize()  # TODO
    log_config = apps_folder / 'logging.conf'
    if log_config.is_file():
        logging.config.fileConfig(str(log_config))
    else:
        log_file = str(apps_folder / 'websaw.log')
        logging.basicConfig(
            format='%(asctime)s %(name)s %(threadName)s %(levelname)s: %(message)s',
            filename=log_file,
            level=logging.DEBUG
        )
