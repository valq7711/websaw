import threading
from types import SimpleNamespace
from typing import Optional


class Fixture:

    _local = threading.local()
    is_hook = False
    context_key: Optional[str]

    @classmethod
    def initialize_safe_storage(cls):
        cls._local.fixtures_data = {}

    @classmethod
    def prepare_for_use(cls, f):
        cls._local.fixtures_data[f] = SimpleNamespace()

    @property
    def data(self) -> SimpleNamespace:
        return self._local.fixtures_data[self]

    def app_mounted(self, ctx):
        ...

    def take_on(self, ctx):
        ...

    def take_off(self, ctx):
        ...
