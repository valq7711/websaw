from typing import List

from ..core.fixture import Fixture


class DBRegistry(Fixture):
    """
    This fixture is intended to use in `db_admin`-like mixin.
    It allows db-fixtures to perform self-registration in db_admin mixin.
    """
    def __init__(self):
        self._db_keys = set()

    def register(self, fixture_key: str):
        """Register db-fixture."""
        self._db_keys.add(fixture_key)

    @property
    def db_keys(self) -> List[str]:
        """Return a set of db-fixtures keys registered in this registry."""
        return {*self._db_keys}
