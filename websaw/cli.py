"""WEBSAW - a web framework for rapid development with pleasure"""

import os
import click
import sys
import platform
import json
import pydal
import zipfile
import signal
import logging
import ombott
import inspect

from .watcher import watch

# Optional web servers for speed
try:
    import gunicorn
except ImportError:
    gunicorn = None

from .core.install import install_args
from .core import import_apps
from . import server_adapters
from .core import globs
from .core.reloader import Reloader


WEBSAW_CMD = sys.argv[0]

ART = r"""
                   __
  ___     ______  / /_  _________ __      __
  | | /| / /> _ \/ __ \/ ___/ __ `/ | /| / />
  | |/ |/ />  __/ /_/ (__  ) /_/ /| |/ |/ />
  |__/|__/>\___/_.___/____/\__,_/ |__/|__/>

it is just the beginning...
"""

#########################################################################################
# CLI
#########################################################################################

__ssl__ = __import__("ssl")
_ssl = getattr(__ssl__, "_ssl") or getattr(__ssl__, "_ssl2")





def keyboardInterruptHandler(signal, frame):
    """Catch interrupts like Ctrl-C"""
    click.echo(
        "KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal)
    )
    sys.exit(0)


@click.group(
    context_settings=dict(help_option_names=["-h", "-help", "--help"]),
    help=f'{__doc__}\n\nType "{WEBSAW_CMD} COMMAND -h" for available options on commands'
)
def cli():
    pass


@cli.command()
@click.argument("apps_folder")
@click.option(
    "-Y",
    "--yes",
    is_flag=True,
    default=False,
    help="No prompt, assume yes to questions",
    show_default=True,
)
def setup(**kwargs):
    """Setup new apps folder or reinstall it"""
    install_args(kwargs, reinstall_apps=True)


@cli.command()
@click.argument("apps_folder", type=click.Path(exists=True))
@click.argument("func")
@click.option(
    "-Y",
    "--yes",
    is_flag=True,
    default=False,
    help="No prompt, assume yes to questions",
    show_default=True,
)
@click.option(
    "--args",
    default="{}",
    help="Arguments passed to the program/function",
    show_default=True,
)
def call(apps_folder, func, yes, args):
    """Call a function inside apps_folder"""
    kwargs = json.loads(args)
    install_args(dict(apps_folder=apps_folder, yes=yes))
    apps_folder_name = os.path.basename(os.environ["WEBSAW_APPS_FOLDER"])
    module, name = ("%s.%s" % (apps_folder_name, func)).rsplit(".", 1)
    env = {}
    exec("from %s import %s" % (module, name), {}, env)
    env[name](**kwargs)


@cli.command(name="set_password")
@click.option(
    "--password",
    prompt=True,
    confirmation_prompt=True,
    hide_input=True,
    help="Password value (asked if missing)",
)
@click.option(
    "-p",
    "--password_file",
    default="password.txt",
    help="File for the encrypted password",
    show_default=True,
)
def set_password(password, password_file):
    """Set administrator's password"""
    click.echo('Storing the hashed password in file "%s"\n' % password_file)
    with open(password_file, "w") as fp:
        fp.write(str(pydal.validators.CRYPT()(password)[0]))


@cli.command(name="new_app")
@click.argument("apps_folder")
@click.argument("app_name")
@click.option(
    "-Y",
    "--yes",
    is_flag=True,
    default=False,
    help="No prompt, assume yes to questions",
    show_default=True,
)
@click.option(
    "-s",
    "--scaffold_zip",
    default=None,
    help="Path to the zip with the scaffolding app",
    show_default=False,
)
def new_app(apps_folder, app_name, yes, scaffold_zip):
    """Create a new app copying the scaffolding one"""
    install_args(dict(apps_folder=apps_folder, yes=yes))
    source = scaffold_zip or os.path.join(
        os.path.dirname(__file__), "assets", "websaw.app._scaffold.zip"
    )
    target_dir = os.path.join(os.environ["WEBSAW_APPS_FOLDER"], app_name)
    if not os.path.exists(source):
        click.echo("Source app %s does not exists" % source)
        sys.exit(1)
    elif os.path.exists(target_dir):
        click.echo("Target folder %s already exists" % target_dir)
        sys.exit(1)
    else:
        zfile = zipfile.ZipFile(source, "r")
        zfile.extractall(target_dir)
        zfile.close()


