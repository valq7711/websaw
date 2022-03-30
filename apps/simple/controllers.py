from websaw import DefaultApp, DefaultContext, Template
from websaw.core import Fixture
from websaw.fixtures import Env
import ombott

from ..mixins import info

ombott.default_app().setup(dict(debug=True))


# make a simple custom fixture that uses another fixture (session)
class LastVisited(Fixture):
    def take_off(self, ctx: DefaultContext):
        session = ctx.session  # magic goes here - we touch session and ctx activates it!
        last_visited = session.get('last_visited', [])
        last_visited.append(ctx.request.path)
        last_visited = last_visited[-5:]
        session['last_visited'] = last_visited


# extend default context with our fixture and info-mixin context
class Context(info.Context, DefaultContext):
    track_visited = LastVisited()
    welcome_templ_overwrite = Template('welcome.html')
    env = {
        'foo': 'foo_value'
    }


ctxd = Context()
app = DefaultApp(ctxd, dict(group_name='websaw_apps_group_one'), name=__package__)

# use mixin(s)
app.mixin(info.app)


@app.route('index')
@app.use(ctxd.track_visited)  # note there is no session, but it used!
def index(ctx: Context):
    ret = {
        k: ctx[k]
        for k in 'app_name base_url static_base_url folder template_folder static_folder'.split()
    }
    ret['app_data_keys'] = [*ctx.app_data.__dict__]
    ret['env'] = ctx.env
    return ret


@app.route('set_env')
@app.use(Env(foo='change foo value', bar='bar value'))
def set_env(ctx: Context):
    return ctx.env


@app.route('session')
def session(ctx: Context):
    ret = {
        'group_session_data': {**ctx.group_session},
        'session_data': {**ctx.session},
        'local_data_keys': [*ctx.session.data.__dict__],
    }
    return ret


# reuse mixin template
@app.route('reuse_welcome_template')
@app.use(ctxd.welcome_templ)
def app_welcome(ctx: Context):
    return dict(msg='Hey! This is message from app controller')



# let's go to:
# http://127.0.0.1:8000/simple
# http://127.0.0.1:8000/simple/index
# http://127.0.0.1:8000/simple/session
# http://127.0.0.1:8000/simple/reuse_welcome_template

# provided by mixin
# http://127.0.0.1:8000/simple/welcome
# http://127.0.0.1:8000/simple/welcome_template_overwritten
# http://127.0.0.1:8000/simple/info/app

