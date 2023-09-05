from websaw import DefaultApp, DefaultContext, Reloader
from websaw.core import Fixture
from websaw.fixtures import Env, XAuth
from websaw.templates import UTemplate
import ombott

from . import utemplates as ut

ombott.default_app().setup(dict(debug=True))


class GetUserMenus(XAuth):
    
    def take_on(self, ctx:DefaultContext):
        ctx.env['default_template_context']['menu'] = [
        ]
        

menu=GetUserMenus()

# extend default context with our fixture and info-mixin context
class Context(DefaultContext):
    env={
        'menus' : [],
        'menu': [],
        'default_template_context': dict(user = ''),
        'default_template_context': dict(buttons = ''),
        
    }
    menu=menu

ctxd = Context()
app = DefaultApp(ctxd, config=dict(group_name='websaw_apps_group_one'), name=__package__)

# use mixin(s)

@app.route('index')
@app.use(ctxd.menu, ut.index)  # note there is no session, but it used!
def index(ctx: Context):
    return dict()