@cli.command()
@click.argument("apps_folder", type=click.Path(exists=True))
@click.option(
    "-Y",
    "--yes",
    is_flag=True,
    default=False,
    help="No prompt, assume yes to questions",
    show_default=True,
)
@click.option("-H", "--host", default="127.0.0.1", help="Host name", show_default=True)
@click.option(
    "-P", "--port", default=8000, type=int, help="Port number", show_default=True
)
@click.option(
    "-p",
    "--password_file",
    default="password.txt",
    help="File for the encrypted password",
    show_default=True,
)
@click.option(
    "-s",
    "--server",
    default="default",
    type=click.Choice(
        ["default", "wsgiref", "gunicorn", "gevent", "waitress"]
        + server_adapters.__all__
    ),
    help="server to use",
    show_default=True,
)
@click.option(
    "-w",
    "--number_workers",
    default=0,
    type=int,
    help="Number of workers",
    show_default=True,
)
@click.option(
    "-d",
    "--admin_mode",
    default="full",
    help="Admin mode: demo, readonly, full, none",
    show_default=True,
)
@click.option(
    "--watch",
    default="lazy",
    type=click.Choice(["off", "sync", "lazy"]),
    help="Watch python changes and reload apps automatically, modes: off, sync, lazy",
    show_default=True,
)
@click.option(
    "--ssl_cert", type=click.Path(exists=True), help="SSL certificate file for HTTPS"
)
@click.option("--ssl_key", type=click.Path(exists=True), help="SSL key file for HTTPS")
def run(**kwargs):
    """Run all the applications on apps_folder"""
    install_args(kwargs)

    from . import __version__

    click.secho(ART, fg="cyan")
    click.echo("Websaw: %s on Python %s\n\n" % (__version__, sys.version))

    # If we know where the password is stored, read it, otherwise ask for one
    try:
        import pyjsaw
        click.echo(f"Found pyjsaw {pyjsaw.__version__} installed!")
    except ImportError:
        pyjsaw = None

    pyjsaw_installed = pyjsaw is not None or os.path.exists(os.path.join(globs.current_config.apps_folder, "pyjsaw"))
    if pyjsaw_installed:
        if not (kwargs["admin_mode"] in ("full", "readonly") and Reloader.read_password_hash() is not None):
            click.echo(
                'You have not set an admin password. Run "%s set_password" to do so.'
                % WEBSAW_CMD
            )
        else:
            click.echo(
                "Pyjsaw is at: http://%s:%s/pyjsaw"
                % (kwargs["host"], kwargs["port"])
            )

    # Start
    import_apps(pyjsaw)
    start_server(kwargs)


def start_server(kwargs):
    host = kwargs["host"]
    port = int(kwargs["port"])
    apps_folder = kwargs["apps_folder"]
    number_workers = kwargs["number_workers"]
    params = dict(host=host, port=port, reloader=False)
    server_config = dict(
        platform=platform.system().lower(),
        server=None if kwargs["server"] == "default" else kwargs["server"],
        number_workers=number_workers,
    )

    if not server_config["server"]:
        if server_config["platform"] == "windows" or number_workers < 2:
            server_config["server"] = "rocket"
        else:
            if not gunicorn:
                logging.error("gunicorn not installed")
                return
            server_config["server"] = "gunicorn"

    # Catch interrupts like Ctrl-C if needed
    if server_config["server"] not in {"rocket", "wsgirefWsTwistedServer"}:
        signal.signal(signal.SIGINT, keyboardInterruptHandler)

    params["server"] = server_config["server"]
    if params["server"] in server_adapters.__all__:
        params["server"] = getattr(server_adapters, params["server"])()
    if number_workers > 1:
        params["workers"] = number_workers
    if server_config["server"] == "gunicorn":
        sys.argv[:] = sys.argv[:1]  # else break gunicorn
    if kwargs["ssl_cert"] is not None:
        params["certfile"] = kwargs["ssl_cert"]
        params["keyfile"] = kwargs["ssl_key"]

    if server_config["server"] == "gevent":
        if not hasattr(_ssl, "sslwrap"):
            _ssl.sslwrap = new_sslwrap

    if kwargs["watch"] != "off":
        watch(apps_folder, server_config, kwargs["watch"])
    ombott.run(**params)


def new_sslwrap(
    sock,
    server_side=False,
    keyfile=None,
    certfile=None,
    cert_reqs=__ssl__.CERT_NONE,
    ssl_version=__ssl__.PROTOCOL_SSLv23,
    ca_certs=None,
    ciphers=None,
):
    context = __ssl__.SSLContext(ssl_version)
    context.verify_mode = cert_reqs or __ssl__.CERT_NONE
    if ca_certs:
        context.load_verify_locations(ca_certs)
    if certfile:
        context.load_cert_chain(certfile, keyfile)
    if ciphers:
        context.set_ciphers(ciphers)
    caller_self = inspect.currentframe().f_back.f_locals["self"]
    return context._wrap_socket(sock, server_side=server_side, ssl_sock=caller_self)
