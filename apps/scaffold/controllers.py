from websaw import DefaultApp, DefaultContext, Reloader
from websaw.core import Fixture
from websaw.fixtures import Env, XAuth
from websaw.templates import UTemplate
import ombott

from ..mixins import info, auth
from . import utemplates as ut

ombott.default_app().setup(dict(debug=True))


class GetUserMenus(XAuth):
    
    def take_on(self, ctx:DefaultContext):
        navbar = ctx.navbar
        user = ctx.current_user.user
        ctx.env['default_template_context']['menu'] = [
            {'label': 'Home', 'href':ctx.URL('index')},
            {'label': 'About', 'href':ctx.URL('about')}
            ]

menu=GetUserMenus()


# make a simple custom fixture that uses another fixture (session)
class LastVisited(Fixture):
    def take_off(self, ctx: DefaultContext):
        session = ctx.session  # magic goes here - we touch session and ctx activates it!
        last_visited = session.get('last_visited', [])
        last_visited.append(ctx.request.path)
        last_visited = last_visited[-5:]
        session['last_visited'] = last_visited

# make a simple fixture that deals with the navbar. This can be extended to use auth
# extend default context with our fixture and info-mixin context
class Context(info.Context, auth.Context, DefaultContext):
    env={
        'menus' : [],
        'menu': [],
        'default_template_context': dict(user = ''),
        'default_template_context': dict(buttons = ''),
        
    }
    track_visited = LastVisited()
    index_template = UTemplate(ut.index)
    menu=menu

ctxd = Context()
app = DefaultApp(ctxd, config=dict(group_name='websaw_apps_group_one'), name=__package__)

# use mixin(s)
app.mixin(info.app, auth.app)

@app.route('index')
@app.use(ctxd.menu, ctxd.track_visited, ctxd.index_template)  # note there is no session, but it used!
def index(ctx: Context):
    user=ctx.current_user.user
    
    print('User is ', user)
    ret = {
        k: ctx[k]
        for k in 'app_name base_url static_base_url folder template_folder static_folder'.split()
    }
    ret['app_data_keys'] = [*ctx.app_data.__dict__]
    ret['env'] = ctx.env
    ret['ctx_fixtures'] = {k: repr(f) for k, f in ctx._fixt.items()}
    return dict(msg=ret)

@app.route('about')
@app.use(ctxd.menu, ctxd.track_visited, ctxd.index_template)  # note there is no session, but it used!
def index(ctx: Context):
    ret = {
        k: ctx[k]
        for k in 'app_name base_url static_base_url folder template_folder static_folder'.split()
    }
    ret['app_data_keys'] = [*ctx.app_data.__dict__]
    ret['env'] = ctx.env
    ret['ctx_fixtures'] = {k: repr(f) for k, f in ctx._fixt.items()}
    return dict(msg=ret)


@app.route('set_env')
@app.use(Env(foo='change foo value', bar='bar value'))
def set_env(ctx: Context):
    return ctx.env


# Use the  local 'private' index template
@app.route('session')
@app.use(ut.index)
def session(ctx: Context):
    ctx.env['default_template_context']['user'] = 'Fred Elliot'
    ret = {
        'group_session_data': {**ctx.group_session},
        'session_data': {**ctx.session},
        'local_data_keys': [*ctx.session.data.__dict__],

    }
    return dict(msg=ret)


# use mixin template
@app.route('use_mixin_template')
@app.use(ctxd.welcome_template)
def app_welcome(ctx: Context):
    return dict(msg='Hey! This is message from app controller using the INFO mixin template')

# use another specific template
@app.route('upytl_demo')
@app.use(ut.upytl_demo)
def upytl_demo(ctx: Context):
    return dict(msg='Hey! This page is rendered using UPYTL and the upytl_demo Template')


# let's go to:
# http://127.0.0.1:8000/scaffold
# http://127.0.0.1:8000/scaffold/index
# http://127.0.0.1:8000/scaffold/session
# http://127.0.0.1:8000/scaffold/use_mixin_template
# http://127.0.0.1:8000/scaffold/upytl_demo

# provided by mixins/info
# http://127.0.0.1:8000/scaffold/welcome
# http://127.0.0.1:8000/scaffold/mixin_template_overwritten
# http://127.0.0.1:8000/simple/info/app

