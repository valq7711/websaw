from websaw import DefaultApp, DefaultContext, XAuth, AuthErr, redirect
from websaw.core import Fixture
import ombott


ombott.default_app().setup(dict(debug=True))


class Auth(XAuth):
    users = {}

    def register(self, fields):
        self.users[fields['id']] = fields

    def user_by_login(self, login: str) -> dict:
        login = login.lower()
        user = (u for u in self.users.values() if u['name'].lower() == login)
        return next(user, None)

    def user_for_session(self, user):
        suser = super().user_for_session(user)
        suser['email'] = user['email']
        suser['name'] = user['name']
        return suser


auth = Auth()


auth.register(dict(
    id=1,
    name='Tom',
    password=auth.crypt('tom_pass'),
    is_blocked=False,
    email='tom@qq.com'
))

auth.register(dict(
    id=2,
    name='Kevin',
    password=auth.crypt('kevin_pass'),
    is_blocked=False,
    email='kevin@qq.com'
))

auth.register(dict(
    id=3,
    name='John',
    password=auth.crypt('john_pass'),
    is_blocked=True,
    email='john@qq.com'
))

# extend default context with our fixture
class Context(DefaultContext):
    auth = auth


ctx_ = Context()
app = DefaultApp(ctx_, config=dict(group_name='websaw_apps_group_one'), name=__package__)


@app.route('login')
def login(ctx: Context):
    q = ctx.request.query
    user, autherr = ctx.auth.login(q.login, q.pw)
    if user:
        redirect(ctx.URL('private'))
    return autherr.as_dict()


@app.route('logout')
def logout(ctx: Context):
    user = ctx.auth.user or dict(name="Guest")
    ctx.auth.logout()
    return f"Byе {user['name']}!"


@app.route('private')
@app.use(ctx_.auth_guard)
def private(ctx: Context):
    return dict(user_in_session=ctx.auth_guard.user)

