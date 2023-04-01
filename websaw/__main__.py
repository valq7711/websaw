import sys
from websaw.cli import cli


def _maybe_gevent():
    for arg in sys.argv[1:]:
        if 'gevent' in arg.lower():
            from gevent import monkey
            monkey.patch_all()
            break


_maybe_gevent()
cli()
