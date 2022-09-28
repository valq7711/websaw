from websaw import DefaultApp, DefaultContext, Reloader
from websaw.core import Fixture
from websaw.fixtures import Env, XAuth
from websaw.templates import UTemplate
import ombott

from ..mixins import auth, db_admin

from . import utemplates as ut
from .app_db import db

ombott.default_app().setup(dict(debug=True))


class GetUserMenus(XAuth):
    
    def take_on(self, ctx:DefaultContext):
        navbar = ctx.navbar
        user = ctx.current_user.user
        ctx.env['default_template_context']['menu'] = [
            {'label': 'Home', 'href':ctx.URL('index')},
            {'label': 'About', 'href':ctx.URL('about')},
            {'label': 'DB Admin', 'href':ctx.URL('db_admin')}
            ]

menu=GetUserMenus()

# extend default context with our fixture and info-mixin context
class Context(db_admin.Context, auth.Context, DefaultContext):
    env={
        'menus' : [],
        'menu': [],
        'default_template_context': dict(user = ''),
        'default_template_context': dict(buttons = ''),
        
    }
    db = db
    menu=menu

ctxd = Context()
app = DefaultApp(ctxd, config=dict(group_name='websaw_apps_group_one'), name=__package__)

# use mixin(s)
app.mixin(db_admin.app, auth.app)

@app.route('index')
@app.use(ctxd.menu, ut.index)  # note there is no session, but it used!
def index(ctx: Context):
    user=ctx.current_user.user
    session = ctx.session
    flash = ctx.flash
    ret = 'You can customise this page by adding any components or functionality you need'
    return dict(msg=ret)

@app.route('about')
@app.use(ctxd.menu, ut.about)  # note there is no session, but it used!
def about(ctx: Context):
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

