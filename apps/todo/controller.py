from websaw import DefaultApp, DefaultContext, redirect
from websaw.core import Fixture
import ombott

from . import todo_templates as tt

ombott.default_app().setup(dict(debug=True))

from .todo_db import db
from .. common.common_utils import SQLForm

# extend default context with our fixture
class Context(DefaultContext):
    db=db
    
ctxd = Context()
app = DefaultApp(ctxd, name=__package__)


@app.route('index')
@app.use(tt.todo_template)
def index(ctx: Context):
    session = ctx.session
    db = ctx.db
    session["counter"] = session.get("counter", 0) + 1
    list_items = db(db.todo).select()
    list_count = len(list_items)
    return dict(show_form=False, items_count=list_count, items = list_items.as_dict(), session=session)


@app.route('todo', method=['GET', 'POST'])
@app.use(tt.todo_template)
def index(ctx: Context):
    session = ctx.session
    db = ctx.db
    
    query = ctx.request.query.decode()
    action = query.get("action")
    if not action:
        redirect(ctx.URL('index'))
    else:
        list_items = db(db.todo).select()
        list_count = len(list_items)
        
        form = SQLForm(db.todo) #intialise our form
        if action == 'new':
            if form.process(ctx, db, db.todo, None).accepted:
                if ctx.request.method == 'POST':
                    redirect(ctx.URL('index'))
        
        if action == 'update':
            pid = query.get('pid', None)
            if not pid:
                redirect(ctx.URL('index'))
            todo = db(db.todo.id == int(pid)).select().first()
            
            if form.process(ctx, db, db.todo, todo).accepted:
                if ctx.request.method == 'POST':
                    redirect(ctx.URL('index'))
    
        if action == 'delete':
            pid = query.get('pid', None)
            if not pid:
                redirect(ctx.URL('index'))
            todo = db.todo(pid)
            if todo is None:
                redirect(ctx.URL("index"))
            db(db.todo.id == pid).delete()
            db.commit()
            redirect(ctx.URL("index"))
        
        return dict(show_form=True, form_options = form.get_options(), items_count=list_count, items = list_items.as_dict(), session=session)

