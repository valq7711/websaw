from websaw import DefaultApp, DefaultContext
from websaw.core import Fixture
from websaw.fixtures import XAuth
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

class Context(info.Context, auth.Context, DefaultContext):
    env={
        'menus' : [],
        'menu': [],
        'default_template_context': dict(user = ''),
        'default_template_context': dict(buttons = ''),
        
    }
    index_template = UTemplate(ut.index)
    menu=menu

ctxd = Context()
app = DefaultApp(ctxd, config=dict(group_name='websaw_apps_group_one'), name=__package__)

# use mixin(s)
app.mixin(info.app, auth.app)

@app.route('index')
@app.use(ctxd.menu, ctxd.index_template)  # note there is no session, but it used!
def index(ctx: Context):
    user=ctx.current_user.user
    flash = ctx.flash
    ret = {
        k: ctx[k]
        for k in 'app_name base_url static_base_url folder template_folder static_folder'.split()
    }
    ret['app_data_keys'] = [*ctx.app_data.__dict__]
    ret['env'] = ctx.env
    ret['ctx_fixtures'] = {k: repr(f) for k, f in ctx._fixt.items()}
    return dict(msg=ret)

@app.route('about')
@app.use(ctxd.menu,ut.about) 
def about(ctx: Context):
    ret = dict(mixin = 'http://127.0.0.1:8000/basic',
                index = 'http://127.0.0.1:8000/basic/index',
                welcome='http://127.0.0.1:8000/basic/welcome',
                session='http://127.0.0.1:8000/basic/session',
                use_mixin_template='http://127.0.0.1:8000/basic/use_mixin_template',
                template_overwrite= 'http://127.0.0.1:8000/basic/mixin_template_overwritten',
                info= 'http://127.0.0.1:8000/basic/info/app'
                )
    
    return dict(msg=ret)

# Use the  local 'private' index template implicitly
@app.route('session')
@app.use(ut.index)
def session(ctx: Context):
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

