from websaw import DefaultApp, DefaultContext, redirect
from websaw.core import Fixture

import ombott

from . import grid_templates as gt
from . import settings

ombott.default_app().setup(dict(debug=True))

from .todo_db import db
from .. common.common_utils import SQLForm
from .. common.common_utils import SQLGrid

#class DBRegistry(Fixture):
#    def __init__(self):
#        self.dbs_keys = set()

# extend default context with our fixture
class Context(DefaultContext):
    db=db

    
ctxd = Context()
app = DefaultApp(ctxd, name=__package__)


@app.route('index')
@app.use(gt.grid_template)
def index(ctx: Context):
    db = ctx.db
    grid=SQLGrid(ctx, 'db', db.todo, upload=True, download=True, page_title='My Todos Grid')
    
    if grid().accepted:
        ## do some additonal processing here
        print('Grid is good')
    else:
        ## raise the appropriate errors
        print('Grid is bad')
    return dict(grid= grid.get_options())        
    
    
@app.route('actions', method=['GET', 'POST'])
@app.use(gt.action_template)
def action(ctx: Context):
    session = ctx.session
    
    query = ctx.request.query.decode()
    action = query.get("action")
    db = query.get('cdb')
    table = query.get('table')
    show_buttons=True
        
    if not action or not table:
        redirect(ctx.URL('index'))
    else:
        db = ctx.ask('db')
        form = SQLForm(db[table]) #intialise our form
        if action == 'create':
            if form.process(ctx, db, db[table], None).accepted:
                if ctx.request.method == 'POST':
                    redirect(ctx.URL('index'))
        
        elif action == 'update':
            id = query.get('id', None)
            if not id:
                redirect(ctx.URL('index'))
            todo = db(db[table].id == int(id)).select().first()
            
            if form.process(ctx, db, db.todo, todo).accepted:
                if ctx.request.method == 'POST':
                    redirect(ctx.URL('index'))
    
        elif action == 'view':
            show_buttons = False
            id = query.get('id', None)
            if not id:
                redirect(ctx.URL('index'))
            todo = db(db[table].id == int(id)).select().first()
            
            if form.process(ctx, db, db.todo, todo).accepted:
                if ctx.request.method == 'POST':
                    redirect(ctx.URL('index'))
    
        if action == 'delete':
            id = query.get('id', None)
            if not id:
                redirect(ctx.URL('index'))
            todo = db[table](id)
            if todo is None:
                redirect(ctx.URL("index"))
            db(db[table].id == id).delete()
            db.commit()
            redirect(ctx.URL("index"))
        
        elif action == 'download':
            
            filename = settings.DOWNLOAD_FOLDER+'/'+table+'.csv'
            with open(filename, 'w', encoding='utf-8', newline='') as dumpfile:
                dumpfile.write(str(db(db[table]).select()))
            redirect(ctx.URL("index"))

        elif action == 'upload':
            
            filename = settings.UPLOAD_FOLDER+'/'+table+'.csv'
            try:
                with open(filename, 'r', encoding='utf-8', newline='') as dumpfile:
                    db[table].import_from_csv_file(dumpfile)
                db.commit()    
            except Exception as e:
                redirect(ctx.URL('index'))
            finally:
                redirect(ctx.URL("index"))

        return dict(form_options = form.get_options(), show_button=show_buttons)

