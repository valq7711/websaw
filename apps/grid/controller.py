from websaw import DefaultApp, DefaultContext, redirect
from websaw.core import Fixture

import ombott

from . import grid_templates as gt
from . import settings

ombott.default_app().setup(dict(debug=True))

from .todo_db import db
from .. common.common_utils import SimpleGrid

# extend default context with our fixture
class Context(DefaultContext):
    db=db
    

ctxd = Context()
app = DefaultApp(ctxd, name=__package__)


@app.route('index')
@app.use(gt.grid_template)
def index(ctx: Context):
    db = ctx.db
    grid=SimpleGrid(ctx, 'db', db.todo, is_crud=False, page_title='Simple Grid no CRUD')
    
    if grid().accepted:
        ## do some additonal processing here
        print('Grid is good')
    else:
        ## raise the appropriate errors
        print('Grid is bad')
    return dict(grid= grid.get_options())        
