from .core import BaseContext

from .fixtures import (
    Session, GroupSession,
    URL,
    AuthGuard,
    CurrentUser,
)


class DefaultContext(BaseContext):
    group_session = GroupSession()
    session = Session()
    URL = URL()
    auth_guard = AuthGuard()
    current_user = CurrentUser()
